import uno
import string
import locale

debug=1
def expandref(inputstr,divider):
	#result_list.extend("abc")=> ['a','b','c']
	if debug==1:
		f.write("expandref() get input: "+ inputstr + "\n")
	position=inputstr.find(divider)
	if position==-1:
		return inputstr
	str1=inputstr[:position]
	str2=inputstr[position+1:]
	# get ref prefix in str1
	i=0
	while str1[i].isalpha():
		i=i+1
		if i>=len(str1):
			return inputstr
	prefix1=str1[:i]
	# get the start number of ref
	numstart=str1[i:]
	if numstart.isdigit():
		numstart=int(numstart)
	else:
		return inputstr
	if debug==1:
		f.write("expandref(): prefix "+ prefix1 + "\n")
		f.write("expandref(): numstart "+ str(numstart) + "\n")
	# get the end number of ref
	if str2.isdigit():
		numend=int(str2)
	elif str2[:i]==prefix1 and str2[i-1:].isdigit():
		numend=int(str2)
	else:
		return inputstr
	if debug==1:
		f.write("expandref(): numend "+ str(numend) + "\n")
	if numend<=numstart:
		return inputstr
	ref_l=[]
	for i in range(numstart,numend+1):
		ref_l.append(prefix1+str(i))
	return ref_l

def GetOooDesktop():
	local=uno.getComponentContext()
	resolver=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
	context=resolver.resolve("uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext")
	Desktop=context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",context)
	doc=Desktop.getCurrentComponent()
	return doc

def Startprocess():
	doc=GetOooDesktop()
	#sheet=doc.getSheets().getByIndex(0)
	sheet=doc.getCurrentController().getActiveSheet()
	logfile="e:\\TEMP\\python_debug.txt"
	bom4sch="e:\\TEMP\\bom4sch.txt"
	#logfile="D:\\tmp\\PCB\\python_debug.txt"
	#bom4sch="D:\\tmp\\PCB\\reflist.txt"
	#logfile="/home/user/tmp/ooo_python_debug.txt" #in Linux,dir cann't be like "~/dir" or there will be error
	#bom4sch="/home/user/tmp/bom4sch.txt"
	global f
	f=open(logfile,'w')
	f.write("----log start----\n")
	bom_f=open(bom4sch,'w')

	# to get the columns where "item","description" and "ref" in
	flag=0
	for i in range(0,10):
		tempstr=sheet.getCellByPosition(i,0).getString()
		tempstr=tempstr.encode('utf-8').upper()
		if debug==1:
			f.write(str(i)+ " " +tempstr + "\n")
		if tempstr=="ITEM":
			itemcol=i
			flag=flag+1
		elif tempstr=="DESCRIPTION":
			desccol=i
			flag=flag+2
		elif tempstr=="REF":
			refcol=i
			flag=flag+4
		if flag==7:
			break

	if flag!=7:
		if debug==1:
			f.write("flag = " + str(flag) + " but not =7! item description ref\n")
			f.closed
		return

	targetcol=refcol+1
	row=1
	refdivider=" "
	divider="-"
	while sheet.getCellByPosition(itemcol,row).getString()!="":
		# expand the ref column
		reflist=sheet.getCellByPosition(refcol,row).getString().encode('utf-8').split(refdivider)
		description=sheet.getCellByPosition(desccol,row).getString().encode('utf-8')
		if debug==1:
			f.write("main(): list of refstring: " + str(reflist) +"\n")
		reflistnew=[]
		# for each ref in the original reflist
		for ref in reflist:
			if ref=="":
				continue
			if debug==1:
				f.write("main(): ref in reflist: " + ref +"\n")
			# check whether there is '-' in the ref string
			if not ref.find(divider)==-1:
				#reflistnew.extend(expandref(ref,divider))
				expandresult=expandref(ref,divider)
				resulttype=type(expandresult)
				if resulttype==str:
					reflistnew.append(expandresult)
				if resulttype==list:
					reflistnew.extend(expandresult)
			else:
				if debug==1:
					f.write("main(): ref: " + str(ref) +"\n")
				reflistnew.append(ref)
		# put the member in the list to string
		refstrnew=""
		if debug==1:
			f.write("main():reflistnew: " + str(reflistnew) +"\n")
		refstrnew=""
		reflistnew.sort()
		for ref in reflistnew:
			refstrnew=refstrnew + str(ref) + " "
			bom_f.write(str(ref) + "\t" + description + "\n")
		if not refstrnew=="":
			if debug==1:
				f.write("main():ref string after expand: " + refstrnew +"\n")
			sheet.getCellByPosition(targetcol,row).setString(refstrnew[:-1])
			sheet.getCellByPosition(targetcol+1,row).setString(len(reflistnew))
		row=row+1
	f.write("file closed normally")
	f.closed
	bom_f.write("file closed normally")
	bom_f.closed
