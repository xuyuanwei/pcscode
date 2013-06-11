# -*- coding: utf-8 -*-
#**********************************************************************
#    Copyright (C) 2011 249134091@qq.com 
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
#**********************************************************************
import uno
import string
import locale
import re
import os
from operator import itemgetter, attrgetter
from datetime import date
from com.sun.star.container import NoSuchElementException
import subprocess
import sys
userhome=os.environ['HOME']+'/'
defaultconfigdir=".libreoffice/3/user/Scripts/python/"
scriptdir=userhome+defaultconfigdir
if sys.path[-1]!=scriptdir:
    print(sys.path[-1])
    sys.path.append(scriptdir) 
import OOoBasic
import commonfun


def GetOooDesktop():
    local=uno.getComponentContext()
    resolver=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
    context=resolver.resolve("uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext")
    Desktop=context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",context)
    doc=Desktop.getCurrentComponent()
    return doc

def layercount(layerno):
    return len(layerno)-len(re.sub('\.','',layerno))

def printerpbom(allitemlist,bomfile):
    bomfile.write("depth\t" + "layername\t" + "pn\t" + "quantity" + "\t" + "refs\t" + "remark" + "\n")
    for items in allitemlist:
        #        bomfile.write(str(items['depth']) + "\t" + items['layername'] + "\t" + items['pn'] + "\t" + items['des'] + "\t" + str(items['quantity']) + "\t" + str(items['reflist']) + "\t" + items['remark'] + "\n")
        bomfile.write(str(items['depth']) + "\t" + items['layername'] + "\t" + items['pn'] + "\t" + str(items['quantity']) + "\t" + str(items['reflist']) + "\t" + items['remark'] + "\n")
    return 0

def geterpbomlist():
    doc=GetOooDesktop()
    try:
        sheet_erp=doc.getSheets().getByName("erp")
    except NoSuchElementException:
        f.write("Error: sheet \"erp\" not found")
        return -1
    #start process the erp bom,just fetch each component
    maxline=1000
    layer_name=["whole"]
    startrow=1
    layer_col=0
    pn_col=1
    des_col=3
    quantity_col=5
    ref_col=7
    remark_col=8

    refdivider=" "
    erp_ele_all=[]

    layerno=sheet_erp.getCellByPosition(layer_col,startrow).getString().encode('utf-8')
    pn=sheet_erp.getCellByPosition(pn_col,startrow).getString().encode('utf-8')
    depth=layercount(layerno)
    pre_layerno=layerno
    pre_pn=pn
    pre_depth=depth
    nextrow=startrow
    while layerno!="":
        des=sheet_erp.getCellByPosition(des_col,nextrow).getString().encode('utf-8')
        quantity=sheet_erp.getCellByPosition(quantity_col,nextrow).getString().encode('utf-8').rstrip('0').rstrip('.')
        reflist=sheet_erp.getCellByPosition(ref_col,nextrow).getString().encode('utf-8').split(refdivider)
        #reflist.sort()
        refcount=len(reflist)
        if refcount==0:
            refcount=1
        remark=sheet_erp.getCellByPosition(remark_col,nextrow).getString().encode('utf-8')

        depth=layercount(layerno)
        if depth==0:
            f.write("Error: depth = 0\n")
            break
        if depth>pre_depth:
            layer_name.append(pre_pn)
            f.write("Info: find layer\t" + pre_pn + "\n")

        if depth<pre_depth:
            layer_name.pop(depth)
        ele_dict={'depth':depth,
                'layername':layer_name[depth-1],
                'pn':pn,
                'des':des,
                'quantity':quantity,
                'reflist':reflist,
                'remark':remark}
        erp_ele_all.append(ele_dict)
        #f.write("geterpbom debug" + str(ele_dict['depth'])+"\t"+ele_dict['layername']+"\t"+ele_dict['pn']+"\t"+str(ele_dict['reflist'])+ "\t" + ele_dict['remark'] + "\n")
        pre_pn=pn
        pre_layerno=layerno
        pre_depth=depth

        nextrow=nextrow+1
        layerno=sheet_erp.getCellByPosition(layer_col,nextrow).getString().encode('utf-8')
        pn=sheet_erp.getCellByPosition(pn_col,nextrow).getString().encode('utf-8')
    #erp_ele_all=sorted(erp_ele_all,key=itemgetter('layername', 'pn'))
    erp_ele_all=sorted(erp_ele_all,key=itemgetter('depth','layername', 'pn'))
    return erp_ele_all

