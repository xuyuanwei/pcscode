#!/usr/bin/env python3
import gi
gi.require_version('Soup', '2.4')
gi.require_version('Json', '1.0')
from gi.repository import Soup
from gi.repository import Json
from gi.repository import GLib

class HttpClient():
    def __init__(self):
        self.session = Soup.SessionSync.new()
        self.message = None

    def postMessage(self,url,content):
        self.message = Soup.Message.new("POST", url)
        self.message.set_request("text/html",Soup.MemoryUse.COPY,content.encode('utf-8'))
        self.session.send_message(self.message)
        print("msg post data = " + content)
        print("msg return code = " + str(self.message.status_code))
        print("msg return body = " + str(self.message.props.response_body_data.get_data()))

    def jsonBuild(self):
        build = Json.Builder.new()
        build.begin_object()
        build.set_member_name("memName")
        build.add_string_value("memValue")
        build.end_object()

        generator = Json.Generator.new();
        root = build.get_root()  #Json.Node
        generator.set_root(root)
        #print("json builder return: " + str(generator.to_data()))
        return str(generator.to_data()[0])


if __name__ == "__main__":
    url = "http://server.addr.com"
    postTest = HttpClient()
    postTest.postMessage(url,postTest.jsonBuild());
