# -*- coding: utf-8 -*-
import uno
import sys
import os
import time
import string
import difflib

userhome=os.environ['HOME']+'/'
defaultconfigdir=".config/libreoffice/3/user/Scripts/python/"
scriptdir=userhome+defaultconfigdir
if sys.path[-1]!=scriptdir:
    print(sys.path[-1])
    sys.path.append(scriptdir) 
import OOoBasic
import commonfun

def GetOooDesktop():
    local=uno.getComponentContext()
    resolver=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
    context=resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    Desktop=context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",context)
    doc=Desktop.getCurrentComponent()
    return doc

def resisterDescriptionStandardlize(ResString):
    type_keyword=["电阻"]
    decal_keyword=["0603","0805","1206"]
    unit_keyword=['R','K','M']
    precision_keyword=["5%","1%"]
    mountType_keyword=["贴片","插件"]

    isResister=0
    inputstr=ResString.strip().upper()
    #check whether it is Resister
    for word in type_keyword:
        if inputstr.find(word)>=0:
            isResister=1
            break
    if isResister==0:
        return ""

    #check precision
    precision=""
    for word in precision_keyword:
        if inputstr.find(word)>=0:
            precision=word
            break

    #check decal
    position=-1
    decal=""
    for word in decal_keyword:
        position=inputstr.find(word)
        if position>=0:
            decal=word
            break
    #to prevent decal like "R0603",where 'R' is also a unit flag
    #if it is,then strip it from inputstr
    if position>=1 and inputstr[position-1]=='R':
        inputstr=inputstr[:position-1] + inputstr[position+4:]

    #check unit and get value
    position=-1
    valueStr=""
    for word in unit_keyword:
        position=inputstr.find(word)
        if position>=0:
            break

    #assume there would be two bype value string like "3K3" and "3.3K",
    #make "3K3" format as standard
    valueBegin=position-1
    while valueBegin>=0:
        if inputstr[valueBegin].isdigit() or inputstr[valueBegin]=='.':
            valueBegin-=1
        else:
            break

    valueEnd=position+1
    while valueEnd<len(inputstr):
        if inputstr[valueEnd].isdigit():
            valueEnd+=1
        else:
            break

    valueStr=inputstr[valueBegin+1:valueEnd]
    dotPosition=valueStr.find('.')
    #hope it fully meet the value format as 3.3K
    if dotPosition!=-1 and valueStr[-1]==inputstr[position]:
        valueStr=valueStr[0:dotPosition]+inputstr[position]+valueStr[dotPosition+1:]

    #check mounttype
    mountType=""
    for word in mountType_keyword:
        if inputstr.find(word)!=-1:
            mountType=word
            break

    return mountType+" "+"Resister " + valueStr +" "+precision+" "+decal


