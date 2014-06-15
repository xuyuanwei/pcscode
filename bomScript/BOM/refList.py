#!/usr/bin/python
debug=1
logfile="./python_debug.txt"

def expandref(inputstr,divider):
    #result_list.extend("abc")=> ['a','b','c']
    f=open(logfile,'w')
    if debug==1:
        f.write("expandref() get input: "+ inputstr + "\n")
    position=inputstr.find(divider)
    if position==-1:
        return [inputstr]
    str1=inputstr[:position]
    str2=inputstr[position+1:]
    # get ref prefix in str1
    i=0
    while str1[i].isalpha():
        i=i+1
        if i>=len(str1):
            return [inputstr]
    prefix1=str1[:i]
    # get the start number of ref
    numstart=str1[i:]
    if numstart.isdigit():
        numstart=int(numstart)
    else:
        return [inputstr]
    if debug==1:
        f.write("expandref(): prefix "+ prefix1 + "\n")
        f.write("expandref(): numstart "+ str(numstart) + "\n")
    # get the end number of ref
    if str2.isdigit():
        numend=int(str2)
    elif str2[:i]==prefix1 and str2[i-1:].isdigit():
        numend=int(str2)
    else:
        return [inputstr]
    if debug==1:
        f.write("expandref(): numend "+ str(numend) + "\n")
    if numend<=numstart:
        return [inputstr]
    ref_l=[]
    for i in range(numstart,numend+1):
        ref_l.append(prefix1+str(i))
    f.close()
    return ref_l

def expandrefString(refstring,refdivider,expandseperator):
    reflist=refstring.strip(refdivider).split(refdivider)
    returnlist=[]
    for ref in reflist:
        if ref=='':
            continue
        returnlist.extend(expandref(ref,expandseperator))
    return returnlist

''' read value+refs.txt file,format like
    "
    10nF	C12 C13
    "
    and print to be like
    "
    C12	10nF
    C13	10nF
    "
    '''

inputfile="./value+refs.txt"
outputfile="./reflist.txt"
fin=open(inputfile,'r')
fout=open(outputfile,'w')

seperator='\t'
refSeperator=' '
for line in fin.readlines():
    line=line.strip('\r\n').strip('\n').strip(' ').strip('\t')
    length=len(line)
    if(length==0):
        continue
    sepPositioin=line.find(seperator)
    valueStr=line[:sepPositioin]
    refList=expandrefString(line[sepPositioin+1:],' ','-')
    print("reflist: "+str(refList))
    for ref in refList:
        fout.write(ref+seperator+valueStr+"\n")


fin.close()
fout.close()

