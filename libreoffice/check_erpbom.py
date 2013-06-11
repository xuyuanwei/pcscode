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
            #TODO:need to check whether it is digital
            depth=item[3]
            layer_name=pn
            # in the erp bom,the name of lay1 is not availabe,
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
    #dbdir="E:\\xulin\\ERP\\erpbom\\"
    pre_layer_name=""   #depth in dictionary is String type
    vlookup_area="'file:///D:/ERP/KC.xls'#$Sheet1.$A$1:$C$2000"

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
        finddes_formula="=VLOOKUP(A" + str(nextrow+1) + "," + vlookup_area +",2,0)"
        finddes_formula1="=VLOOKUP(M" + str(nextrow+1) + "," + vlookup_area + ",2,0)"
        findck_formula="=VLOOKUP(M" + str(nextrow+1) + ","+ vlookup_area +",3,0)"
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
        sheet_bom.getCellByPosition(quantity_col,nextrow).setString(element['quantity'])
        sheet_bom.getCellByPosition(quantity2_col,nextrow).setValue(1)
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

#TODO
def getconfig():
    #configfile=".\\config.txt" #in Windows
    configfile="./config.txt" #in Linux
    if not os.path.isfile(configfile):
        return -1
    fconfig=open(configfile,'r')
    line=fconfig.readline().strip()
    while line!='':
        line=re.sub('\n','',line)
        if line[:1]=='#':
            line=fconfig.readline().strip()
            continue



def Startprocess():
    global linux
    linux=0
    global diff_file
    if linux:
        logfile="/home/cylinc/tmp/erpbomcheck_log.txt" #in Linux,dir cann't be like "~/dir" or there will be error
        erpbomoutput="/home/cylinc/tmp/erpbom.txt"
        origbomoutput="/home/cylinc/tmp/origbom.txt"
        diff_file="./diff.txt"
        cmd='gedit'
    else:
        rootdir="D:\\ERP\\"
        logfile=rootdir + "python_debug.txt"
        erpbomoutput=rootdir + "erpbom.txt"
        origbomoutput=rootdir + "origbom.txt"
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

    #createerpbom(origbom_item_list)

    erpbom_item_list=geterpbomlist()
    erp_bom_f=open(erpbomoutput,'w')
    printerpbom(erpbom_item_list,erp_bom_f)
    erp_bom_f.write("file is normally closed")
    erp_bom_f.closed
    compbomlist(origbom_item_list,erpbom_item_list)
    subprocess.Popen([cmd,diff_file])

    f.write("file is normally closed")
    f.closed


def test():
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
    '''
    try:
        sheet_bom=doc.getSheets().getByName("bom")
    except NoSuchElementException:
        sheets.insertNewByName("bom",1)
        sheet_bom=doc.getSheets().getByName("bom")
        '''

def compbomlist(orig_dic_list,erp_dic_list):
    f_diff=open(diff_file,'w')
    orig_str_list=[]
    erp_str_list=[]
    for item in orig_dic_list:
        orig_str_list.append(str(item['depth'])+" " + item['layername']+" " + item['pn']+ " " + str(item['quantity'])+ " " + str(item['reflist'])+ " " + item['remark'])
        '''
        orig_str_list.append(str(item['depth'])+" " + \
                item['layername']+" " + \
                item['pn']+ " " + \
                str(item['quantity'])+ " " + \
                str(item['reflist'])+ " " + \
                item['remark'])
                '''
    for item in erp_dic_list:
        if item['depth']==1:
            erp_str_list.append(str(item['depth'])+" " + orig_dic_list[0]['layername']+" " + item['pn']+ " " + str(item['quantity'])+ " " + str(item['reflist'])+ " " + item['remark'])
            '''
            erp_str_list.append(str(item['depth'])+" " + \
                    orig_dic_list[0]['layername']+" " + \
                    item['pn']+ " " + \
                    str(item['quantity'])+ " " + \
                    str(item['reflist'])+ " " + \
                    item['remark'])
                    '''
        else:
            erp_str_list.append(str(item['depth'])+" " + item['layername']+" " + item['pn']+ " " + str(item['quantity'])+ " " + str(item['reflist'])+ " " + item['remark'])
            '''
            erp_str_list.append(str(item['depth'])+" " + \
                    item['layername']+" " + \
                    item['pn']+ " " + \
                    str(item['quantity'])+ " " + \
                    str(item['reflist'])+ " " + \
                    item['remark'])
                    '''

    origlist_len=len(orig_str_list)
    erplist_len=len(erp_str_list)
    j=0
    strstoppostion=29
    for i in range(origlist_len):
        if j>=erplist_len:
            f_diff.write("erplist_len over")
            break
        #f_diff.write(orig_str_list[i] + " is in check" + "i: " + str(i) + "j: " + str(j) + "\n")

        while orig_str_list[i][:strstoppostion]>erp_str_list[j][:strstoppostion]:
            f_diff.write("erp  + " + erp_str_list[j])
            f_diff.write("\n")
            f_diff.write("\n")
            j=j+1
            continue
        if orig_str_list[i][:strstoppostion]==erp_str_list[j][:strstoppostion]:
            if orig_str_list[i]==erp_str_list[j]:
                j=j+1
                continue
            else:
                f_diff.write("orig * "+orig_str_list[i])
                f_diff.write("\n")
                f_diff.write("erp  * " +erp_str_list[j])
                f_diff.write("\n")
                f_diff.write("\n")
                j=j+1
                continue

        if orig_str_list[i][:strstoppostion]<erp_str_list[j][:strstoppostion]:
            f_diff.write("orig + " + orig_str_list[i])
            f_diff.write("\n")
            f_diff.write("\n")
            continue


        '''
        while orig_str_list[i]>erp_str_list[j] and j<erplist_len:
            if orig_str_list[i][:strstoppostion]==erp_str_list[j][:strstoppostion]:
                #TODO: here some pre-condition is needed,like the depth must be 1~9
                #orig_str_list[i]="* "+ orig_str_list[i]
                #erp_str_list[j]="* " + erp_str_list[j]
                f_diff.write("orig * "+orig_str_list[i])
                f_diff.write("\n")
                f_diff.write("erp  * " +erp_str_list[j])
                f_diff.write("\n")
                f_diff.write("\n")
                break
            else:
                #erp_str_list[j]="+ " + erp_str_list[j]
                f_diff.write("erp  + " + erp_str_list[j])
                f_diff.write("\n")
                f_diff.write("\n")
                j=j+1
                continue
        if orig_str_list[i]==erp_str_list[j]:
            orig_str_list[i]=''
            erp_str_list[j]=''
            j=j+1
            continue
        if orig_str_list[i]<erp_str_list[j]:
            f_diff.write("orig + " + orig_str_list[i])
            f_diff.write("\n")
            f_diff.write("\n")
            continue
        #i have to put j+1 here, but it for the while clause
        j=j+1
        '''
    #f_diff.write("debug: i: "+str(i)+":"+str(origlist_len)+" j: "+str(j)+":"+str(erplist_len))
    if j>=erplist_len:
        #f_diff.write("test1")
        for x in range(i,origlist_len-1):
            f_diff.write("orig + " + orig_str_list[x])
            f_diff.write("\n")
            f_diff.write("\n")
    else:
        #f_diff.write("test2")
        for x in range(j,erplist_len-1):
            f_diff.write("erp  + " + erp_str_list[x])
            f_diff.write("\n")
            f_diff.write("\n")
    f_diff.close()
    return 0


g_exportedScripts=Startprocess,
