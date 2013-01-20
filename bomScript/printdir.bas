Option Explicit
' find PTB, then collect them in one et file
Sub collectsheetinfo()

Dim path As String
Dim result As Integer
Dim i, j, k, row, boardcount As Integer
Dim PTBnum() As Integer
Dim workbook1, workbook2 As workbook
Dim PTBworksheet As Worksheet
Dim collectbook As workbook
Dim range1 As Range
Dim versionstr, machinename, machinenum As String
Dim fullpath As String
path = InputBox("Please enter the path to search for PTB: ", "enter path")
If path = "" Then
    Exit Sub
End If
row = 1
Set collectbook = Workbooks.Add
Call collectbook.SaveAs(path & "PTBcollect.et")

result = findspreadsheet(path, 0, 1)
fullpath = path & "spreadsheetinfo.et"
Set workbook1 = Workbooks.Open(filename:=fullpath)
i = 1
While Cells(i, 1) <> ""
    result = 0
    workbook1.Activate
    If Cells(i, 1) <> "spreadsheetinfo.et" And Cells(i, 1) <> "PTBcollect.et" Then
        fullpath = Cells(i, 2)
        Set workbook2 = Workbooks.Open(filename:=fullpath)
        workbook2.Activate
        result = isPTB(workbook2.Name, PTBnum())
        ' copy PTB data to the collectbook
        ' 机型 代号 版本 组件名称 责任人 PCB编号 组件编号 状态 备注
        For j = 1 To result
            workbook2.Activate
            Set PTBworksheet = Worksheets(PTBnum(j))
            PTBworksheet.Activate
            'versionstr = PTBworksheet.Name      ' temp use
            machinename = Trim(Right(Cells(3, 1), Len(Cells(3, 1)) - 5))
            machinenum = Trim(Right(Cells(3, 4), Len(Cells(3, 4)) - 5))
            versionstr = Trim(Right(Cells(5, 7), Len(Cells(5, 7)) - 11))
                        
            'Set range1 = Range("B1")
            'boardcount = range1.Rows.count - 6
            collectbook.Activate
            k = 7
            'For k = 7 To range1.Rows.count
            While PTBworksheet.Cells(k, 2) <> ""
                Cells(row, 1) = k - 6 '& "/" & range1.Rows.count - 6
                Cells(row, 2) = machinename
                Cells(row, 3) = machinenum
                Cells(row, 4) = versionstr
                Cells(row, 5) = PTBworksheet.Cells(k, 2)    '组件名称
                Cells(row, 6) = PTBworksheet.Cells(k, 3)    '责任人
                Cells(row, 7) = PTBworksheet.Cells(k, 7)    'PCB编号
                Cells(row, 8) = PTBworksheet.Cells(k, 8)    '组件编号
                Cells(row, 9) = PTBworksheet.Cells(k, 9)    '状态
                Cells(row, 10) = PTBworksheet.Cells(k, 12)  '备注
                k = k + 1
                row = row + 1
            Wend
        Next j
        workbook2.Close savechanges:=False
    End If
    
    If result > 0 Then
        MsgBox ("find PTB,result is: " & result)
    End If
    
    i = i + 1
Wend
workbook1.Close
collectbook.Close savechanges:=True

End Sub


Sub printfiles()
Dim pathname, result As String
pathname = "D:\tmp\EIO\"
'pathname = "D:\Document\eio_and_wps"
'printdir (pathname)
'openetfiles (pathname)
'result = dirtransverse(pathname, 0)
result = findspreadsheet(pathname, 0, 0)

End Sub

Sub expandref()

Dim row, col As Integer
row = 2
col = 5
While Cells(row, col) <> ""
    Cells(row, col + 2) = expand(Cells(row, col))
    row = row + 1
Wend

End Sub

Sub notanything()


End Sub

' return count of PTB
Function isPTB(ByVal filename As String, ByRef num() As Integer) As Integer

Dim i, sheetcount As Integer
Dim PTBsheetcount As Integer
Dim formatflag As Boolean
Dim workbook1 As workbook
Dim worksheet1 As Worksheet
Dim nosubfixfilename As String
nosubfixfilename = Left(filename, InStr(1, filename, ".") - 1)

