#**********************************************************************
#    this script is used to delete the material code in the unwanted warehouse
#**********************************************************************
#    Copyright (C) 2011 xuyuanwei@gmail.com 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#**********************************************************************
import uno
import sys
import os
import time
from com.sun.star.sheet.CellInsertMode import DOWN
from com.sun.star.sheet.CellInsertMode import ROWS
from com.sun.star.sheet.FillDirection import TO_BOTTOM
from com.sun.star.sheet.FillMode import SIMPLE
from com.sun.star.sheet.CellDeleteMode import UP
from com.sun.star.sheet.CellDeleteMode import ROWS
from com.sun.star.sheet.CellFlags import FORMULA
import string

#add the diretory of this script to the PYTHONPATH,in order to import OOoBasic
#It seems there is no such problem in Windows
#sys.path.append(os.getcwd()) #getcwd() is the cwd of start of libreoffice
#scriptdir=os.path.dirname(sys.argv[0])
#scriptdir=os.path.realpath(__file__)
print(sys.path)
userhome=os.environ['HOME']+'/'
defaultconfigdir=".libreoffice/3/user/Scripts/python/"
scriptdir=userhome+defaultconfigdir
if sys.path[-1]!=scriptdir:
    print(sys.path[-1])
    sys.path.append(scriptdir) 
import OOoBasic
import commonfun

def kc_process():
    sheet1=OOoBasic.GetOooDesktop().getSheets().getByIndex(0)
    configfile=scriptdir+"config"
    varNlist=["wantedlist","warehousecol","startrow","unwantedlist"]
    section="warehouse"
    result=commonfun.readvarible(configfile,section)
    try:
        wantedlist=result['wantedlist'].split(',')
        usewanted=1
    except KeyError:
        try:
            unwantedlist=result['unwantedlist'].split(',')
            usewanted=0
        except KeyError:
            print("no list get")
            return -1

    try:
        startrow=int(result['startrow'])-1
        keywordcolumn=ord(result['warehousecol'].upper())-ord('A')
    except KeyError:
        print("startrow/keywordcolumn not get")
        return -1

    '''
    unwantedlist=["WHDI","WXC1"]
    wantedlist=["ZC","GZC","BCPC","CPC"]
    keywordcolumn=2
    startrow=1
    '''
    i=startrow
    value=sheet1.getCellByPosition(keywordcolumn,i).getString()
    #print("Debug: Value: " + value)
    #first to count how many rows in the sheet
    while value != "":
        i=i+1
        value=sheet1.getCellByPosition(keywordcolumn,i).getString()
        #print("Value: " + value)
    #print("there are total " + str(i) + " lines")
    count=i-1
    matchresult=0
    matchcount=0
    while count>=startrow:
        matchresult=0
        value=sheet1.getCellByPosition(keywordcolumn,count).getString()
        #either unwantedlist or wantedlist will take effect,but won't at the same time
        #if both list existing,unwantedlist will be used
        if usewanted==0:
            for unwantedkey in unwantedlist:
                if value == unwantedkey:
                    matchresult=1
                    matchcount=matchcount+1
                    break
        if usewanted==1:
            matchresult=1
            for wantedkey in wantedlist:
                if value == wantedkey:
                    matchresult=0
                    break
            if matchresult==1:
                matchcount=matchcount+1
        if matchresult== 0 and matchcount>0:
            OOoBasic.deleterows(sheet1,count+1,matchcount)
            matchcount=0
        if matchresult== 1 and count==startrow:
            OOoBasic.deleterows(sheet1,count,matchcount)
            matchcount=0
        count=count-1
    return 0

g_exportedScripts =kc_process,