def getorigbomlist():
    doc=GetOooDesktop()
    global f
    try:
        sheet_orig=doc.getSheets().getByName("orig")
    except NoSuchElementException:
        f.write("Error: failed to get the sheet named \"orig\"")
        #f.write("错误:没有找到名为\"orig\"的表格")
        return -1 

    startrow=6
    item_col=0
    pn_col=1
    des_col=3
    quantity_col=4
    ref_col=5
    remark_col=6

    layer_name=""
    orig_ele_all=[]
    nextrow=startrow
    item=sheet_orig.getCellByPosition(item_col,nextrow).getString().encode('utf-8').strip()
    f.write("firt item: " + str(item) + "\n")
    while item!="":
        pn=sheet_orig.getCellByPosition(pn_col,nextrow).getString().encode('utf-8').strip()
        des=sheet_orig.getCellByPosition(des_col,nextrow).getString().encode('utf-8')
        quantity=sheet_orig.getCellByPosition(quantity_col,nextrow).getString().encode('utf-8')
        reflist=sheet_orig.getCellByPosition(ref_col,nextrow).getString().encode('utf-8').strip().split(" ")
        remark=sheet_orig.getCellByPosition(remark_col,nextrow).getString().encode('utf-8').strip()
        templist=[]
        if len(reflist)>1:
            for e in reflist:
                if e != '':
                    templist.append(e)
            reflist=templist
        if item[:3].upper()=="LAY":
            depth=item[3:]
            layer_name=pn
            # in the erp bom,the name of layer1 is not availabe,
            # using "whole" instead
            #if depth=="1":
            #    layer_name="whole"
            f.write("find layer: " + layer_name + "depth: " + depth + "\n")
            nextrow=nextrow+1
            item=sheet_orig.getCellByPosition(item_col,nextrow).getString().encode('utf-8').strip()
            continue    #ignore the layer item
        refcount=len(reflist)
        if refcount==0:
            refcount=1
        f.write(str(item) + "\t" + pn + "\t" + des + "\t" + str(reflist) + str(quantity) + ":" + str(refcount) + "\n")

        if refcount==1 and reflist[0]=='':
            refcount=0
        if refcount!=0 and str(refcount) != quantity:
            quantity=str(quantity) + ":" + str(refcount)
        if quantity=='':
            quantity="Warning"

        if layer_name=="":
            f.write("Error: getorigbomlist(): layer not found when reach pn: " + pn + "\n")
            f.write("pre-cell value: " + sheet_orig.getCellByPosition(item_col,nextrow-1).getString().encode('utf-8').strip() + "\n")
            break
        ele_dict={'depth':depth,
                'layername':layer_name,
                'pn':pn,
                'des':des,
                'quantity':quantity,
                'reflist':reflist,
                'remark':remark}
        #        f.write(str(ele_dict['depth'])+"\t"+ele_dict['layername']+"\t"+ele_dict['pn']+"\t"+str(ele_dict['reflist'])+ ele_dict['remark'] + "\n")
        orig_ele_all.append(ele_dict)
        nextrow=nextrow+1
        item=sheet_orig.getCellByPosition(item_col,nextrow).getString().encode('utf-8').strip()
    #orig_ele_all=sorted(orig_ele_all,key=itemgetter('layername', 'pn'))
    orig_ele_all=sorted(orig_ele_all,key=itemgetter('depth','layername', 'pn'))
    return orig_ele_all