Set workbook1 = Workbooks(filename)
'For Each workbook1 In Workbooks
    workbook1.Activate
    MsgBox (workbook1.Name)
    sheetcount = Worksheets.count
    PTBsheetcount = 0
    For i = 1 To sheetcount
        Set worksheet1 = Worksheets(i)
        worksheet1.Activate
        formatflag = Left(Cells(3, 1), 5) = "机种型号：" And Left(Cells(3, 4), 5) = "机种代号："
        formatflag = formatflag And Left(Cells(5, 4), 6) = "上一版配套表" And Left(Cells(5, 7), 5) = "新版配套表"
        If formatflag Then
            PTBsheetcount = PTBsheetcount + 1
            ReDim Preserve num(1 To PTBsheetcount)
            num(PTBsheetcount) = i
        End If
    Next i
'Next workbook1
    
isPTB = PTBsheetcount

End Function

' return count of BOM
Function isBOM(ByVal filename As String, ByRef num() As Integer) As Integer

Dim i, sheetcount As Integer
Dim BOMsheetcount As Integer
Dim formatflag As Boolean
Dim workbook1 As workbook
Dim worksheet1 As Worksheet
Dim nosubfixfilename As String
nosubfixfilename = Left(filename, InStr(1, filename, ".") - 1)

Set workbook1 = Workbooks(filename)
'For Each workbook1 In Workbooks
    workbook1.Activate
    'MsgBox (workbook1.Name)
    sheetcount = Worksheets.count
    BOMsheetcount = 0
    For i = 1 To sheetcount
        Set worksheet1 = Worksheets(i)
        worksheet1.Activate
        formatflag = Left(Cells(3, 1), 5) = "机种型号：" And Left(Cells(3, 3), 5) = "机种代号："
        formatflag = formatflag And Left(Cells(4, 1), 5) = "组件编号：" And Left(Cells(4, 3), 5) = "组件名称："
        formatflag = formatflag And Cells(6, 1) = "序号" And Cells(6, 2) = "物料编号"

        If formatflag Then
            BOMsheetcount = BOMsheetcount + 1
            ReDim Preserve num(1 To BOMsheetcount)
            num(BOMsheetcount) = i
        End If
    Next i
'Next workbook1
    
isBOM = BOMsheetcount

End Function
' base on the dirtransverse() function
' mode: 0: find spreadsheet; 1: find PTB or BOM
Function findspreadsheet(ByVal path As String, ByVal depth As Integer, ByVal mode As Integer) As Integer

Dim filename As String
Dim maxdepth As Integer
Dim result, PTBresult, BOMresult, fileattr As Integer
Dim subdirs() As String
Dim PTBsheetnum() As Integer
Dim BOMsheetnum() As Integer
Dim subdirscount As Integer
Dim i As Integer
Dim outputfile As String
Dim fileext As String
'Dim workbook1, BOMcollect As workbook
Dim wboutput As workbook
Dim booktocheck As workbook
Dim sourcesheet As Worksheet
' in wboutput,sheet(1): PTB;sheet(2):BOM;sheet(3):other;sheet(4): all
Dim currentsheet As Worksheet
Dim fullpath As String
Dim maxversionsheetno As Integer
' row1: row in sheet1; so on
'Static row1, row2, row3, row4 As Integer    ' static only is meaningful to Sub,but not Function
Dim row1, row2, row3, row4 As Integer
Dim maxversionstr As String
Dim machinename(), machinenum(), versionstr() As String
Dim groupwareno(), groupwarename() As String
Dim wboutputisopen, isopenflag As Boolean
Dim wboutputname As String
Dim sheetcount As Integer

wboutputname = "spreadsheetinfo.et"

' big problem,when reenter to this function,below value will reset
row1 = row1 + 1
row2 = row2 + 1
row3 = row3 + 1
row4 = row4 + 1


outputfile = "d:\tmp\dirtransverse.txt"
subdirscount = 0
If Right(path, 1) <> "\" Then
    path = path & "\"
End If
If depth = 0 Then
    Open outputfile For Output As #1
    ' check if "spreadsheetinfo.et" is existing
    If isfileexist(path & wboutputname) Then
        If isfileopen(wboutputname) Then
        
            wboutputisopen = True
            Set wboutput = Workbooks(wboutputname)
        Else
            wboutputisopen = False
            Set wboutput = Workbooks.Open(path & wboutputname)
        End If
    Else
        Set wboutput = Workbooks.Add
        If isfileopen(wboutputname) Then
            MsgBox (wboutputname & " is opened in another directiry,click OK to close")
            Workbooks(wboutputname).Close
        End If
        Call wboutput.SaveAs(path & wboutputname)
    End If
Else
    Set wboutput = Workbooks(wboutputname)
End If

