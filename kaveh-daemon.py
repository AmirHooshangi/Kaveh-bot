import http.client
import schedule
import socketserver
import time
import threading
from http.server import BaseHTTPRequestHandler

import os

print(os.system('ls'))


def register_proxy():
    print("Call shodamaaaa")
    connection = http.client.HTTPConnection("127.0.0.1:6060")
    connection.request("GET", "/oskesh?ip=52.58.234.28:7070")

schedule.every().minute.do(register_proxy)

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if '/daemon' in self.path:
            print("I was called")
            self.send_response_only(200)
            self.wfile.write('Hello World'.encode())

def schedule():
    while 1:
        register_proxy()
        time.sleep(10)

# makes our logic non blocking
thread = threading.Thread(target=schedule)
thread.start()


with socketserver.TCPServer(("", 7070), GetHandler) as httpd:
    print("serving at port", 7070)
    httpd.serve_forever()

