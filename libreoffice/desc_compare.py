#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uno
import string

logfile="e:\\xulin\\TEMP\\py_desc_compare.txt"
diffoutput="e:\\xulin\\TEMP\\py_desc_diff.txt"
#logfile="/home/cylinc/tmp/py_desc_compare.txt"

def GetOooDesktop():
	local=uno.getComponentContext()
	resolver=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
	context=resolver.resolve("uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext")
	Desktop=context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",context)
	doc=Desktop.getCurrentComponent()
	return doc

#res_cn="µç×è".encode('utf-8')
#smd_cn="ÌùÆ¬".encode('utf-8')
#dip_cn="²å¼þ".encode('utf-8')
#cap_cn="µçÈÝ".encode('utf-8')

res_cn=b'\xe7\x94\xb5\xe9\x98\xbb'
smd_cn=b'\xe8\xb4\xb4\xe7\x89\x87'
dip_cn=b'\xe6\x8f\x92\xe4\xbb\xb6'
cap_cn=b'\xe7\x94\xb5\xe5\xae\xb9'

ResName=["RES","RESISTOR",res_cn]
ResMountType1=["SMD","SURFACE MOUNT",smd_cn]
ResMountType2=["DIP",dip_cn]

ResDecal=["0402","0603","0805","1206","1210"]
ResPrecision=["5%","1%"]
ResValueUnit=["K","R","M"]
ResPowerDiss=["W"]

# get the digits arround the keyword
def getValue(sourcestr,keyword):
	#print("getValue(): keyword: " + keyword)
	if keyword=="" or sourcestr=="":
		return ""	
	position=sourcestr.find(keyword)
	if position==-1:
		return ""
	if position==0:
		position=sourcestr.find(keyword,1)
	while not position==-1:
		startpos=position-1
		# try to find the postion of '1' in the string "1.5pF" or "1/16W"
		while sourcestr[startpos].isdigit() or sourcestr[startpos]=="." or sourcestr[startpos]=="/" :
			startpos=startpos-1
			if startpos==-1:
				break
		# if there is no digit before the keyword, then try to find the next position of  keyword
		if startpos==position-1:
			position=sourcestr.find(keyword,position+1)
			continue

		length=len(sourcestr)
		endpos=position+len(keyword)
		# if the keyword is the last charater in the string
		if endpos==length:
			#print("getvalue(): return from pos1")
			return sourcestr[startpos+1:]

		# try to find the digits after the keyword like "1K5"
		while sourcestr[endpos].isdigit():
			endpos=endpos+1
			if endpos==length:
				break
		# debug_print
		'''
		#print("getvalue(): return from pos2")
		#print("getvalue():start: {0};end: {1}".format(startpos+1,endpos))
		#print("getvalue(): " + sourcestr[startpos+1:endpos]) 
		'''
		return sourcestr[startpos+1:endpos]
	return ""

def isResiterStr(description):
	for string in ResName:
		position=description.find(string)
		if position>-1:
			tempstr1=description[position+len(string)]
			tempstr2=description[position-1]
			#print("tempstr1: {0};tempstr2: {1}".format(tempstr1,tempstr2))
			if position==0:
				if tempstr1>="A" and tempstr1<="Z":
					continue
				else:
					return 1
			elif (tempstr1>="A" and tempstr1<="Z") or (tempstr2>="A" and tempstr2<="Z"):
				continue
			else:
				return 1
	return 0

def CreateStdResDesc(description):
	result=""
	if description=="":
		return result
	if not isResiterStr(description):
		return ""
	result=result+"Resistor"
	for mounttype in ResMountType1:
		if description.find(mounttype)>-1:
			result=result+ " SMD"
			break
	for mounttype in ResMountType2:
		if description.find(mounttype)>-1:
			result=result+ " DIP"
			break
	for decal in ResDecal:
		if description.find(decal)>-1:
			result=result+ " " + decal
			break
	for powerdiss in ResPowerDiss:
		value=getValue(description,powerdiss)
		if value==None:
			#print("[W]aring: Error in getValue()")
			continue
		if not value=="":
			result=result+ " " + value
			break
	for unit in ResValueUnit:
		value=getValue(description,unit)
		if value==None:
			#print("[W]aring: Error in getValue()")
			continue
		if not value=="":
			#print("value: " +str(type(value)))
			result=result+ " " + value
			break
	for precision in ResPrecision:
		if description.find(precision)>-1:
			result=result+ " " + precision
			break
	return result

CapName=["CAP","CAPACITOR",cap_cn]
CapMountType1=["SMD","SURFACE MOUNT",smd_cn]
CapMountType2=["DIP",dip_cn]
CapDecal=["0402","0603","0805","1206","1210"]
CapPrecision=["20%","10%","5%","+20/-80%"]
CapValueUnit=["PF","NF","UF","P","N","U"]
CapVoltage=["V"]
CapMeterial=["NPO","X7R","X5R","Y5V"]

def isCapacitor(description):
	for string in CapName:
		if description.find(string)>-1:
			return 1
	return 0

def CreateStdCapDesc(description):
	result=""
	if description=="":
		return result
	if not isCapacitor(description):
		return ""
	result=result+"Capacitor"
	for mounttype in CapMountType1:
		if description.find(mounttype)>-1:
			result=result+ " SMD"
			break
	for mounttype in CapMountType2:
		if description.find(mounttype)>-1:
			result=result+ " DIP"
			break
	for decal in CapDecal:
		if description.find(decal)>-1:
			result=result+ " " + decal
			break
	for unit in CapValueUnit:
		value=getValue(description,unit)
		if value==None:
			#print("[W]aring: Error in getValue()")
			continue
		if not value=="":
			result=result+ " " + value
			break
	for voltage in CapVoltage:
		value=getValue(description,voltage)
		if not value=="":
			result=result+ " " + value
			break
	for precision in CapPrecision:
		if description.find(precision)>-1:
			result=result+ " " + precision
			break
	for material in CapMeterial:
		if description.find(material)>-1:
			result=result+ " " + material
			break
	#print("Capstd: result: "+result)
	return result

