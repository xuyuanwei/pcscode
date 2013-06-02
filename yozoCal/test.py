import sys
sys.path.append("/usr/local/Yozosoft/Yozo_Office/Yozo_Office.jar")
import application
from application import Application,Workbooks

#import application.Application as Application
#import application.Workbooks as Workbooks

currentOS=Application.getOS()
if currentOS==0:
    print "OS is Windows"
if currentOS==1:
    print "OS is Linux"
if currentOS==2:
    print "OS is Mac"
if currentOS==0:
    print "OS is unkown"

wbs=Application.getWorkbooks()
workbook=wbs.getActiveWorkbook()
sheet=workbook.getWorksheets().getActiveWorksheet()
sheet.setCellValue(2,3,"test")

