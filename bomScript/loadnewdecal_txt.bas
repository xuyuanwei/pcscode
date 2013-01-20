sub loadnewdecal()

	dim comp as object
	Dim etobject As Object
	dim i,j as integer
	newdecalfile=".\newdecal.txt"
	logfilename=".\loadattr.log"

	result=MsgBox("Do you want to load the pcb attribute?", vbYesNo)	
	if result=vbno then
		exit sub
	end if
	
	open newdecalfile for input as #2
	Open logfilename For Output As #1 
	Print #1,"Reference" & " " & "Old_Decal" & " " & "New_Decal"
	'i=0  'start row
	dim divider as string
	dim linecount as integer
	dim compname,decal as string
	divider=Chr$(9)
	linecount=0
	do while not eof(2)
		line input #2, decalline
		linecount=linecount+1
		position=InStr(decalline,divider)
		if position<0 then
			print #1, "Error: " & linecount; " no divider found"
			goto nextline
		end if
		compname=Left(decalline,position-1)
		decal=Right(decal,Len(decalline)-position)

  		Set comps=ActiveDocument.GetObjects(plogObjectTypeComponent,compname,0)
  		If comps.Count=0 Then
  			Print #1, "Error:" & compname; " is not found in sch"
  			GoTo nextline
  		End If
		Print #1,comps(1).Name & " " & comps(1).PCBDecal;
		comps(1).PCBDecal=decal
		Print #1, " " & comps(1).PCBDecal
nextline:
		Loop
	wend
	Close #1
	close #2
	MsgBox("finished")
	Shell "D:\program Files\notepad++\notepad++.exe " & logfilename,1
	Exit Sub
end sub

sub main
	loadnewdecal
end sub