maxdepth = 10
filename = Dir(path, vbDirectory)
If filename = "" Then
    result = MsgBox(path & "is not found", vbOKOnly, "Warning")
    findspreadsheet = -1        ' **** follow the function name
    Exit Function
End If
       
'Line Input [#]StreamNum, S$
       
While filename <> ""
    If filename = "." Or filename = ".." Then
        GoTo nextfile1
    End If

    If GetAttr(path & filename) = vbDirectory Then
        'MsgBox ("find dir: " & filename)
        subdirscount = subdirscount + 1
        'Debug.Print "find dir: " & filename
        ReDim Preserve subdirs(1 To subdirscount)
        subdirs(subdirscount) = path & filename & "\"
        GoTo nextfile1
    Else
        'MsgBox ("find file: " & filename)
        'Debug.Print "find file: " & filename
        fileext = Right(filename, Len(filename) - InStrRev(filename, "."))
        If fileext = "et" Or fileext = "xls" Then
        fullpath = path & filename
        Print #1, fullpath
            If mode = 0 Then
                wboutput.Activate
                sheetcount = wboutput.Worksheets.count
                If sheetcount = 3 Then  ' more strict check is need?
                    wboutput.Worksheets.Add
                End If
                Set currentsheet = Worksheets(4)
                currentsheet.Name = "All"
                currentsheet.Activate
                Cells(row4, 1) = filename
                Cells(row4, 2) = fullpath
                Cells(row4, 3) = FileDateTime(fullpath)
                row4 = row4 + 1
                Cells(row4, 1) = ""
                GoTo nextfile1
            End If
            
            If mode = 1 Then ' to find PTB and BOM
                If isfileopen(filename) Then
                    isopenflag = True
                    Set booktocheck = Workbooks(filename)
                Else
                    isopenflag = False
                    Set booktocheck = Workbooks.Open(filename:=fullpath)
                End If
                PTBresult = isPTB(booktocheck.Name, PTBsheetnum())
                BOMresult = isBOM(booktocheck.Name, BOMsheetnum())
                If PTBresult = 0 And BOMresult = 0 Then
                    wboutput.Activate
                    Set currentsheet = Worksheets(3)
                    currentsheet.Activate
                    Cells(row3, 1) = filename
                    Cells(row3, 2) = fullpath
                    Cells(row3, 3) = FileDateTime(fullpath)
                    row3 = row3 + 1
                    Cells(row3, 1) = ""
                    GoTo nextfile
                End If
                If PTBresult > 0 Then
                    ReDim machinename(1 To PTBresult)
                    ReDim machinenum(1 To PTBresult)
                    ReDim versionstr(1 To PTBresult)
                    ' fetch the PTB info
                    booktocheck.Activate
                    maxversionstr = "A0"
                     
                    ' I assume that the PTB sheets in one workbook are of the same machine
                    For i = 1 To PTBresult
                        Set sourcesheet = Worksheets(PTBsheetnum(i))
                        sourcesheet.Activate
                        machinename(i) = Trim(Right(Cells(3, 1), Len(Cells(3, 1)) - 5))
                        machinenum(i) = Trim(Right(Cells(3, 4), Len(Cells(3, 4)) - 5))
                        versionstr(i) = Trim(Right(Cells(5, 7), Len(Cells(5, 7)) - 11))
                        ' record the max version
                        If versionstr(i) > maxversionstr Then
                            maxversionstr = versionstr(i)
                            maxversionsheetno = i
                        End If
                    Next i
                    ' write PTB info of max version to workbook1
                    wboutput.Activate
                    Set currentsheet = wboutput.Worksheets(1)
                    currentsheet.Activate
                    Cells(row1, 1) = machinename(maxversionsheetno)
                    Cells(row1, 2) = machinenum(maxversionsheetno)
                    Cells(row1, 3) = versionstr(maxversionsheetno)
                    Cells(row1, 4) = fullpath
                    Cells(row1, 5) = FileDateTime(fullpath)
                    row1 = row1 + 1
                    Cells(row1, 1) = ""
                Else
                '.............................................
                    ReDim machinename(1 To BOMresult)
                    ReDim machinenum(1 To BOMresult)
                    ReDim versionstr(1 To BOMresult)
                    ReDim groupwareno(1 To BOMresult)
                    ReDim groupwarename(1 To BOMresult)
                    ' fetch the PTB info
                    booktocheck.Activate
                    maxversionstr = "A0"
                    
                    
                    For i = 1 To BOMresult
                        Set sourcesheet = Worksheets(BOMsheetnum(i))
                        sourcesheet.Activate
                        machinename(i) = Trim(Right(Cells(3, 1), Len(Cells(3, 1)) - 5))
                        machinenum(i) = Trim(Right(Cells(3, 3), Len(Cells(3, 3)) - 5))
                        groupwareno(i) = Trim(Right(Cells(4, 1), Len(Cells(4, 1)) - 5))
                        groupwarename(i) = Trim(Right(Cells(4, 3), Len(Cells(4, 3)) - 5))
                        versionstr(i) = Trim(Right(Cells(5, 5), Len(Cells(5, 5)) - 4))
                    Next i
                    
                    wboutput.Activate
                    Set currentsheet = wboutput.Worksheets(2)
                    currentsheet.Activate
                    For i = 1 To BOMresult
                        Cells(row2, 1) = machinename(i)
                        Cells(row2, 2) = machinenum(i)
                        Cells(row2, 3) = groupwareno(i)
                        Cells(row2, 4) = groupwarename(i)
                        Cells(row2, 5) = versionstr(i)
                        Cells(row2, 6) = fullpath
                        Cells(row2, 7) = FileDateTime(fullpath)
                        row2 = row2 + 1
                        Cells(row2, 1) = ""
                    Next i
                '.................................................................
                End If
            End If
        Else
            GoTo nextfile1
        End If
    End If