def createerpbom(origbomlist):
    global f
    doc=GetOooDesktop()
    try:
        doc.Sheets.removeByName("bom")
        doc.Sheets.insertNewByName("bom",1)
    except NoSuchElementException:
        doc.Sheets.insertNewByName("bom",1)
    sheet_bom=doc.getSheets().getByName("bom")
    layer_col=0
    layer_des_col=1
    item_col=11
    pn_col=12
    pn_des_col=13
    quantity_col=14
    quantity2_col=15
    warehouse_col=17
    remark_col=18
    ref_col=20
    startrow=0
    nextrow=startrow
    itemcount=0
    pre_layer_name=""   #depth in dictionary is String type
    vlookup_area="'file:///D:/ERP/KC.xls'#$Sheet1.$A$1:$C$1048576"

    headrow=0
    head=unicode("物料清单编号 说明 部门名称 版本号 主备注 BOM类型 锁定 审批 自定义项1 自定义项2 自定义项3 项目编号 组件物料号 说明 分子 分母 损耗率% 仓库帐号 备注 物料属性 位号 生效日期 失效日期 组件自定义1 组件自定义2 组件自定义3 替代原则 替代物料编码1 替代用量1 替代序号1 位号1 备注1 替代物料编码2 替代用量2 替代序号2 位号2 备注2 替代物料编码3 替代用量3 替代序号3 位号3 备注3","utf-8").encode("cp936")
    headlist=head.split(" ")
    i=0
    for title in headlist:
        sheet_bom.getCellByPosition(i,headrow).setString(title)
        i=i+1
    starttime=date.today()
    endtime=date(starttime.year+10,starttime.month,starttime.day)
    starttimecol=21
    endtimecol=22
    for element in origbomlist:
        if element['layername']!=pre_layer_name:
            f.write("createerpbom: new layer meet\n")
            itemcount=0
            nextrow=nextrow+1
        finddes_formula='=VLOOKUP(A' + str(nextrow+1) + ',' + vlookup_area +',2,0)'
        finddes_formula1='=VLOOKUP(M' + str(nextrow+1) + ',' + vlookup_area + ',2,0)'
        findck_formula='=VLOOKUP(M' + str(nextrow+1) + ','+ vlookup_area +',3,0)'
        #sheet_bom.getCellByPosition(0, 2).CharFontName = "Arial"
        sheet_bom.getCellByPosition(layer_col,nextrow).setString(element['layername'])
        sheet_bom.getCellByPosition(layer_des_col,nextrow).setFormula(finddes_formula)
        sheet_bom.getCellByPosition(2,nextrow).setString(unicode("开发部","utf-8").encode("cp936"))
        sheet_bom.getCellByPosition(3,nextrow).setString("V1.0")
        sheet_bom.getCellByPosition(5,nextrow).setString(unicode("o-外协BOM","utf-8").encode("cp936"))
        sheet_bom.getCellByPosition(6,nextrow).setString("N")
        sheet_bom.getCellByPosition(7,nextrow).setString("N")
        itemcount=itemcount+10
        sheet_bom.getCellByPosition(item_col,nextrow).setValue(itemcount)
        sheet_bom.getCellByPosition(pn_col,nextrow).setString(element['pn'])
        sheet_bom.getCellByPosition(pn_des_col,nextrow).setFormula(finddes_formula1)
        position=element['quantity'].find('/')
        if position==-1:
            sheet_bom.getCellByPosition(quantity_col,nextrow).setString(element['quantity'])
            sheet_bom.getCellByPosition(quantity2_col,nextrow).setValue(1)
        else:
            sheet_bom.getCellByPosition(quantity_col,nextrow).setString(element['quantity'][:position])
            sheet_bom.getCellByPosition(quantity2_col,nextrow).setValue(element['quantity'][position+1:])

        sheet_bom.getCellByPosition(16,nextrow).setValue(0)
        sheet_bom.getCellByPosition(warehouse_col,nextrow).setFormula(findck_formula)
        sheet_bom.getCellByPosition(remark_col,nextrow).setString(unicode(element['remark'],'utf-8').encode('cp936'))
        sheet_bom.getCellByPosition(19,nextrow).setString(unicode("M-自备物料","utf-8").encode("cp936"))
        refstr=str(element['reflist'])
        refstr=refstr.replace(", "," ")
        refstr=refstr.replace("'","")
        refstr=refstr.replace("[","")
        refstr=refstr.replace("]","")
        sheet_bom.getCellByPosition(ref_col,nextrow).setString(refstr)
        sheet_bom.getCellByPosition(starttimecol,nextrow).setString(starttime.isoformat())
        sheet_bom.getCellByPosition(endtimecol,nextrow).setString(endtime.isoformat())
        pre_layer_name=element['layername']
        nextrow=nextrow+1


