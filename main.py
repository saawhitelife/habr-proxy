from http.server import HTTPServer, SimpleHTTPRequestHandler
import re
import os
from requests import get as rget


def create_page_to_display(path):
    regex = re.compile(r'(\b[а-яА-Я]{6}\b)', re.U)
    response = rget('https://habr.com' + str(path))
    open("page.html", 'w').write(response.text)
    with open("page.html", "r") as html_reader:
        content = html_reader.read()
    html_reader.close()
    content = content.replace("https://habr.com",
                                  "http://127.0.0.1:8000")
    content = re.sub(regex, r'\1™', content)
    open("page.html", 'w').write(content)


def handle_file(path):
    response = rget('https://habr.com' + path)
    if not os.path.exists("/".join(path.lstrip("/").split("/")[:-1])):
        os.makedirs("/".join(path.lstrip("/").split("/")[:-1]))
    open(path.lstrip("/"), 'wb').write(response.content)


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print("SELF PATH %s" % self.path)
        if len(self.path.split(".")) > 1:
            if self.path.endswith("svg"):
                handle_file(self.path)
                file = open(self.path.lstrip("/"), 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
            elif self.path.endswith("woff2"):
                handle_file(self.path)
                file = open(self.path.lstrip("/"), 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'application/font-woff')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
            elif self.path.endswith("png"):
                handle_file(self.path)
                file = open(self.path.lstrip("/"), 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
            elif self.path.endswith("webmanifest"):
                response = rget('https://habr.com' + self.path)
                open(self.path.lstrip("/"), 'wb').write(response.content)
                file = open(self.path.lstrip("/"), 'rb')
                self.send_response(200)
                self.send_header('Content-type', 'application/manifest+json')
                self.end_headers()
                self.wfile.write(file.read())
                file.close()
        else:
            create_page_to_display(self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('page.html', 'rb') as html_reader:
                html = html_reader.read()
                self.wfile.write(html)


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