nextfile:
    If isopenflag = False Then
        booktocheck.Close savechanges:=False
    End If
nextfile1:
    filename = Dir()
Wend

If depth <= 10 Then
    For i = 1 To subdirscount
        Call findspreadsheet(subdirs(i), depth + 1, mode) ' **** follow the function name
    Next i
End If


If depth = 0 Then
    Close #1
    MsgBox ("DirTransverse finish")
    'Shell "Notepad " & outputfile, 1
    Call wboutput.Save
End If
    
End Function



' dir() cannot be used in recurse
' follow function refers to "http://topic.csdn.net/t/20010723/16/205693.html"
' using as a module
Function dirtransverse(ByVal path As String, ByVal depth As Integer) As Integer

Dim filename As String
Dim maxdepth As Integer
Dim result, fileattr As Integer
Dim subdirs() As String
Dim subdirscount As Integer
Dim i As Integer
Dim outputfile As String

outputfile = "d:\tmp\dirtransverse.txt"
subdirscount = 0
If Right(path, 1) <> "\" Then
    path = path & "\"
End If
If depth = 0 Then
    Open outputfile For Output As #1
End If

maxdepth = 10
filename = Dir(path, vbDirectory)
If filename = "" Then
    result = MsgBox(path & "is not found", vbOKOnly, "Warning")
    dirtransverse = -1
    Exit Function
End If
       
'Line Input [#]StreamNum, S$
       
While filename <> ""
    If filename = "." Or filename = ".." Then
        GoTo nextfile
    End If
    'If GetAttr(path & filename) = vbDirectory And depth <= maxdepth Then
    If GetAttr(path & filename) = vbDirectory Then
        'MsgBox ("find dir: " & filename)
        subdirscount = subdirscount + 1
        Debug.Print "find dir: " & filename
        ReDim Preserve subdirs(1 To subdirscount)
        subdirs(subdirscount) = path & filename & "\"
    Else
        'MsgBox ("find file: " & filename)
        Debug.Print "find file: " & filename
        Print #1, path & filename
    End If
nextfile:
    filename = Dir()
Wend

If depth <= 10 Then
    For i = 1 To subdirscount
        Call dirtransverse(subdirs(i), depth + 1)
    Next i
End If


If depth = 0 Then
    Close #1
    MsgBox ("DirTransverse finish")
    Shell "Notepad " & outputfile, 1
End If
    
End Function
' using trim() is better,if divider is blank
Function stripstring(ByVal inputstr As String, ByVal devider As String, ByRef count) As String
    
    Dim char As String
    Dim length As Integer
    Dim i As Integer
    Dim startblankcount, endblankcount As Integer
    Dim twodividerflag As Boolean
    Dim position As Integer
    Dim result As String
    
    twodividerflag = False
    startblankcount = 0
    endblankcount = 0
    length = Len(inputstr)
    result = ""
    i = 1
    char = Mid(inputstr, i, 1)
    While char = " " Or char = divider
        startblankcount = startblankcount + 1
        i = i + 1
        char = Mid(inputstr, i, 1)
    Wend
    
    i = length
    char = Mid(inputstr, i, -1)
    While char = " " Or char = divider
        endblankcount = endblankcount + 1
        i = i - 1
        char = Mid(inputstr, i, -1)
    Wend
    inputstr = Mid(inputstr, startblankcount + 1, length - startblankcount - endblankcount)
    
    position = InStr(1, inputstr, divider)
    If position = 0 Then
        stripstring = inputstr
        Exit Function
    End If
    i = position
    While position <> 0
        If position = i + 1 Then
        
        '.............
        
        End If
        
        '.................
        
    Wend
    
    '......................
