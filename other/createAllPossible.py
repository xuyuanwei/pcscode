#!/bin/env python

import os

'''
charactorList=['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g',
        'h','i','j','k','l','m','n',
        'o','p','q','r','s','t',
        'u','v','w','x','y','z',
        'A','B','C','D','E','F','G',
        'H','I','J','K','L','M','N',
        'O','P','Q','R','S','T',
        'U','V','W','X','Y','Z',
        '~','!','@','#','$','%','^','&','*','(',')','_','+','-','=','{','}','|','[',']','\\',':','"',';','\'','<','>','?',',','.','/']
        '''

charactorList=['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g',
        'h','i','j','k','l','m','n',
        'o','p','q','r','s','t',
        'u','v','w','x','y','z',
        'A','B','C','D','E','F','G',
        'H','I','J','K','L','M','N',
        'O','P','Q','R','S','T',
        'U','V','W','X','Y','Z' ]
charactorList_length=len(charactorList)
outputFileNameBase="./output_data"

def createAllPosible(output_File_Name_Base,level,charactor_List):
    if output_File_Name_Base==None or level<0 or charactor_List==None:
        print("parameter error")
        return -1

    currentFileName=output_File_Name_Base+str(level)+".txt"
    
    if os.path.isfile(currentFileName):
        print(currentFileName + " already exists")
        return 0

    outputFileHandler=open(currentFileName,'w+')

    if level==0:
        for c in charactor_List:
            outputFileHandler.write(c)
            outputFileHandler.write('\n')
        outputFileHandler.close()
        return 0

    headerFileName=output_File_Name_Base+str(level-1)+".txt"
    headerFileHandler=open(headerFileName,'r')
    headerString=headerFileHandler.readline().strip("\r\n").strip('\n')
    while headerString:
        #print("headerString: "+headerString)
        for c in charactor_List:
            outputFileHandler.write(headerString + c)
            outputFileHandler.write('\n')

        headerString=headerFileHandler.readline().strip("\r\n").strip('\n')

    headerFileHandler.close()
    outputFileHandler.close()
    print("level " + str(level)+" done")
    lineCount = pow(charactorList_length,level+1)
    print("length of line output: "+str(lineCount))
    return 0

if __name__=='__main__':
    level=4

    print("length of charactorList: "+str(charactorList_length))

    for i in range(0,level):
        createAllPosible(outputFileNameBase,i,charactorList)





