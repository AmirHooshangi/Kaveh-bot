import http.client
import schedule
import socketserver
import time
import threading
from http.server import BaseHTTPRequestHandler
import sys
import os

print(os.system('ls'))
ip = sys.argv[1]

def register_proxy():
    print("Call shodamaaaa")
    connection = http.client.HTTPConnection("52.58.234.28:6060")
    connection.request("GET", "/register?ip="+ip)

schedule.every().minute.do(register_proxy)

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if '/daemon' in self.path:
            print("I was called")
            self.send_response_only(200)
            self.wfile.write('Hello World'.encode())

def schedule():
    while 1:
        try:
            register_proxy()
        except Exception as e: print(e)
        time.sleep(10)

# makes our logic non blocking
thread = threading.Thread(target=schedule)
thread.start()


with socketserver.TCPServer(("", 7070), GetHandler) as httpd:
    print("serving at port", 7070)
    httpd.serve_forever()

