sub main()
	call loadattr()
end sub

Sub printcomponents()
	Dim comp As Object
	Dim etobject As Object
	Dim filename As String
	filename="d:\tmp\logicoutput.txt"
	Open filename For Output As #1
	For Each comp In ActiveDocument.Components
		Print #1,comp.Name & " " & comp.PartType & " " & comp.PCBDecal
	Next comp
	Close #1

End Sub

sub loadattr()

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
	i=1
	while etobject.cells(i,1)<>""
		for each comp in ActiveDocument.Components
			if comp.Name=etobject.cells(i,1) then
				Print #1,comp.Name & " " & comp.PCBDecal;
				comp.PCBDecal=etobject.cells(i,2)
				Print #1, " " & comp.PCBDecal
				goto nextcell
			elseif left(comp.Name,1) > left(etobject.cells(i,1),1) then
				print #1, etobject.cells(i,1) & " is not found in sch"
				goto nextcell
			end if
		next
nextcell:
		i=i+1
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

Sub loadbominfo()
	dim comp as object
	Dim etobject As Object
	dim i,j as integer
	dim startrow,pncol,refcol as integer
	dim itemcount as integer
	dim result as integer
	Dim reflist(1 To 10000) As String
	Dim pnlist(1 To 10000) As String
	Dim itemlist(1 To 10000) As Integer
	dim arraylen as integer
	dim refstr as string
	dim pnstr as string
	dim startind as integer
	dim inttemp as integer
	dim temp as integer
	dim logfilename as string
	dim refcount as integer
	dim foundinbom as boolean
	arraylen=1000
	startind=1
	logfilename="D:\tmp\loadbominfo.log"

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

	result=MsgBox("Do you want to load the bom ino in the sheet " & etobject.ActiveWorkbook.Name, vbYesNo)	
	if result=vbno then
		exit sub
	end if
	
	' here is the format of BOM
	startrow=7
	pncol=2
	refcol=6
	If etobject.cells(startrow-1,pncol)<>"PN" Or etobject.cells(startrow-1,refcol)<>"REF" Then
		MsgBox("Format Error:PN and REF cols are not found,Exit!")
		Exit Sub
	End If
	
	Open logfilename For Output As #1 
	' load bom info to array
	i=startrow
	pnstr=etobject.cells(i,pncol)
	refstr=etobject.cells(i,refcol)
	refstr=mytrim(expand(refstr))
	while pnstr <>""
		If isKONKApn(pnstr)=True And refstr<>"" Then
			inttemp=startind
			' startind will be changed in the changerefstr2array() 
			call changerefstr2array(refstr,reflist(),startind,arraylen)
			for j=inttemp to startind
				pnlist(j)=pnstr
			next j
		End If
		i=i+1
		If i>1000 Then
			MsgBox("Over 1000")
			Exit Sub
		End If
		pnstr=etobject.cells(i,pncol)
		refstr=etobject.cells(i,refcol)
		refstr=mytrim(expand(refstr))
	wend
			
	refcount=startind-1
	for i=1 to refcount 
		itemlist(i)=i
	next i

	' sort array according reference	
	for i=1 to refcount
		for j=1 to refcount-i
			'if reflist(j)>reflist(j+1) then
			result=myrefcompare(reflist(itemlist(j)),reflist(itemlist(j+1)))
			If result=1 Then
				temp=itemlist(j)
				itemlist(j)=itemlist(j+1)
				itemlist(j+1)=temp
			ElseIf result=0 Then
				'Print #1, reflist(itemlist(j)) & " is duplicated"
				' ADD '_' BEFORE ONE REF
				'reflist(itemlist(j))="_" & reflist(itemlist(j))
			end if
		next j
	next i

	For i=1 To refcount -1
		If reflist(itemlist(i))=reflist(itemlist(i+1)) Then
			Print #1, reflist(itemlist(i)) & " is duplicated"
		End If
	Next i
	
	Print #1
	' compare and ...
	itemcount=1
	temp=1	
	i=1
	for each comp in ActiveDocument.Components
		while comp.name>reflist(itemlist(i))
			i=i+1
			if i>refcount then
				if comp.attributes("PN") is Nothing then
					comp.attributes.add "PN","BOM_NC"
				else
					comp.attributes("PN")="BOM_NC"
				end if
				print #1, comp.name & "BOM_NC"	
				goto NEXTCOMP
			end if
		wend
		if comp.name=reflist(itemlist(i)) then
			if comp.attributes("PN") is Nothing then
				comp.attributes.add "PN",pnlist(itemlist(i))
			else
				comp.attributes("PN")=pnlist(itemlist(i))
			end if
			reflist(itemlist(i))="0"
			i=i+1				
			' else: comp.name<reflist(itemlist(i))
		else	 
			if comp.attributes("PN") is Nothing then
				comp.attributes.add "PN","BOM_NC"
			else
				comp.attributes("PN")="BOM_NC"
			end if
			Print #1, comp.Name & Chr(9) & "BOM_NC"	
		end if
NEXTCOMP:
	next comp
	
	for i=1 to refcount
		if reflist(itemlist(i))<>"0" then
			print #1,reflist(itemlist(i)) & " is not in SCH"
		end if
	next i

	close #1

	msgbox("Bom info is loaded!")
	shell "notepad " & logfilename,1
	
	exit sub

etError:
	msgbox Err.Description,vbExclamation,"Error Running et"
	on error goto 0
	exit sub

End Sub

