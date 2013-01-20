
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
dim isfileflag as boolean
dim fileext as string
dim wboutputname as string
dim isfileexist as boolean
dim isfileopen as boolean
dim rowmax,colmax as integer

rowmax=5000
colmax=255
outputfile = "d:\tmp\dirtransverse.txt"
wboutputname="combine.xls"
subdirscount = 0
If Right(path, 1) <> "\" Then
    path = path & "\"
End If

If depth = 0 Then
    Open outputfile For Output As #1
    ' check if "combine.xls" is existing
    If isfileexist(path & wboutputname) Then
        iswboutputexist = True
        If isfileopen(wboutputname) Then
            wboutputisopen = True
            Set wboutput = Workbooks(wboutputname)
        Else
            wboutputisopen = False
            Set wboutput = Workbooks.Open(path & wboutputname)
        End If
    Else
        iswboutputexist = False
        Set wboutput = Workbooks.Add

        If isfileopen(wboutputname) Then
            MsgBox (wboutputname & " is opened in another directiry,click OK to close")
            Workbooks(wboutputname).Close
        End If
        Call wboutput.SaveAs(path & wboutputname)
    End If
    wboutput.Activate
    Worksheets(1).Name = "bined"
	set targetsheet=worksheets(1)
    
Else
    Set wboutput = Workbooks(wboutputname)
End If

'here set the start position in the target sheet "bined"
startrow=1
startcol=1

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
		isfileflag=0
    Else
        'MsgBox ("find file: " & filename)
        Debug.Print "find file: " & filename
		fullpath=path & filename
        Print #1, fullpath
        'Print #1, path & filename
		isfileflag=1
		
    End If
		
	'check weather is excel file
	if isfileflag then
		fileext=Right(filename, Len(filename) - InStrRev(filename, "."))
		'if it is excel file,then open it
		if fileext="xls" then
			if isfileopen(filename) then
				isopenflag=true
				set booktoread=workbooks(filename)
			else
				isopenflag=false
				set booktoread=workbooks.open(filename:=fullpath)
			end if
			'try to get the range in the booktoread
			booktoread.activate
			set sheettoread=worksheets(1)
			for row=1 to rowmax
				if cells(row,1)="" then
					rowend=row
					goto colcount
				end if
			next row
colcount:
			for col=1 to colmax
				if cells(1,col)="" then
					colend=col
					goto rangecopy
				end if
			next col
rangecopy:
			set rangetoread=ranges(cells(1,1),cells(rowend,colend))
			targetsheet.activate
			cells(startrow,1)=filename
			set targetrange=ranges(cells(startrow,2),cells(startrow+rowend-1,2+colend-1))
			rangetoread.copy targetrange
			startrow=startrow+rowend
		end if
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


sub main()
	dim path as string
	path = InputBox("Please enter the path to search: ", "enter path")
	If path = "" Then
		Exit Sub
	End If
	call dirtransverse(path,1)
	
end sub