def CapDescriptionStandardlize(CapString):
    """
    warning: 10pF is the min value to process
    """
    type_keyword=["电解电容","钽电容","电容"]
    CapDecal_keyword=["0603","0805","1206","1210"]
    TCapDecal_keyword=['A','B','C','D']
    unit_keyword=['P','N','U','μ']
    precision_keyword=["5%","10%","20%"]
    mountType_keyword=["贴片","插件"]
    material_keyword=["NPO","X5R","X7R"]

    inputstr=CapString.strip().upper()
    #check for type
    typeStr=""
    for word in type_keyword:
        if inputstr.find(word)!=-1:
            typeStr=word
            break

    if typeStr=="":
        return ""
    #check for material,"NPO" confict with unit keyword
    position=-1
    if typeStr=="电容":
        position=inputstr.find("NPO")
        if position!=-1:
            inputstr=inputstr[:position]+inputstr[position+3:]
    #check for value
    unitStr=""
    valueStr=""
    for word in unit_keyword:
        position=inputstr.find(word)
        if position!=-1:
            unitStr=word
            break

    valueStart=position-1
    while valueStart>=0:
        if inputstr[valueStart].isdigit() or inputstr[valueStart]=='.':
            valueStart-=1
        else:
            break

    if unitStr=='μ':
        valueStr=inputstr[valueStart+1:position+2]
    else:
        valueStr=inputstr[valueStart+1:position+1]

    digitalLen=position-1-valueStart
    #if like 22P,then change to 220P as last digit is the power
    if unitStr=='P' and digitalLen==2:
        valueStr=valueStr[:2]+'0'+'P' 

    if unitStr=='P' and digitalLen==3 and valueStr[2]=='0':
        valueStr+="(Waring)"

    #change 2.2N like to be 222P
    #there are so many probability to express a cap value,like 2.2N,220N,0.47U
    #TODO:and assumed there is no 2N2 such way,it is not supported in code
    #TODO:2.2F like is not supported
    if unitStr=='N':
        valueStr=str(int(float(valueStr[:-1])*1000))
        len1=len(valueStr)
        valueTemp=valueStr.rstrip('0')
        len2=len(valueTemp)
        if len2==1:
            valueTemp=valueTemp+'0'
            len2=2
        valueStr=valueTemp+str(len1-len2)+'P'

    if unitStr=='U':
        valueStr=str(int(float(valueStr[:-1])*1000000))
        len1=len(valueStr)
        valueTemp=valueStr.rstrip('0')
        len2=len(valueTemp)
        if len2==1:
            valueTemp=valueTemp+'0'
            len2=2
        valueStr=valueTemp+str(len1-len2)+'P'

    if unitStr=='μ':
        valueStr=str(int(float(valueStr[:-2])*1000000))
        len1=len(valueStr)
        valueTemp=valueStr.rstrip('0')
        len2=len(valueTemp)
        if len2==1:
            valueTemp=valueTemp+'0'
            len2=2
        valueStr=valueTemp+str(len1-len2)+'P'

    #check for decal
    decalStr=""
    if typeStr=="电容":
        for word in CapDecal_keyword:
            if inputstr.find(word)!=-1:
                decalStr=word
                break

    if typeStr=="钽电容":
        for word in TCapDecal_keyword:
            if inputstr.find(word)!=-1:
                decalStr=word
                break

    #check for precision
    precision=""
    for word in precision_keyword:
        if inputstr.find(word)!=-1:
            precision=word
            break
    #check for voltage
    voltage=""
    position=inputstr.find('V')
    voltageStart=position-1
    while voltageStart>=0:
        if inputstr[voltageStart].isdigit():
            voltageStart-=1
        else:
            break
    voltage=inputstr[voltageStart+1:position+1]
    #check for mount type
    mountType=""
    for word in mountType_keyword:
        if inputstr.find(word)!=-1:
            mountType=word
            break

    return mountType+" "+typeStr +" "+ valueStr +" "+precision+" "+decalStr +" "+ voltage


def standardlizeDescription(materialDescription):
    if materialDescription.find("电阻")!=-1:
        return resisterDescriptionStandardlize(materialDescription)
    if materialDescription.find("电容")!=-1:
        return CapDescriptionStandardlize(materialDescription)
    return materialDescription


def standardlize():
    #sheet=GetOooDesktop().getSheets().getByName("库存")
    sheet=GetOooDesktop().getCurrentController().getActiveSheet()
    column=1
    for i in range(1,200):
        cellstr= sheet.getCellByPosition(column,i).getString().encode('utf-8')
        print("get str: " + cellstr)
        newstr=standardlizeDescription(cellstr)
        print("new str: " + newstr)
        sheet.getCellByPosition(column+1,i).setString(newstr) 

def findmatch(string,strlist):
    listLen=len(strlist)
    if string=="" or listLen==0:
        return (-1,0)
    rate=0
    maxMatchIndex=-1
    for i in range(0,listLen):
        s=difflib.SequenceMatcher(None,string,strlist[i])
        if s.ratio()>rate:
            maxMatchIndex=i
            rate=s.ratio()

    return (maxMatchIndex,rate)


def fetchPNTable():
    sheetname="库存"
    pnCol=0
    DescCol=1
    startRow=2
    endRow=200

    global pnList
    global descList
    pnList=[]
    descList=[]
    sheet=GetOooDesktop().getSheets().getByName(sheetname)
    for r in range(startRow,endRow):
        description=sheet.getCellByPosition(DescCol,r).getString().strip().upper().encode('utf-8')
        if description!="":
            descList.append(standardlizeDescription(description))
            pnList.append(sheet.getCellByPosition(pnCol,r).getString())
    return


def getMatchPn():
    descriptionCol=2
    startRow=1
    endRow=93
    pnCol=0
    sheet=GetOooDesktop().getCurrentController().getActiveSheet()

    fetchPNTable()

    global descList
    global pnList

    for r in range(startRow,endRow):
        desc=sheet.getCellByPosition(descriptionCol,r).getString().strip().upper().encode('utf-8')
        result=findmatch(standardlizeDescription(desc),descList)
        if result[0]!=-1:
            sheet.getCellByPosition(pnCol,r).setString(pnList[result[0]])
            sheet.getCellByPosition(pnCol+1,r).setValue(result[1])
        else:
            sheet.getCellByPosition(pnCol,r).setString("")
            sheet.getCellByPosition(pnCol+1,r).setValue(result[1])



g_exportedScripts=standardlize,getMatchPn

