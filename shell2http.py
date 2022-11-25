import subprocess
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer

routes = {}

def shellHTTPRequestHandler(is_output)
    print("is_output",is_output)
    class ShellHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            if self.path in routes:
                if(is_output):
                    output = subprocess.Popen(routes[self.path], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()
                    self.wfile.write(output)
                else:
                    subprocess.Popen(routes[self.path], shell=True)

                
    return ShellHTTPRequestHandler


def serve():
    parser = ArgumentParser()
    parser.add_argument("-o","--output",action="store_true",help="Send back ouput")
    parser.add_argument('-p', '--port', default=8080, type=int)
    parser.add_argument('command', nargs='+')
    args = parser.parse_args()

    if len(args.command) % 2:
        args.command = ['/'] + args.command

    global routes
    routes = dict(zip(args.command[0::2], args.command[1::2]))
    for path, command in routes.items():
        print(f'http://localhost:{args.port}{path}', command)
    with HTTPServer(('', args.port), shellHTTPRequestHandler(args.ouput)) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    serve()
