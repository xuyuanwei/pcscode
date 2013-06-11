#**********************************************************************
#   A module of basic operation of Libreoffice/Openoffice
#   Reference: Danny.OOo.OOoLib.py
#**********************************************************************
#   Copyright (c) 2011-2012 Cylinc
#   xuyuanwei@gmail.com
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   See:  http://www.gnu.org/licenses/lgpl.html
#
#*********************************************************************
#   If you make changes, please append to the change log below.
#
#*********************************************************************

import uno
from com.sun.star.sheet.CellInsertMode import DOWN
from com.sun.star.sheet.CellInsertMode import ROWS
from com.sun.star.sheet.FillDirection import TO_BOTTOM
from com.sun.star.sheet.FillMode import SIMPLE
from com.sun.star.sheet.CellDeleteMode import UP
from com.sun.star.sheet.CellDeleteMode import ROWS

def GetOooDesktop():
    local=uno.getComponentContext()
    resolver=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
    context=resolver.resolve("uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext")
    Desktop=context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",context)
    doc=Desktop.getCurrentComponent()
    return doc

def insertrows(sheetname,currentrow,nrow,insertmode=ROWS):
    '''insert nrow rows in the sheetname
	   sheetname: sheet handler
       currentrow: current cell position,integer
       nrow: how many rows to insert
       insertmode: NONE, DOWN, RIGHT, ROWS, COLUMNS
    '''
    #range1 is the range to be inserted
    range1 = uno.createUnoStruct("com.sun.star.table.CellRangeAddress")
    range1.StartColumn = 0 #hardcoded, should be cursor coordinate
    range1.StartRow = currentrow 
    range1.EndColumn = 1  
    range1.EndRow = currentrow + nrow -1
    try:
        sheetname.insertCells(range1,insertmode)
        return 0
    except:
        return -1

def deleterows(sheetname,currentrow,nrow,deletemode=ROWS):
    '''delete nrow rows in sheetname
	   sheetname: sheet handler
       currentrow: current cell position,integer
       nrow: how many rows to delete 
       insertmode: NONE, DOWN, RIGHT, ROWS, COLUMNS
    '''
    #range1 is the range to be deleted 
    range1 = uno.createUnoStruct("com.sun.star.table.CellRangeAddress")
    range1.StartColumn = 0 #hardcoded, should be cursor coordinate
    range1.StartRow = currentrow 
    range1.EndColumn = 1  
    range1.EndRow = currentrow + nrow -1
    sheetname.removeRange(range1,deletemode)
    return 0