End Function
' It is used to expand "C123-C125 C133" to be "C123 C124 C125 C133"
Function expand(ByVal inputstr As String) As String

Dim flagchar, divider, tempstr As String
Dim position, startpos, endpos As Integer
Dim temp As Integer
Dim length As Integer
Dim result As String
Dim prefix, tempchar As String
Dim ref, startref, endref As Integer

length = Len(inputstr)
flagchar = "-"
divider = " "
result = ""
prefix = ""

position = InStr(1, inputstr, flagchar)
If position = 0 Then
    expand = inputstr
    Exit Function
End If
While position <> 0
    prefix = ""
    ' get the start position and the end position
    tempstr = Left(inputstr, position)
    startpos = InStrRev(tempstr, divider)
    ' get prefix string
    temp = startpos + 1
    tempchar = Mid(inputstr, temp, 1)
    While tempchar >= "A" And tempchar <= "Z"
        prefix = prefix & tempchar
        temp = temp + 1
        tempchar = Mid(inputstr, temp, 1)
    Wend
    startref = CInt(Mid(inputstr, temp, position - temp))
    
    If startpos <> 0 Then
        result = result & Left(tempstr, startpos)
    End If
    'tempstr = Right(inputstr, length - position)
    endpos = InStr(position, inputstr, divider)
    
    If endpos = 0 Then
        endpos = length
    End If
    endref = CInt(Mid(inputstr, position + 1, endpos - position))
    
    For ref = startref To endref
        result = result & prefix & CStr(ref) & " "
    Next ref
    
    inputstr = Right(inputstr, length - endpos)
    length = Len(inputstr)
    position = InStr(1, inputstr, flagchar)
    If position = 0 Then
        result = result & inputstr
    End If
Wend
    expand = result

End Function
Function isfileexist(ByVal fullpath As String) As Boolean
    If Dir(fullpath) <> "" Then
        isfileexist = True
    Else
        isfileexist = False
    End If
End Function

Function isfileopen(ByVal filename As String) As Boolean
    Dim fileopen As workbook
    For Each fileopen In Workbooks
        If fileopen.Name = filename Then
            isfileopen = True
            Exit Function
        End If
    Next fileopen
    isfileopen = False
End Function
Sub logicbomcomp()
    Dim i, j As Integer
    Dim activebookcount As Integer
    Dim wb As workbook
    Dim oldbom, newbom As workbook
    Dim oldbomflag, newbomflag As Boolean
    Dim partnamepos, decalpos, footprintpos, referencepos, qtypos As Integer
    For Each wb In Workbooks
        activebookcount = activebookcount + 1
    Next wb
    If activebookcount <> 2 Then
        MsgBox ("Warning: more than 2 workbook are opened")
        Exit Sub
    End If

    oldbomflag = False
    newbomflag = False
    For Each wb In Workbooks
        If InStr(1, wb.Name, "old") Or InStr(1, wb.Name, "OLD") Then
            Set oldbom = wb
            oldbomflag = True
        End If
        If InStr(1, wb.Name, "new") Or InStr(1, wb.Name, "NEW") Then
            Set newbom = wb
            newbomflag = True
        End If
    Next wb

    If oldbomflag = False Or newbomflag = False Then
        MsgBox ("Warning: one bom is not found")
        Exit Sub
    End If

    ' look at the first row,try to find "Part Name","PCB DECAL","PCB Footprint","Reference","Qty"
    For i = 1 To 255
        If Cells(1, i) = "Part Name" Then
            partnamepos = i
        End If
        If Cells(1, i) = "PCB DECAL" Then
            decalpos = i
        End If
        If Cells(1, i) = "PCB Footprint" Then
            footprintpos = i
        End If
        If Cells(1, i) = "Reference" Then
            referencepos = i
        End If
        If Cells(1, i) = "Qty" Then
            qtypos = i
        End If
    Next i

    oldbom.Activate


            

End Sub

