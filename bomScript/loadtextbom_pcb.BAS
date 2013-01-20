Sub Main
	Dim comps As Object	
	Dim refline As String
	Dim position As Integer
	Dim compname As String
	Dim bomvalue As String
	Dim inputfile As String
	Dim logfile As String
	Dim t As String
	t=Chr$(9)
	logfile="D:\tmp\PCB\loadtextbom.log"
	inputfile="D:\tmp\PCB\reflist.txt"
	'inputfile="e:\xulin\TEMP\bom4sch.txt"
	'logfile="E:\xulin\TEMP\loadtextbom.log"
	Open inputfile For Input As #1
	Open logfile For Output As #2
	
	For Each comps In ActiveDocument.Components
		If comps.Attributes("BOMValue") Is Nothing Then
			'comps.Attributes.Add("BOMValue", "BomNC")
			comps.Attributes.Add("BOMValue", "xxx")
		Else
			'comps.Attributes("BOMValue")="BomNC"
			comps.Attributes("BOMValue")="xxx"
		End If
	Next comps
	
	Do While Not EOF(1)
		Line Input #1, refline 'Text of this line will be stored in variable TextLine
		If refline="" Then GoTo fileclose
  		position=InStr(refline,t)
  		compname=Left(refline,position-1)
  		bomvalue=Right(refline,Len(refline)-position)
  		If compname="" Then GoTo fileclose
  		Print #2, compname
  		On Error GoTo errprocess
  		Set comps=ActiveDocument.GetObjects(ppcbObjectTypeComponent,compname,0)
  		If comps.Count=0 Then
  			Print #2, "Error:" & compname; " is not found"
  			GoTo linenext
  		End If
		If comps(1).Attributes("BOMValue") Is Nothing Then
			comps(1).Attributes.Add("BOMValue", bomvalue)
		Else
			comps(1).Attributes("BOMValue")=bomvalue
		End If
		If comps(1).Attributes("Value") Is Nothing Then
			print #2, "Info:" & compname & t & "novalue" & t & bomvalue
		Else
			print #2, "Info:" & compname & t & comps(1).Attributes("Value") & t & bomvalue
		End If
linenext:
  	Loop
  	GoTo fileclose
errprocess:
	MsgBox(Err.Description)
	Print #2,Err.Description
	On Error GoTo 0
	GoTo linenext
fileclose:
Close #1
'MsgBox("file1 is closed")
Print #2,"last comp: " & compname
'MsgBox("file2 is closed")
Close #2
On Error GoTo openerror
Shell "D:\program Files\notepad++\notepad++.exe " &logfile,1
Exit Sub
openerror:
	MsgBox(Err.Description + logfile)
End Sub
