#!/usr/bin/env python
import os,sys
import glob
import Image

sourceFileDir="./source/"
for file in glob.glob(sourceFileDir+"*.jpg"):
    print file
    im=Image.open(file)
    box=(116,230,815,928)
    region=im.crop(box)
    region.save(sourceFileDir+"output_"+os.path.basename(file)[:-4]+".bmp","BMP")

