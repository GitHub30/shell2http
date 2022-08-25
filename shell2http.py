from subprocess import Popen
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer

routes = {}


class ShellHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path in routes:
            Popen(routes[self.path], shell=True)


def serve():
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int)
    parser.add_argument('command', nargs='+')
    args = parser.parse_args()

    if len(args.command) % 2:
        args.command = ['/'] + args.command

    global routes
    routes = dict(zip(args.command[0::2], args.command[1::2]))
    for path, command in routes.items():
        print(f'http://localhost:{args.port}{path}', command)
    with HTTPServer(('', args.port), ShellHTTPRequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    serve()
