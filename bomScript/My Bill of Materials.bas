Dim part As Object
Sub Main
	dim i,j as integer
	dim tempint as integer
	dim tempstr as string
	dim report as string
	dim compcount as integer
	dim comp as object
	dim compobjs as objects
	Dim comparray() As String
	Dim item() As Integer
	Dim count As Integer
	' return all objects, not only components
	'set compobjs=activedocument.getobjects(,,false)
	'compcount=compobjs.count
	
	set compobjs=activedocument.components
	compcount=compobjs.count
	redim comparray(1 to compcount, 1 to 4) as string
	redim item(1 to compcount)
	msgbox("there is total " & compcount & " components")
	for i=1 to compcount
		item(i)=i
	next i
	' --- used to test two Dimensional string array
	'comparray(1,1)="Name"
	'comparray(1,2)="PartType"
	'comparray(1,3)="VALUE"
	'comparray(1,4)="PCBDecal"
	'msgbox(comparray(1,1) & comparray(1,2) & comparray(1,3) & comparray(1,4))
	' ---
	i=1
	For Each comp In ActiveDocument.Components
		comparray(i,1)=comp.Name
		comparray(i,2)=comp.PartType
		comparray(i,3)=AttrValue(comp, "VALUE")
		comparray(i,4)=comp.PCBDecal
		i=i+1
	next comp	

	report = DefaultFilePath & "\report.rep"
	sep = Chr(9)
	Open report For Output As #1
	Print #1, "Bill Of Materials for "; ActiveDocument; " on  "; Date
	print #1
	Print #1, "Item" & sep & "Parttype" & sep & "Value" & sep & "PCBDecal" & sep & "References" & sep & "Quantity"
	
	tempint=1
	for i=1 to compcount
		tempstr=""
		if comparray(i,1)="0" then 
			goto nexti
		else
			tempstr=comparray(i,1)
			count=1
		end if
		for j=i+1 to compcount
			if	comparray(j,1)="0" then
				goto nextj
			end if
			If UCase(comparray(i,3))=UCase(comparray(j,3)) And UCase(comparray(i,4))=UCase(comparray(j,4)) Then
				tempstr=tempstr & " " & comparray(j,1)
				comparray(j,1)="0"
				count=count + 1
			end if
nextj:
		next j
		print #1, tempint;
		print #1, sep & comparray(i,2);
		print #1, sep & comparray(i,3);
		print #1, sep & comparray(i,4);
		Print #1, sep & tempstr;
		Print #1, sep & count
		tempint=tempint +1

nexti:
		next i
	Close #1
	Shell "notepad " & report, 1
' --- bubble sort
'	for i=1 to compcount
'		for j=1 to compcount-i
'			if comparray(item(j),3)>comparray(item(j+1),3) then
'				tempint=item(j)
'				item(j)=item(j+1)
'				item(j+1)=tempint
'			end if
'			if comparray(item(j),3)=comparray(item(j+1),3) then
'				if comparray(item(j),4)>comparray(item(j+1),4) then
'					tempint=item(j)
'					item(j)=item(j+1)
'					item(j+1)=tempint
'				end if
'			end if
'		next j
'	next i	
' --- bubble sort end
End Sub

Function AttrValue (comp As Object, atrName As String) As String
	If comp.Attributes(atrName) Is Nothing Then
		AttrValue = ""
	Else
		AttrValue = comp.Attributes(atrName).value
	End If
End Function

