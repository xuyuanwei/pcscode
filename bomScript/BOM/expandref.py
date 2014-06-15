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

if __name__=="__main__":
    logfile="d:\\tmp\\python_debug.txt"
    sourcefile=".\\refs.txt"
    output=".\\expandref.txt"

    global f
    f=open(logfile,'w')
    f.write("----log start----\n")

    fsource=open(sourcefile,'r')
    fout=open(output,'w')

    # to get the columns where "item","description" and "ref" in
    refdivider=" "
    divider="-"

    for line in fsource.readlines():
        line=line.rstrip("\r\n").rstrip('\n').strip(' ')
        refList=line.split(' ')
        expandRefList=[]
        for ref in refList:
            if ref=='':
                continue
            if ref.find(divider)!=-1:
                expandresult=expandref(ref,divider)
                resulttype=type(expandresult)
                if resulttype==str:
                    expandRefList.append(expandresult)
                if resulttype==list:
                    expandRefList.extend(expandresult)
            else:
                expandRefList.append(ref)

        refstring=str(expandRefList).replace('\'','').replace(' ','')
        fout.write(refstring[1:-1]+"\t"+str(len(expandRefList))+'\n')


    f.write("file closed normally")
    f.close()
    fout.close()