def Startprocess():
    global linux
    linux=1
    global diff_file
    global rootdir
    if linux:
        rootdir="/home/cylinc/tmp/"
        logfile=rootdir + "erpbomcheck_log.txt" #in Linux,dir cann't be like "~/dir" or there will be error
        erpbomoutput=rootdir + "erpbom.txt"
        origbomoutput=rootdir + "origbom.txt"
        diff_file=rootdir + "diff.txt"
        cmd='gedit'
    else:
        rootdir="D:\\ERP\\"
        logfile=rootdir + "python_debug.txt"
        erpbomoutput=rootdir + "erpbom.txt"
        origbomoutput=rootdir + "origbom.txt"
        diff_file=rootdir + "diff.txt"
        cmd='notepad'
    global f
    global erp_bom_f
    global orig_bom_f
    f=open(logfile,'w')
    f.write("----log start----\n")

    origbom_item_list=getorigbomlist()
    if origbom_item_list==-1:
        f.close()
        subprocess.Popen([cmd,logfile])
        return -1

    orig_bom_f=open(origbomoutput,'w')
    printerpbom(origbom_item_list,orig_bom_f)
    orig_bom_f.write("file is normally closed")
    orig_bom_f.closed

    createerpbom(origbom_item_list)

    f.write("file is normally closed")
    f.closed



def test():
    configfile="/home/cylinc/Codes/python/erpbomabout/trunk/config"
    varNlist=["dbfiledir","headtitle","erpbomsheetname","layer_col","layer_des_col","item_col","pn_col","pn_des_col","quantity_col","quantity2_col","warehouse_col","remark_col","ref_col","startrow"]
    section="createerpbom"
    result=commonfun.readvarible(configfile,section,varNlist)
    len1=len(varNlist)
    len2=len(result)
    print("len1: %s\t len2: %s"%(str(len1),str(len2)))
    if len1!=len2:
        print("length error")
    else:
        for i in range(len1):
            print("%s\t%s\n"%(varNlist[i],result[i]))
    '''
    doc=GetOooDesktop()
    sheets=doc.Sheets
    count=sheets.Count
    print("There are " + str(count) + " sheet(s)")
    try:
        sheets.removeByName("bom")
        sheets.insertNewByName("bom",1)
    except NoSuchElementException:
        sheets.insertNewByName("bom",1)
    sheet_bom=doc.getSheets().getByName("bom")
    try:
        sheet_bom=doc.getSheets().getByName("bom")
    except NoSuchElementException:
        sheets.insertNewByName("bom",1)
        sheet_bom=doc.getSheets().getByName("bom")
        '''

