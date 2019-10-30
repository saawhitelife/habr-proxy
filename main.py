from http.server import HTTPServer, SimpleHTTPRequestHandler
import re
from requests import get as rget
from bs4 import BeautifulSoup as bs


def create_page_to_display(path):
    if len(path.split(".")) > 1:
        return
    regex = re.compile(r'(\s)(\b[а-яА-Я]{6}\b)([\s/.,:])', re.U)
    response = rget('https://habr.com' + str(path))
    open("page.html", 'w').write(response.text)
    with open("page.html", "r") as f:
        content = f.read()
    new_content = content.replace("https://habr.com",
                                  "http://127.0.0.1:8000")
    new_content_2 = re.sub(regex, r'\1\2™\3', new_content)
    open("page.html", 'w').write(new_content_2)
    soup = bs(new_content, 'html.parser')
    my_div = soup.find("div", class_="post__wrapper")
    if my_div:
        for child in my_div.descendants:
            if child.string:
                child.string = re.sub(regex, r'\1\2™\3', child.string)
                print(child.string)
    print(soup)
    open("page.html", 'w').write(str(soup))
    # with open('page.html', "w") as page_writer:
    #     for line in response.iter_lines(decode_unicode=1):
    #         # print("TYPE OF LINE %s" % type(line))
    #         if type(line) is bytes:
    #             pass
    #         print("LINE MB? %s" % line)
    #         new_line = str(line).replace("https://habr.com",
    #                                 "http://127.0.0.1:8000")\
    #         # .replace("href=\"/", "href=\"http://127.0.0.1:8000/")
    #         # new_line = new_line.replace("href=\"/",
    #         #                         "href=\"http://127.0.0.1:8000/")
    #         print("str(new_line) IS %s" % str(new_line))
    #         # new_line_2 = re.sub(regex, r'\1\2™\3', new_line)
    #         # new_line_3 = re.sub(regex_2, r'\1\2™\3', new_line_2)
    #         page_writer.write(new_line)
    # page_writer.close()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print("SELF PATH %s" % self.path)
        # if self.path.endswith("svg"):
        #     response = rget('https://habr.com' + self.path)
        #     open(self.path.lstrip("/"), 'wb').write(response.content)
        #     file = open(self.path.lstrip("/"), 'rb')
        #     self.send_response(200)
        #     self.send_header('Content-type', 'image/svg+xml')
        #     self.end_headers()
        #     self.wfile.write(file.read())
        #     file.close()
        # elif self.path.endswith("webmanifest"):
        #     response = rget('https://habr.com' + self.path)
        #     open(self.path.lstrip("/"), 'wb').write(response.content)
        #     file = open(self.path.lstrip("/"), 'rb')
        #     self.send_response(200)
        #     self.send_header('Content-type', 'application/manifest+json')
        #     self.end_headers()
        #     self.wfile.write(file.read())
        #     file.close()
        # elif str(self.path).endswith("png"):
        #
        # else:
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