Function myrefcompare(ByVal input1 As String,ByVal input2 As String) As Integer

	Dim charpart1,charpart2 As String
	Dim numpart1,numpart2 As Integer
	Dim len1,len2 As Integer
	Dim i As Integer
	Dim char As String
	If input1="" Or input2="" Then
		myrefcompare=-2
		Exit Function
	End If
	
	input1=UCase(input1)
	input2=UCase(input2)
	If Left(input1,1)="_" Or Left(input2,1)="_" Then
		myrefcompare=StrComp(input1,input2)
		Exit Function
	End If
	
	len1=Len(input1)
	len2=Len(input2)
	i=1
	char=Mid(input1,i,1)
	While char>="A" And char<="Z"
		charpart1=charpart1 & char
		i=i+1
		If i>len1 Then
			myrefcompare=StrComp(input1,input2)
			Exit Function
		End If
		char=Mid(input1,i,1)
	Wend
	numpart1=CInt(Right(input1,len1-i+1))
	
	i=1
	char=Mid(input2,i,1)
	While char>="A" And char<="Z"
		charpart2=charpart2 & char
		i=i+1
		If i>len2 Then
			myrefcompare=StrComp(input1,input2)
			Exit Function
		End If
		char=Mid(input2,i,1)
	Wend
	numpart2=CInt(Right(input2,len2-i+1))
	
	If charpart1<> charpart2 Then
		myrefcompare=StrComp(charpart1,charpart2)
		Exit Function
	ElseIf numpart1>numpart2 Then
		myrefcompare=1
	ElseIf numpart1=numpart2 Then
		myrefcompare=0
	ElseIf numpart1<numpart2 Then
		myrefcompare=-1
	End If
		
	
End Function
		
Function isKONKApn(ByVal inputstr As String) As Boolean

Dim length As Integer
Dim i As Integer
length=Len(inputstr)
If length<>8 Then
	isKONKApn=False
	Exit Function
End If

For i=1 To length
	If Not(Mid(inputstr,i,1)>="0" And Mid(inputstr,i,1)<="9") Then
		isKONKApn=False
		Exit Function
	End If
Next i

isKONKApn=True
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

Function isPN(ByVal pn As String) As Boolean
    Dim divider As String
    Dim i, length As Integer
    Dim dividercount As Integer
    Dim dividerpos(1 To 4) As Integer
	'Dim dividerpos As Integer
	'dividerpos = Array(2, 7, 12, 15)
	dividerpos(1)=2
	dividerpos(2)=7
	dividerpos(3)=12
	dividerpos(4)=15
	
    pn = Trim(pn)
    length = Len(pn)
    If length <> 17 Then
        isPN = False
        Exit Function
    End If
        
    isPN = True
    divider = "-"
    dividercount = 0
    For i = 1 To length
        If Mid(pn, i, 1) = divider Then
            dividercount = dividercount + 1
            If dividercount > 4 Then
                isPN = False
                Exit Function
            End If
            If dividerpos(dividercount)<>i Then
                isPN = False
                Exit Function
            End If
        End If
    Next i
    If dividercount < 4 Then
        isPN = False
    End If
        
End Function


' In fact,it returns the quantity of reference
Function dividercount(ByVal inputstr As String, ByVal divider As String) As Integer
    Dim length As Integer
    Dim i As Integer
    Dim preposition, position As Integer
    length = Len(inputstr)
    dividercount = 0
    While Mid(inputstr, 1, 1) = divider
        inputstr = Right(inputstr, length - 1)
        length = Len(inputstr)
    Wend
    While Mid(inputstr, length, 1) = divider
        inputstr = Left(inputstr, length - 1)
        length = Len(inputstr)
    Wend
    preposition = 1
    position = InStr(1, inputstr, divider)
    preposition = position
    While position > 0
        If (position - preposition) = 1 Then
            GoTo nextpos
        Else
            dividercount = dividercount + 1
        End If
nextpos:
        preposition = position
        position = InStr(position + 1, inputstr, divider)
    Wend
        
    dividercount = dividercount + 1
End Function

function changerefstr2array(byval inputstr as string,byref array() as string,byref startindex as integer,byval arrlen as integer)

	dim length,count as integer
	dim position as integer
	inputstr= UCase(mytrim(inputstr))
	length = Len(inputstr)

	count = dividercount(inputstr, " ")
	if (startindex+count-1)>arrlen then
		arrlen=startindex+count-1
		ReDim preserve array(1 To arrlen)
	end if

	For i = startindex To startindex+count-1
		position = InStr(1, inputstr, " ")
		If position = 0 Then
			array(i) = inputstr
		Else
			array(i) = Left(inputstr, position - 1)
			inputstr = Right(inputstr, length - position)
			length = Len(inputstr)
		End If
    Next i
	startindex=startindex+count

end function

Function mytrim(ByVal inputstr) As String
    Dim i, length As Integer
    Dim prespacepos As Integer
    Dim char As String
    If inputstr = "" Then
        mytrim = ""
        Exit Function
    End If
    length = Len(inputstr)
   
    i = 1
    While Mid(inputstr, i, 1) = " "
        i = i + 1
        If i = length + 1 Then
            Exit Function
        End If
    Wend
    inputstr = Right(inputstr, length - (i - 1))
    length = Len(inputstr)
    
    i = length
    While Mid(inputstr, i, 1) = " "
        i = i - 1
        If i = 0 Then
            Exit Function
        End If
        
    Wend
    inputstr = Left(inputstr, i)
    length = Len(inputstr)
    
    mytrim = ""
    prespacepos = 1
    For i = 1 To length
        char = Mid(inputstr, i, 1)
        If char <> " " Then
            mytrim = mytrim & char
        Else
            If (i - prespacepos) = 1 Then
                prespacepos = i
                GoTo inext
            Else
                prespacepos = i
                mytrim = mytrim & " "
            End If
        End If
inext:
    Next i
    
End Function
