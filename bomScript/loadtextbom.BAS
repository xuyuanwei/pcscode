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
	inputfile="D:\tmp\PCB\reflist.txt"
	logfile="D:\tmp\PCB\loadtextbom.log"
	Open inputfile For Input As #1
	Open logfile For Output As #2
	Do While Not EOF(1)
		Line Input #1, refline 'Text of this line will be stored in variable TextLine
  		position=InStr(refline,t)
  		compname=Left(refline,position-1)
  		bomvalue=Right(refline,Len(refline)-position)
  		If compname="" Then GoTo fileclose
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
	Print #2,Err.Description
	On Error GoTo 0
	GoTo linenext
fileclose:
Close #1
Close #2
Shell "D:\program Files\notepad++\notepad++.exe " & logfile,1
End Sub
