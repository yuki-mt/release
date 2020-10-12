from http.server import SimpleHTTPRequestHandler, HTTPServer
import base64

BASIC_USERNAME = 'a'
BASIC_PW= 'b'
PORT = 8000

def pass_basic_auth(auth_header: str) -> bool:
    encoded_value = base64.b64encode(f"{BASIC_USERNAME}:{BASIC_PW}".encode('utf-8'))
    check_value = "Basic {}".format(encoded_value.decode(encoding='utf-8'))
    return auth_header == check_value

class GetHandler(SimpleHTTPRequestHandler):
    def run(self):
        auth = dict(self.headers).get('Authorization')
        print(self.headers)
        print(self.path)
        print(pass_basic_auth(auth))
        SimpleHTTPRequestHandler.do_GET(self)

    def do_GET(self):
        self.run()

    def do_HEAD(self):
        self.run()


with HTTPServer(("", PORT), GetHandler) as server:
    print("serving at port", PORT)
    server.serve_forever()
