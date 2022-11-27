import os
import subprocess
from argparse import ArgumentParser
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

index_page = '<!DOCTYPE html><html><head><title>Index</title><style>a{display:block;margin:16px}</style></head><body>%s</body></html>'


def shellHTTPRequestHandler(args):

    if len(args.command) % 2:
        args.command = ['/'] + args.command

    routes = dict(zip(args.command[0::2], args.command[1::2]))
    for path, command in routes.items():
        print(f'http://localhost:{args.port}{path}', command)

    class ShellHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            parsed_url = urlparse(self.path)
            if args.sse:
                self.send_header('Content-Type', 'text/event-stream')
                args.output = True
            self.end_headers()
            if parsed_url.path == '/' and '/' not in routes and not args.no_index:
                paths = list(routes.keys())
                if args.add_exit:
                    paths.append('/exit')
                html = (index_page % ''.join(
                    map(lambda p: f'<a href={p} target=_blank>{p}</a>', paths)))
                self.wfile.write(html.encode('utf-8'))
            if parsed_url.path in routes:
                kwargs = {
                    'args': routes[parsed_url.path],
                    'shell': True
                }
                if args.form:
                    query = dict(('v_' + k, '\t'.join(v))
                                 for k, v in parse_qs(parsed_url.query).items())
                    kwargs['env'] = {**os.environ, **query}
                if args.output:
                    kwargs['stdout'] = subprocess.PIPE
                proc = subprocess.Popen(**kwargs)
                if args.output:
                    for line in proc.stdout:
                        self.wfile.write(line)
            if parsed_url.path == '/exit' and args.add_exit:
                exit()

    return ShellHTTPRequestHandler


def serve():
    parser = ArgumentParser()
    parser.add_argument('-form', action='store_true',
                        help='parse query into environment vars')
    parser.add_argument('-no-index', action='store_true',
                        help='do not generate index page')
    parser.add_argument('-add-exit', action='store_true',
                        help='add /exit command')
    parser.add_argument('-output', action='store_true',
                        help='send back output')
    parser.add_argument('-sse', action='store_true',
                        help='use Server Sent Events')
    parser.add_argument('-p', '--port', default=8080, type=int)
    parser.add_argument('command', nargs='+')
    args = parser.parse_args()

    with HTTPServer(('', args.port), shellHTTPRequestHandler(args)) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    serve()