def isstrEqual(str1,str2):
	divider=" "
	if str1==str2:
		return 1
	if str1=="" or str2=="":
		return -1
	list1=str1.split(divider)
	list2=str2.split(divider)
	newlist1=[]
	for member in list1:
		if not member=='':
			newlist1.append(member)
	newlist2=[]
	for member in list2:
		if not member=='':
			newlist2.append(member)
	newlist1.sort()
	newlist2.sort()
	#print("newlist1: "+str(newlist1)+"\n")
	#print("newlist2: "+str(newlist2)+"\n")
	f.write("newlist1: "+str(newlist1)+"\n")
	f.write("newlist2: "+str(newlist2)+"\n")
	if newlist1==newlist2:
		return 1
	else:
		fdiff.write("\n")
		fdiff.write("newlist1: "+str(newlist1)+"\n")
		fdiff.write("newlist2: "+str(newlist2)+"\n")
		return 0


f=open(logfile,'w')
fdiff=open(diffoutput,'w')

def Startprocess():
	'''
	usage:
		the target of this function is to compare the two kinds of descriptions of one PN material, if in case of:
			1) resister: unify the descriptions to be stand description
	2) capitance:unify the descriptions to be stand description
	3) others: trim the two description strings,then to compare

	1. set the sheet name to be "sheet1",you are encouraged to create a new file to do this
	2. the first row of data is 1
	3. the 1st col should be pn, the 2nd col should be description1,
	   the 3rd should be description2
	4. current,the last row is set to be 600
	'''

	doc=GetOooDesktop()
	sheet=doc.getSheets().getByName("sheet1")
	#inputstr1="Resistor 0402 Surface Mount 1% 2R0 1/16W "
	#inputstr2="SMD¡¡CAP	Capacitor SM 0402 NPO Ceramic 5% 50V 10P"
	#inputstr2=inputstr2.upper()
	#print(inputstr2)
	#print(CreateStdCapDesc(inputstr2))
	startrow=0
	endrow=600
	item_col=0
	desc_col1=1
	desc_col2=2
	outputcol=3
	'''
	ResName[2]=ResName[2].encode('utf-8')
	ResMountType1[2]=ResMountType1[2].encode('utf-8')
	ResMountType2[1]=ResMountType2[1].encode('utf-8')
	CapName[2]=CapName[2].encode('utf-8')
	CapMountType1[2]=CapMountType1[2].encode('utf-8')
	CapMountType2[1]=CapMountType2[1].encode('utf-8')
	'''

	for i in range(startrow,endrow):
		str1=sheet.getCellByPosition(desc_col1,i).getString()
		str1=str1.encode('utf-8')
		str1=str1.upper()
		f.write("str1: "+str1+"\n")

		str2=sheet.getCellByPosition(desc_col2,i).getString()
		str2=str2.encode('utf-8')
		str2=str2.upper()
		f.write("str2: "+str2+"\n")

		if isResiterStr(str1) and isResiterStr(str2):
			result1=CreateStdResDesc(str1)
			result2=CreateStdResDesc(str2)
			f.write("result1: "+result1+"\n")
			f.write("result2: "+result2+"\n")
			if result1==result2:
				sheet.getCellByPosition(outputcol,i).setString("same")
			else:
				sheet.getCellByPosition(outputcol,i).setString("different")
				fdiff.write("\n")
				fdiff.write(sheet.getCellByPosition(item_col,i).getString())
				fdiff.write("\n")
				fdiff.write("result1: "+result1+"\n")
				fdiff.write("result2: "+result2+"\n")
			continue
		if isCapacitor(str1) and isCapacitor(str2):
			result1=CreateStdCapDesc(str1)
			result2=CreateStdCapDesc(str2)
			f.write("result1: "+result1+"\n")
			f.write("result2: "+result2+"\n")
			if result1==result2:
				sheet.getCellByPosition(outputcol,i).setString("same")
			else:
				sheet.getCellByPosition(outputcol,i).setString("different")
				fdiff.write("\n")
				fdiff.write(sheet.getCellByPosition(item_col,i).getString())
				fdiff.write("\n")
				fdiff.write("result1: "+result1+"\n")
				fdiff.write("result2: "+result2+"\n")
			continue
		if isstrEqual(str1,str2)==1:
			sheet.getCellByPosition(outputcol,i).setString("same")
		else:
			sheet.getCellByPosition(outputcol,i).setString("different")
			fdiff.write(sheet.getCellByPosition(item_col,i).getString())
			'''
			fdiff.write("\n")
			fdiff.write("str1: "+str1+"\n")
			fdiff.write("str2: "+str2+"\n")
			'''
	f.closed
	fdiff.closed

def Test():
	inputstr1="SMD IC    MCU STM8S103  TSSOP20    ".encode('utf-8')
	inputstr2="SMD IC MCU STM8S103 TSSOP20".encode('utf-8')
	inputstr1=inputstr1.upper()
	inputstr2=inputstr2.upper()
#   print(inputstr1)
	#print(CreateStdResDesc(inputstr1))
	#print(isstrEqual(inputstr1,inputstr2))

Test()
