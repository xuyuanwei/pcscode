#!/usr/bin/env python
# -*- coding: utf-8 -*-
from win32com.client import Dispatch
import win32com.client
import os
import re
#import bomfun


def doTaskRefperLine(excelbook):
    sheetcount=excelbook.Worksheets.Count
    bomsheet=excelbook.Worksheets(1)
    pnCol=2
    mNameCol=8
    mDescriptionCol=9
    RefCol=7
    titleRow=1

    pn=bomsheet.Cells(titleRow,pnCol).Value
    name=bomsheet.Cells(titleRow,mNameCol).Value
    description=bomsheet.Cells(titleRow,mDescriptionCol).Value
    ref=bomsheet.Cells(titleRow,RefCol).Value
    
    #if pn!="物料编码".encode('utf-8').decode('utf-8') or name!="物料名称".encode('utf-8').decode('utf-8') or description!="规格型号".encode('utf-8').decode('utf-8') or ref!="代号".encode('utf-8').decode('utf-8'):
    #if pn.decode('cp936')!="物料编码" or name.decode('cp936')!="物料名称" or description.decode('cp936')!="规格型号" or ref.decode('cp936')!="代号":
    #if str(pn)!="pn" or str(name)!="mname" or str(description)!="mdescription" or str(ref)!="ref":
    #    print("bom file format error")
    #    return -1

    outputdir="e:\\xulin\\tmp\\bom\\"
    txtfilepath=outputdir+excelbook.Name+"_"+bomsheet.Name+".txt"
    txtfile=open(txtfilepath,'w')

    row=2
    pn=bomsheet.Cells(row,pnCol).Value
    name=bomsheet.Cells(row,mNameCol).Value
    description=bomsheet.Cells(row,mDescriptionCol).Value
    ref=bomsheet.Cells(row,RefCol).Value

    while pn!="" and pn!=None:
        print("get pn: "+pn)
        reflist=expandRefStr(ref,',','-')
        for i in reflist:
            txtfile.write(i+"|"+pn+"|"+name+"|"+description+"\n")
        row=row+1
        pn=bomsheet.Cells(row,pnCol).Value
        name=bomsheet.Cells(row,mNameCol).Value
        description=bomsheet.Cells(row,mDescriptionCol).Value
        ref=bomsheet.Cells(row,RefCol).Value
        #print(type(pn))
    txtfile.close()


def expandRefStr(refstr,divider,link):
    #print("enter expand ref str")
    resultlist=[]
    if refstr=="":
        print("refstr is empty")
        return resultlist 
    reflist=refstr.split(divider)
    for ref in reflist:
        tmplist=expandCombinedRefStr(ref,link)
        resultlist.extend(tmplist)
    return resultlist


def expandCombinedRefStr(inputstr,link):
    #print("enter Combined ref expand")
    templist=[]
    #TODO:every time, function is called,debugfile will be opened and closed
    debug=0
    #result_list.extend("abc")=> ['a','b','c']
    position=inputstr.find(link)
    if position==-1:
        templist.append(inputstr)
        return templist
    str1=inputstr[:position]
    str2=inputstr[position+1:]
    print("str1:" + str1 +"\tstr2:" + str2)
    # get ref prefix in str1
    i=0
    while str1[i].isalpha():
        i=i+1
        if i>=len(str1):
            templist.append(inputstr)
            return templist
    prefix1=str1[:i]
    print("get prefix: " + prefix1)
    # get the start number of ref
    numstart=str1[i:]
    if numstart.isdigit():
        numstart=int(numstart)
        print("numstart: "+ str(numstart))
    else:
        templist.append(inputstr)
        return templist
    # get the end number of ref
    print("str2[:i]:" + str2[:i])
    print("i: " + str(i))
    if str2.isdigit():
        numend=int(str2)
        print("numend: "+ numend)
    elif str2[:i]==prefix1 and str2[i:].isdigit():
        numend=str2[i:]
        print("numend: "+ numend)
        #TODO: why here will error
        #numend=int(numend)
    else:
        templist.append(inputstr)
        return templist

    numend=int(numend)
    if numend<=numstart:
        templist.append(inputstr)
        return templist
    print("expandCombinedRefStr: find ref with link" + inputstr)
    ref_l=[]
    for i in range(numstart,numend+1):
        newref=prefix1+str(i)
        if len(newref)<len(str1):
            tempstr=str(i)
            for j in range(0,len(str1)-len(newref)):
                tempstr='0'+tempstr
            newref=prefix1+tempstr
        ref_l.append(newref)
    return ref_l


if __name__ == "__main__":
    ROWMAX=500
    COLMAX=255
    targetdir="e:\\xulin\\tmp\\bom\\"
    outputdir="e:\\xulin\\tmp\\bom\\"


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
            doTaskRefperLine(xlsBook_r)
            xlsBook_r.Close()

