#!/usr/bin/env python3
import gi
from gi.repository import Gio

class myFile():
    def __init__(self,fileName):
        self.fileName = fileName
        self.fileHandler = Gio.File.new_for_path(fileName)

    def isFileExist(self):
        if(self.fileHandler.query_exists()):
            print("file exists\n")
        else:
            print("file not exists\n")
    def write(self,content):
        dataOutStream = Gio.DataOutputStream.new(Gio.File.append_to(self.fileHandler,Gio.FileCreateFlags.NONE,None))
        dataOutStream.put_string(content+"\n");

if __name__ == "__main__":
    oFile = myFile("./test.txt")
    oFile.isFileExist()
    oFile.write("this is my content");
