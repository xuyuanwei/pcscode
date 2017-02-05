#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import glob
from stat import *
import shutil
import time

global linux
linux=1
if linux:
	sourcedir="./"
	targetdir="/home/cylinc/.config/libreoffice/4/user/Scripts/python/"
else:
	sourcedir=".\\"
	#targetdir="C:\\Program Files\\LibreOffice 3.4\\Basis\\share\\Scripts\\python\\myscript\\"
	targetdir="C:\\Documents and Settings\\Administrator\\Application Data\\LibreOffice\\3\\user\\Scripts\\python\\"
count=0
print(str(time.strftime('%X %x')) +":" + "file Sync monitor start")
while True:
    for file in glob.glob(sourcedir+"*.py"):
        filebasename=os.path.basename(file)
        mode=os.stat(file)[ST_MODE]     #int type
        if not S_ISREG(mode):
            continue
        # if the target file exists
        if not os.path.exists(targetdir+filebasename):
            shutil.copy(file,targetdir)
            print(str(time.strftime('%X %x'))+ ":")
            print("file not existing: " + filebasename + " is synced")
            continue

        # if the source file is newer than the one in the dsc
        mtime_src=os.stat(file)[ST_MTIME]
        mtime_dst=os.stat(targetdir+filebasename)[ST_MTIME]
        if mtime_src>mtime_dst:
            shutil.copy(file,targetdir)
            print(str(time.strftime('%X %x')) + ":")
            print("file is newer: " + filebasename + " is synced")
            continue
    count=count+1
    '''
    if count==1:
        break
        '''
    time.sleep(5)
