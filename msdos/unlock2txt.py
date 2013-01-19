#!/usr/bin/env python
# -*- coding: utf-8 -*-
from win32com.client import Dispatch
import win32com.client
import os
import re

'''
def getUsedRange(self,wsheet):
    return (wsheet.UsedRange.Row,
            wsheet.UsedRange.Column,
            wsheet.UsedRange.Rows.Count,
            wsheet.UsedRange.Columns.Count)
'''

if __name__ == "__main__":
    #PNFILE = r'c:\screenshot.bmp'
    #xls = easyExcel(r'D:\test.xls')
    #xls.addPicture('Sheet1', PNFILE, 20,20,1000,1000)
    #xls.cpSheet('Sheet1')
    #xls.save()
    #xls.close()

    #ROWMAX=65536
    ROWMAX=500
    COLMAX=255
    targetdir="e:\\xulin\\tmp\\unlock\\"
    outputdir="e:\\xulin\\tmp\\unlock\\output\\"

    xlsApp = win32com.client.Dispatch('Excel.Application')

    filelist=os.listdir(targetdir)
    #print("filelist: " + str(filelist))
    tableDivider="|"
    sheetnum=1
    for file in filelist:
        fullpath=targetdir+file
        if os.path.isfile(fullpath) and file[len(file)-4:]==".xls":
            print("I:Found xls file :" + file)
            xlsBook_r = xlsApp.Workbooks.Open(fullpath)

            sheetcount=xlsBook_r.Worksheets.Count
            for i in range(1,sheetcount+1):
                sheet=xlsBook_r.Worksheets(i)
                txtfilepath=outputdir+xlsBook_r.Name+"_"+sheet.Name+".txt"
                txtfile=open(txtfilepath,'w')
                ROWMAX=sheet.UsedRange.Row+sheet.UsedRange.Rows.Count-1
                COLMAX=sheet.UsedRange.Column+sheet.UsedRange.Columns.Count-1

                print(sheet.Name+":"+"ROW: " +str(ROWMAX)+" COL:"+str(COLMAX))
                tempstr=""
                progress=0
                for row in range(1,ROWMAX+1):
                    rowdata=sheet.Range(sheet.Cells(row, 1), sheet.Cells(row, COLMAX)).Value
                    #change tuple data to string
                    for t in rowdata:
                        for t1 in t:
                            if t1==None:
                                tempstr=tempstr+tableDivider
                            else:
                                t1=re.sub("\n","+",str(t1))
                                tempstr=tempstr+t1+tableDivider
                        tempstr=tempstr+"\n"
                    #every 10 rows write once
                    if row%10==0:
                        txtfile.write(tempstr)
                        tempstr=""
                    #prompt for running progress
                    tempint=int(row/ROWMAX*10)
                    if tempint>progress:
                        for j in range(1,tempint+1):
                            print('#',end="")
                        print("\n")
                        progress=tempint

                txtfile.write(tempstr)
                txtfile.close()

            xlsBook_r.Close()

