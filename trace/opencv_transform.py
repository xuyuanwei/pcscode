#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import cv2
import numpy
import glob
import os

sourceFileDir="./source/"
 
def get_perspective_mat():
    # [x,y]
    source_4points=numpy.array([
        [ 140,629 ], 
        [ 559,629 ],
        [ 140,0  ], 
        [ 559,0  ]
        ],
        numpy.float32)
    x_offset=350
    target_4points=numpy.array([
        [ 38+x_offset,242  ], 
        [ 501+x_offset,242 ], 
        [ 211+x_offset,36  ], 
        [ 332+x_offset,37  ]
        ],
        numpy.float32)

    #print(source_4points)
    #print(target_4points)

    perspective_mat=cv2.getPerspectiveTransform(source_4points,target_4points)
    return perspective_mat

if __name__ == '__main__':
    perspective_mat=get_perspective_mat()
    for file in glob.glob(sourceFileDir+"*.jpg"):
        img=cv2.imread(file)
        print("processing file: " + file)
        crop_startx=116
        crop_starty=230
        crop_endx= 815
        crop_endy= 928

        # crop rectangle [y_min:y_max,x_min:x_max]
        img=img[crop_starty:crop_endy,crop_startx:crop_endx]
        #cv2.imwrite("crop.bmp",img)

        #(x_width,y_height)
        size=(1280,480)
        #perspective_dst=cv2.cv.CreateMat(480,1280,cv2.cv.CV_32FC1)
        perspective_dst=cv2.warpPerspective(img,perspective_mat,size)
        outputFileName="transformed_"+os.path.basename(file)[:-4]+".bmp"
        cv2.imwrite(sourceFileDir+"/"+outputFileName,perspective_dst)
 
 
