from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import sys
import time


ADDR = '0.0.0.0'
PORT = 8088
TEMPLATE = (
    '<!DOCTYPE html>'
    '<html>'
    '  <head><title>Request Counter</title></head>'
    '  <body>'
    '    <h1 style="text-align:center">{} requests since<br/>{}</h1>'
    '  </body>'
    '</html>'
)


class CountHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.server.req_count += 1
        print('\nrequest count:', self.server.req_count)
        self.send_response(405)
        return

    def do_GET(self):
        self.server.req_count += 1

        if len(sys.argv) == 2:
            try:
                sleep_seconds = int(sys.argv[1])
                time.sleep(sleep_seconds)
            except:
                pass

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        out = TEMPLATE.format(
            self.server.req_count,
            self.server.start.strftime('%m/%d/%Y %H:%M:%S')
        ).encode()

        print('\nrequest count:', self.server.req_count)
        self.wfile.write(out)
        return


class CountServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.req_count = 0
        self.start = datetime.now()
        super().__init__(*args, **kwargs)


def run(server_class=CountServer, handler_class=CountHandler):
    server_address = (ADDR, PORT)
    httpd = server_class(server_address, handler_class)
    try:
        print('starting server...\n')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n...closing connection')
        httpd.socket.close()

if __name__ == '__main__':
    run()
