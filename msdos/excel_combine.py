#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this code is used to combine the xls files
# currently,only the content of the first sheet will be gathered

from win32com.client import Dispatch
import win32com.client
import os

class easyExcel:
    '''A utility to make it easier to get at Excel. Remembering
      to save the data is your problem, as is error handling.
      Operates on one workbook at a time.'''

    def __init__(self, filename=None):
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''  

    def save(self, newfilename=None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()    

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def getCell(self, sheet, row, col):
#        "Get value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value

    def setCell(self, sheet, row, col, value):
#        "set value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        sht.Cells(row, col).Value = value

    def getRange(self, sheet, row1, col1, row2, col2):
#        "return a 2d array (i.e. tuple of tuples)"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value

    def setRange(self,sheet,row1,col1,tupledata):
        ROWMAX=65536
        COLMAX=255
        sht=self.xlBook.Worksheets(sheet)
        #count tuple size
        rowcount=len(tupledata)
        maxcol=0
        for t in tupledata:
            if len(t)>maxcol:
                maxcol=len(t)
        print("setRange: get tuple")
        
        row=row1
        for t in tupledata:
            col=col1
            for t1 in t:
                sht.Cells(row, col).Value = t1
                col=col+1
            row=row+1
        return 0

    def usedRow(self,sheet):
        sht=self.xlBook.Worksheets(sheet)
        return sht.UsedRange.Row+sht.UsedRange.Rows.Count-1

    def usedCol(self,sheet):
        sht=self.xlBook.Worksheets(sheet)
        return sht.UsedRange.Column+sht.UsedRange.Columns.Count-1

    def addPicture(self, sheet, pictureName, Left, Top, Width, Height):
#        "Insert a picture in sheet"
        sht = self.xlBook.Worksheets(sheet)
        sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height)

    def cpSheet(self, before):
#        "copy sheet"
        shts = self.xlBook.Worksheets
        shts(1).Copy(None,shts(1))

if __name__ == "__main__":
    #PNFILE = r'c:\screenshot.bmp'
    #xls = easyExcel(r'D:\test.xls')
    #xls.addPicture('Sheet1', PNFILE, 20,20,1000,1000)
    #xls.cpSheet('Sheet1')
    #xls.save()
    #xls.close()

    ROWMAX=65536
    COLMAX=255
    #targetdir is fixed
    targetdir="e:\\xulin\\tmp\\combine\\"
    outputfile=targetdir+"output.xls"
    outputxls=easyExcel()
    outputStartRow=1
    outputStartCol=1

    filelist=os.listdir(targetdir)
    sheetnum=1
    for file in filelist:
        fullpath=targetdir+file
        if fullpath==outputfile:
            continue
        if os.path.isfile(fullpath) and file[len(file)-4:]==".xls":
            print("I:Found xls file :" + file)
            sourcexls=easyExcel(fullpath)
            '''
            # count the rows and cols those have contents,silly way
            i=1
            cellstr=sourcexls.getCell(sheetnum,i,1)
            while cellstr!=None:
                print(str(i)+" row: " + cellstr)
                i=i+1
                cellstr=sourcexls.getCell(sheetnum,i,1)

            rowEnd=i-1

            i=1
            cellstr=sourcexls.getCell(sheetnum,1,i)
            while cellstr!=None:
                print("col: " + cellstr)
                i=i+1
                cellstr=sourcexls.getCell(sheetnum,1,i)
            colEnd=i-1
            '''

            # here use the UsedRange function
            rowEnd=sourcexls.usedRow(sheetnum)
            colEnd=sourcexls.usedCol(sheetnum)

            print("rowEnd: "+str(rowEnd) + " colEnd: " +str(colEnd))
            sourceRange=sourcexls.getRange(sheetnum,1,1,rowEnd,colEnd)
            outputxls.setRange(sheetnum,outputStartRow,outputStartCol,sourceRange)
            outputStartRow=outputStartRow+rowEnd
            outputStartCol=outputStartCol
            sourcexls.close()

    outputxls.save(outputfile)
    outputxls.close()
    print("Done")



'''
    filename="E:\\xulin\\test.xls"
    newfile="E:\\xulin\\output.xls"
    xls=easyExcel(filename)
    newxls=easyExcel()
    content=xls.getCell('Sheet1', 1, 1)
    rangecontent=xls.getRange('Sheet1',1,1,3,3)
    print(rangecontent)
    print(content)
    newxls.setCell('Sheet1',1,1,content)
    newxls.setRange('Sheet1',2,3,rangecontent)

    xls.close()
    newxls.save(newfile)
    newxls.close()
'''

