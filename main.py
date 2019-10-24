from http.server import HTTPServer, SimpleHTTPRequestHandler
import re
from requests import get as rget


def create_page_to_display(path):
    regex = re.compile(r'(\s)(\b\w{6}\b)([\s/.,:])', re.U)
    regex_2 = re.compile(r'(<p>)(\b\w{6}\b)([,])?', re.M | re.U)
    response = rget('https://habr.com' + path)
    with open('page.html', "w") as page_writer:
        for line in response.iter_lines(decode_unicode=True):
            new_line = line.replace("https://habr.com",
                                    "http://127.0.0.1:8000")
            new_line_2 = re.sub(regex, r'\1\2™\3', new_line)
            new_line_3 = re.sub(regex_2, r'\1\2™\3', new_line_2)
            page_writer.write(new_line_3)
    page_writer.close()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        create_page_to_display(self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('page.html', 'rb') as html_page_reader:
            html = html_page_reader.read()
            self.wfile.write(html)


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()