def generateerpbom():
    doc=OOoBasic.GetOooDesktop()
    sheet_orig=doc.getSheets().getByName("orig")
    try:
        doc.Sheets.removeByName("bom")
        doc.Sheets.insertNewByName("bom",1)
    except NoSuchElementException:
        doc.Sheets.insertNewByName("bom",1)
    sheet_bom=doc.getSheets().getByName("bom")

    configfile=scriptdir+"config"
    section="createerpbom"
    configdic=commonfun.readvarible(configfile,section)
    sheet2rowcount=0
    headlist=configdic['headtitle'].split(' ')
    colcount=0
    for tittle in headlist:
        sheet_bom.getCellByPosition(colcount,0).setString(tittle)
        colcount=colcount+1

    origstartrow=int(configdic['startrow'])-1
    origitemcol=ord(configdic['item_col'].upper())-ord('A')
    origPNCol=ord(configdic['pn_col'].upper())-ord('A')
    origDesCol=ord(configdic['des_col'].upper())-ord('A')
    origQuantityCol=ord(configdic['quantity_col'].upper())-ord('A')
    origRefCol=ord(configdic['ref_col'].upper())-ord('A')
    origRemarkCol=ord(configdic['remark_col'].upper())-ord('A')
    asmprefix=configdic['assemblyprefix']
    asmpnflag=0
    asmpn=''
    asmPNDes=''
    preAsmPn=''
    bomRowCount=1
    itemCount=0

    origitem=sheet_orig.getCellByPosition(origitemcol,origstartrow).getString()
    origrowcount=origstartrow
    while origitem!='':
        #first to get the asmpn info
        if origitem[:len(asmprefix)]!=asmprefix and asmpnflag==0:
            origrowcount=origrowcount+1
            origitem=sheet_orig.getCellByPosition(origitemcol,origrowcount).getString()
            continue

        if origitem[:len(asmprefix)]==asmprefix:
            asmpnflag=1
            asmpn=sheet_orig.getCellByPosition(origPNCol,origrowcount).getString()
            asmPNDes=sheet_orig.getCellByPosition(origDesCol,origrowcount).getString()
            print("Debug: find asm component: %s"%asmPNDes)
            if preAsmPn!='':
                bomRowCount=bomRowCount+1
                itemCount=0
            preAsmPn=asmpn
            origrowcount=origrowcount+1
            origitem=sheet_orig.getCellByPosition(origitemcol,origrowcount).getString()
            continue

        #secondly,after read one line from orig sheet,the create one line in bom sheet
        for key in configdic.keys():
            if key[:5]=="Field":
                colnum=int(key[5:])-1
                valuelist=configdic[key].strip().split(',')
                if valuelist[0]=='asm_pn':
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(asmpn)
                    continue
                if valuelist[0]=='asm_description':
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(asmPNDes)
                    continue
                if valuelist[0]=='count':
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setValue(int(valuelist[1])+int(valuelist[2])*itemCount)
                    continue
                if valuelist[0]=='pn':
                    tempstr=sheet_orig.getCellByPosition(origPNCol,origrowcount).getString()
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(tempstr)
                    continue
                if valuelist[0]=='pn_description':
                    tempstr=sheet_orig.getCellByPosition(origDesCol,origrowcount).getString()
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(tempstr)
                    continue
                if valuelist[0]=='formula':
                    #there may be ',' existing in formula string,so special process is neccesary
                    formulaString=configdic[key]
                    position=formulaString.find(',')
                    formulaString=formulaString[position+1:]
                    #TODO: if there are varibles in formula, it will not changed 
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setFormula('=' + formulaString)
                    continue
                if valuelist[0]=='starttime':
                    starttime=date.today()
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(starttime.isoformat())
                    continue
                if valuelist[0]=='offtime':
                    starttime=date.today()
                    endtime=date(starttime.year+10,starttime.month,starttime.day)
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(endtime.isoformat())
                    continue
                if valuelist[0]=='quantity_numerator':
                    quan=sheet_orig.getCellByPosition(origQuantityCol,origrowcount).getString()
                    position=quan.find('/')
                    if position==-1:
                        sheet_bom.getCellByPosition(colnum,bomRowCount).setValue(int(quan))
                    else:
                        sheet_bom.getCellByPosition(colnum,bomRowCount).setValue(quan[:position])
                    continue
                if valuelist[0]=='quantity_denominator':
                    quan=sheet_orig.getCellByPosition(origQuantityCol,origrowcount).getString()
                    position=quan.find('/')
                    if position==-1:
                        sheet_bom.getCellByPosition(colnum,bomRowCount).setValue(1)
                    else:
                        sheet_bom.getCellByPosition(colnum,bomRowCount).setValue(quan[position+1:])
                    continue
                try:
                    #try to check whether is fixed string
                    origcol=ord(configdic[valuelist[0]])-ord('A')
                    tempstr=sheet_orig.getCellByPosition(origcol,origrowcount).getString()
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(tempstr)
                except KeyError:
                    tempstr=valuelist[0]
                    sheet_bom.getCellByPosition(colnum,bomRowCount).setString(tempstr)

        itemCount=itemCount+1
        bomRowCount=bomRowCount+1
        origrowcount=origrowcount+1
        origitem=sheet_orig.getCellByPosition(origitemcol,origrowcount).getString()


g_exportedScripts=Startprocess,test,generateerpbom,
