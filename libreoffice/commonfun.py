# -*- coding: utf-8 -*-
import os
import fileinput
def readvarible(configfilename,sectionname):
    '''
    this function is used to read the cofig file
    configfilename: the full path of the config file
    sectionname: which secton data to read
        the content should be like:
        #Comment content
        [sectionname]
        variable1=content1
        variable2=content2
    '''

    #check if config file exists
    if not os.path.isfile(configfilename):
        print("Debug: readvarible() file is not found")
        return {}

    commentChar='#'
    sectionfoundflag=0
    #return dictrionary type
    dic={}
    for line in fileinput.input(configfilename):
        line=line.strip()
        if len(line)>=1 and line[0]==commentChar:
            continue
        print("Debug: readvarible() line: " + line)
        if sectionfoundflag==0 and line.find('['+sectionname+']')==-1:
            continue
        else:
            if line.find('['+sectionname+']')>=0:
                sectionfoundflag=1
                print("Debug: readvarible() find flag:" +sectionname)
                continue
        if sectionfoundflag==1 and line.find('[')!=-1 and line.find(']')!=-1:
            print("Debug: readvarible() reach next section")
            break
        if line.find('=')==-1:
            continue
        templine=line.strip()
        var=templine.split('=')
        print("Debug: readvarible() get: " + str(var))
        if var[0]=='' or var[1]=='':
            continue
        dic[var[0].strip()]=var[1].strip()
    fileinput.close()
    return dic


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

    valueEnd=position+1
    while valueEnd<len(inputstr):
        if inputstr[valueEnd].isdigit():
            valueEnd+=1

    valueStr=inpustr[valueBegin+1:valueEnd]
    dotPosition=valueStr.find('.')
    #hope it fully meet the value format as 3.3K
    if dotPosition!=-1 and valueStr[-1]==inputstr[position]:
        valueStr=valueStr[0:dotPosition]+inputstr[position]+valueStr[dotPosition+1:]

    #check mounttype
    mountType=""
    for word in mountType_keyword:
        if inpustr.find(word):
            mountType=word

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
        if inputstr.find(word):
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

    valueStart=position-1
    while valueStart>=0:
        if inputstr[valueStart].isdigit():
            valueStart-=1

    valueStr=inpustr[valueStart+1:position+1]
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
    dotPosition=valueStr.find('.')
    if dotPosition!=-1:
        if unitStr=='N':
            valueStr=str(float(valueStr[:-1])*1000)
            len1=len(valueStr)
            valueTemp=valueStr.rstrip('0')
            len2=len(valueTemp)
            valueStr=valueTemp+str(len1-len2)+'P'

        if unitStr=='U':
            valueStr=str(float(valueStr[:-1])*1000000)
            len1=len(valueStr)
            valueTemp=valueStr.rstrip('0')
            len2=len(valueTemp)
            valueStr=valueTemp+str(len1-len2)+'P'

        if unitStr=='μ':
            valueStr=str(float(valueStr[:-2])*1000000)
            len1=len(valueStr)
            valueTemp=valueStr.rstrip('0')
            len2=len(valueTemp)
            valueStr=valueTemp+str(len1-len2)+'P'

    #check for decal
    decalStr=""
    if typeStr=="电容":
        for word in CapDecal_keyword:
            if inputstr.find(word):
                decalStr=word
                break

    if typeStr=="钽电容":
        for word in TCapDecal_keyword:
            if inputstr.find(word):
                decalStr=word
                break

    #check for precision
    precision=""
    for word in precision_keyword:
        if inputstr.find(word):
            precision=word
            break
    #check for voltage
    voltage=""
    position=inputstr.find('V')
    voltageStart=position-1
    while voltageStart>=0:
        if inputstr[voltageStart].isdigit():
            voltageStart-=1
    voltage=inputstr[voltageStart+1:position+1]

    return mountType+" "+typeStr +" "+ valueStr +" "+precision+" "+decal +" "+ voltage


def standardlizeDescription(materialDescription):
    if materialDescription.find("电阻"):
        return resisterDescriptionStandardlize(materialDescription)
    if materialDescription.find("电容"):
        return CapDescriptionStandardlize(materialDescription)
    return materialDescription


