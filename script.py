import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import os
ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    # get the heroku port
    PORT = int(os.environ.get("PORT", 17995))  # as per OP comments default is 17995
else:
    PORT = 3000

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.write("Heroku is awesome")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

try:
    server = ThreadedTCPServer(('', PORT), myHandler)
    print ('Started httpserver on port ' , PORT)
    ip,port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    allow_reuse_address = True
    server.serve_forever()

except KeyboardInterrupt:
    print ('CTRL + C RECEIVED - Shutting down the REST server')
    server.socket.close()