Function tworefstringcomp(ByRef refstr1 As String, ByRef refstr2 As String) As Integer
    Dim length1, length2 As Integer
    Dim tempstr As String
    Dim array1(), array2() As String
    Dim count1, count2 As Integer
    Dim position As Integer
    Dim i As Integer
    If refstr1 = "" Or refstr2 = "" Then
        MsgBox ("tworefstringcomp Warning:reference NULL")
        tworefstringcomp = -1
        Exit Function
    End If
    refstr1 = UCase(Trim(refstr1))
    refstr2 = UCase(Trim(refstr2))
    length1 = Len(refstr1)
    length2 = Len(refstr2)
    
    count1 = dividercount(refstr1, " ")
    count2 = dividercount(refstr2, " ")
    ReDim array1(1 To count1)
    ReDim array2(1 To count2)
    
    For i = 1 To count1
        position = InStr(1, refstr1, " ")
        array1(i) = Left(refstr1, position)
        inputstr = Right(refstr1, length1 - position)
    Next i
    
    For i = 1 To count1
        position = InStr(1, refstr1, " ")
        array1(i) = Left(refstr1, position - 1)
        refstr1 = Right(refstr1, length1 - position)
    Next i
    For i = 1 To count2
        position = InStr(1, refstr2, " ")
        array2(i) = Left(refstr2, position - 1)
        refstr2 = Right(refstr2, length2 - position)
    Next i

    result = twoarraycomp(array1(), count1, array2(), count2)

    refstr1 = ""
    refstr2 = ""

    For i = 1 To count1
        If array1(i) <> " " Then
            refstr1 = refstr1 & " " & array1(i)
        End If
    Next i
    For i = 1 To count2
        If array2(i) <> " " Then
            refstr2 = refstr2 & " " & array2(i)
        End If
    Next i


End Function

Function twoarraycomp(ByRef a1() As String, ByVal leng1 As Integer, ByRef a2() As String, ByVal leng2 As Integer)
    Dim i, j As Integer
    For i = 1 To leng1
        If a1(i) = " " Then
            GoTo inext
        End If
        For j = 1 To leng2
            If a2(j) = " " Then
                GoTo jnext
            End If
            If a1(i) = a2(j) Then
                a1(i) = " "
                a2(j) = " "
                GoTo inext
            End If
jnext:
        Next j
inext:
    Next i
End Function

End Function


Function dividercount(ByVal inputstr As String, ByVal divider As String) As Integer
    Dim length As Integer
    Dim i As Integer
    Dim preposition, positon As Integer
    length = Len(inputstr)
    dividercount = 0
    If Mid(inputstr, 1, 1) = divider Then
        inputstr = Right(inputstr, length - 1)
        length = Len(inputstr)
    End If
    If Mid(inputstr, length, 1) = divider Then
        inputstr = Left(inputstr, length - 1)
        length = Len(inputstr)
    End If
    preposition = 1
    position = InStr(1, inputstr, divider)
    preposition = positon
    While position > 0
        If (position - preposition) = 1 Then
            GoTo nextpos
        Else
            dividercount = dividercount + 1
        End If
nextpos:
        preposition = positon
        position = InStr(position, inputstr, divider)
    Wend
        
    dividercount = dividercount + 1
End Function

' for experimental
Function printdir(ByVal path As String)
Dim filename As String
Dim fullpath As String

filename = Dir(path, vbDirectory)

While filename <> ""
    fullpath = path & filename
    If GetAttr(fullpath) = vbDirectory Then
        MsgBox ("find dir: " & filename)
    Else
        MsgBox ("find file: " & filename)
    End If
    filename = Dir
Wend
End Function
' for experimental
Function openetfiles(ByVal path As String)
Dim filename As String
Dim fullpath As String
Dim dotposition As Integer
Dim postfix As String

Dim row, col As Integer

filename = Dir(path, vbDirectory)

While filename <> ""
    fullpath = path & filename
    If GetAttr(fullpath) = vbDirectory Then
        MsgBox ("find dir: " & filename)
    Else
        MsgBox ("find file: " & filename)
        dotposition = InStr(1, filename, ".")
        postfix = Right(filename, Len(filename) - dotposition)
        If postfix = "et" Then
            'Workbooks.Open (fullpath)
            MsgBox ("file: " & filename & "is open,click" & "OK to close")
            'Workbooks.Application.Visible = False
            'ThisWorkbook.Close (filename)
        End If
    End If
    filename = Dir
Wend
End Function
