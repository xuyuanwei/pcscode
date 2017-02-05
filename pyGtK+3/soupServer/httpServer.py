#!/usr/bin/env python3
# soup server demo
import gi
gi.require_version('Soup', '2.4')
from gi.repository import Soup
from gi.repository import Json

class TestServer():
    def __init__(self):
        self.server = Soup.Server()
        self.server.add_handler("/",self.default_handler)
        self.server.add_handler("/path/subpath",self.test_handler)
        self.server.listen_local(8081,0)

    def default_handler(self, server, msg, path, query, client):
        response = "<html><head><title>404</title></head><body><h1>404</h1></body></html>"
        msg.set_response("text/html", Soup.MemoryUse.COPY,response.encode('utf-8'))
        msg.set_status(404)
        print("test_handler called")

    def test_handler(self, server, msg, path, query, client):
        print("test handler called")
        msg.status_code = 404

    def run(self):
        self.server.run()

if __name__ == "__main__":
    testServer = TestServer()
    testServer.run()
