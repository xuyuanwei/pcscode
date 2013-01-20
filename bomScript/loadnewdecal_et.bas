sub loadnewdecal()

	dim comp as object
	Dim etobject As Object
	dim i,j as integer
	logfilename=".\loadattr.log"

	on error resume next
	set etobject=getobject(,"et.application")
	on error goto eterror
	if etobject is nothing then
		'set etobject=createobject("et.application")
		msgbox("No et file is opening. Exit!")
		exit sub
	elseif etobject.workbooks.count>1 then
		msgbox("too many workbooks are opened. Exit!")
		exit sub
	end if

	result=MsgBox("Do you want to load the attribute in the sheet " & etobject.ActiveWorkbook.Name, vbYesNo)	
	if result=vbno then
		exit sub
	end if
	
	Open logfilename For Output As #1 
	Print #1,"Reference" & " " & "Old_Decal" & " " & "New_Decal"
	i=2  'start row
	compname=etobject.cells(i,1)
	while compname<>""
  		Set comps=ActiveDocument.GetObjects(plogObjectTypeComponent,compname,0)
  		If comps.Count=0 Then
  			Print #1, "Error:" & compname; " is not found in sch"
  			GoTo nextcell
  		End If
		Print #1,comps(1).Name & " " & comps(1).PCBDecal;
		comps(1).PCBDecal=etobject.cells(i,2)
		Print #1, " " & comps(1).PCBDecal

		'for each comp in ActiveDocument.Components
		'	if comp.Name=etobject.cells(i,1) then
		'		Print #1,comp.Name & " " & comp.PCBDecal;
		'		comp.PCBDecal=etobject.cells(i,2)
		'		Print #1, " " & comp.PCBDecal
		'		goto nextcell
		'	elseif left(comp.Name,1) > left(etobject.cells(i,1),1) then
		'		print #1, etobject.cells(i,1) & " is not found in sch"
		'		goto nextcell
		'	end if
		'next
nextcell:
		i=i+1
		compname=etobject.cells(i,1)
	wend
	Close #1
	MsgBox("finished")
	Shell "D:\program Files\notepad++\notepad++.exe " & logfilename,1
	Exit Sub
etError:
	MsgBox Err.Description,vbExclamation,"Error Running et"
	On Error GoTo 0
	Exit Sub
end sub

sub main
	loadnewdecal
end sub
