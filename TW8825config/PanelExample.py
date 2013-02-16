#!/usr/bin/env python

#TODO:  1. serial get available ports, open/close
#       2. serial receive event
#       3. serial send
#       4. Grid operations
import wx
import wx.grid as wxGrid
import os
import serial
import glob
import threading
import time

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX
    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data

    def Clone(self):
        self.__class__(self.GetId(), self.data)

class RegisterGrid(wxGrid.Grid):
    def __init__(self,parent,pos,size):
        wxGrid.Grid.__init__(self,parent,pos=pos,size=size)
        self.rowCount=16
        self.colCount=16
        self.labelList=['0','1','2','3','4','5','6','7','8',
            '9','A','B','C','D','E','F']
        self.labelListLen=len(self.labelList)
        self.CreateGrid(self.rowCount,self.colCount)
        self.fixedSize=25
        for i in range (0,min(self.rowCount,self.colCount,self.labelListLen)):
            self.SetColLabelValue(i,self.labelList[i])
            self.SetColSize(i,self.fixedSize)
            self.SetRowLabelValue(i,self.labelList[i])
            self.SetRowSize(i,self.fixedSize)

        self.SetColLabelSize(self.fixedSize)
        self.SetRowLabelSize(self.fixedSize)

        self.lastClickRow=-1
        self.lastClickCol=-1
        self.defaultCellBackgroudColour=self.GetCellBackgroundColour(0,0)
        self.clickedCellBackgroudColour=wx.LIGHT_GREY

        self.DisableDragColMove()
        self.DisableDragColSize()
        self.DisableDragGridSize()
        self.DisableDragRowSize()

        self.EnableEditing(False)

        #self.Bind(wxGrid.EVT_GRID_CELL_LEFT_CLICK,self.OnCellLeftClick)
        # SELECT_CELL include LEFT_CLICK event
        self.Bind(wxGrid.EVT_GRID_CMD_SELECT_CELL,self.OnCellLeftClick)

        #self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        #self.Bind(wx.EVT_KEY_UP,self.OnKeyUp)

    def OnCellLeftClick(self,evt):
        if(self.lastClickRow!=-1 and evt.GetRow()!=self.lastClickRow):
            for i in range(0,self.colCount):
                self.SetCellBackgroundColour(self.lastClickRow,i,self.defaultCellBackgroudColour)
            
        if(self.lastClickCol!=-1 and evt.GetCol()!=self.lastClickCol):
            for i in range(0,self.rowCount):
                self.SetCellBackgroundColour(i,self.lastClickCol,self.defaultCellBackgroudColour)

        for i in range(0,self.rowCount):
            self.SetCellBackgroundColour(i,evt.GetCol(),self.clickedCellBackgroudColour)
        for i in range(0,self.colCount):
            self.SetCellBackgroundColour(evt.GetRow(),i,self.clickedCellBackgroudColour)
        self.ForceRefresh()
        self.lastClickRow=evt.GetRow()
        self.lastClickCol=evt.GetCol()
        evt.Skip()


        '''
    def OnKeyDown(self,evt):
        print("Key Down captured: "+ str(evt.GetKeyCode()))
        if(evt.GetKeyCode()==61):   # KEY: =
            self.EnableEditing(False)
            if(evt.ControlDown()):
                print("Ctrl + =")
            else:
                print("=")
        if(evt.GetKeyCode()==45):   # KEY: -
            self.EnableEditing(False)
            if(evt.ControlDown()):
                print("Ctrl + -")
            else:
                print("-")
        #self.EnableEditing(True)
        evt.Skip()

    def OnKeyUp(self,evt):
        print("Key Up captured: "+ str(evt.GetKeyCode()))
        if(evt.GetKeyCode()==61 or evt.GetKeyCode()==45):
            self.EnableEditing(False)
            self.SetCellValue(self.lastClickRow,self.lastClickCol,self.GetCellValue(self.lastClickRow,self.lastClickCol)[:2])
        else:
            self.EnableEditing(True)
        evt.Skip()
            '''


            

class myPanel(wx.Panel):
    def __init__(self,parent,ser):
        wx.Panel.__init__(self,parent)
        # Serial Port part
        self.serial=ser
        self.thread=None
        self.alive=threading.Event()
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.cmdBufferLen=256
        self.cmdBuffer=['']*self.cmdBufferLen
        self.cmdBufferPushIndex=0
        self.cmdBufferPopIndex=0
        self.cmdBufferPopIndexLast=-1
        self.cmdBufferPopIndexLastCount=0
        self._parent=parent
        self.portLabel=wx.StaticText(self,label="Port:",pos=(5,32))
        self.portList=["1","2","3","4","5","6","7","8","9"]
        self.serialPortComboBox=wx.ComboBox(self,pos=(45,30),size=(100,25),choices=self.portList,style=wx.CB_DROPDOWN)

        self.portLabel=wx.StaticText(self,label="Baud:",pos=(5,62))
        self.baudList=["4800","9600","19200","38400","57600","115200"]
        self.serialBaudComboBox=wx.ComboBox(self,value="57600",pos=(45,60),size=(100,25),choices=self.baudList,style=wx.CB_DROPDOWN)
        # serial Open/Close button
        self.serialControlButton=wx.Button(self,label="Open",pos=(45,100),size=(80,25))
        self.Bind(wx.EVT_BUTTON,self.serialControl,self.serialControlButton)

        # TW8825 Register Page combobox
        self.pageLabel=wx.StaticText(self,label="Page:",pos=(5,152))
        self.pageList=["0","1","2","3","4"]
        self.RegPageComboBox=wx.ComboBox(self,value="2",pos=(45,150),size=(100,25),choices=self.pageList,style=wx.CB_DROPDOWN)

        # Read 0x00~0xFF registers in one page
        self.readAllButton=wx.Button(self,label="ReadAll",pos=(45,190),size=(80,25))
        self.Bind(wx.EVT_BUTTON,self.readOnePage,self.readAllButton)

        self.grid=RegisterGrid(self,pos=(160,10),size=(430,430))
        self.grid.Bind(wxGrid.EVT_GRID_CMD_SELECT_CELL,self.gridOnCellLeftClick)
        self.hasGridQuery=0
        self.ackOK=0
        self.gridQueryAck=""
        self.page=self.RegPageComboBox.GetValue()
        self.registerIndex=self.grid.labelList[self.grid.lastClickRow]+self.grid.labelList[self.grid.lastClickCol]

        self.grid.Bind(wx.EVT_KEY_DOWN,self.gridOnKeyDown)
        self.grid.Bind(wx.EVT_KEY_UP,self.gridOnKeyUp)

        # in editable(False) mode,using SetCellValue() wouldn't create CELL_CHANGE event
        #self.grid.Bind(wxGrid.EVT_GRID_CMD_CELL_CHANGE,self.gridOnCellChange)  
        #self.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        #self.Bind(wx.EVT_KEY_UP,self.OnKeyUp)

        self.logger=wx.TextCtrl(self,pos=(600,10),size=(180,400),style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.clearLogButton=wx.Button(self,label="Clear",pos=(700,415),size=(80,25))
        self.Bind(wx.EVT_BUTTON,self.logClear,self.clearLogButton)

        self.cmdBufferBox=wx.TextCtrl(self,pos=(600,455),size=(180,100),style=wx.TE_MULTILINE)
        self.sendButton=wx.Button(self,label="Send",pos=(700,560),size=(80,25))
        self.Bind(wx.EVT_BUTTON,self.cmdSend,self.sendButton)

        self.sendCountLabel=wx.StaticText(self,label="lines",pos=(660,565))
        self.sendCountList=["0","5","10"]
        self.sendCountComboBox=wx.ComboBox(self,value="0",pos=(600,560),size=(60,25),choices=self.sendCountList,style=wx.CB_DROPDOWN)
    # update the ports info in the serialPortComboBox
    def updateAvailablePorts(self,portsList):
        if len(portsList)==0:
            return
        self.serialPortComboBox.Clear()
        for port in portsList:
            self.serialPortComboBox.Append(port)
        self.serialPortComboBox.SetValue(portsList[0])

    # serial Open/Close button event
    def serialControl(self,evt):
        if self.serialControlButton.GetLabel()=="Open":
            # serial default setting:
            # port=None
            # baudrate=9600
            # bytesize=EIGHTBITS
            # parity=PARITY_NONE
            # stopbits=STOPBITS_ONE
            # timeout=None
            # xonxoff=False
            # rtscts=False
            # writeTimeout=None
            # dsrdtr=False
            # interCharTimeout=None
            self.serial.port=str(self.serialPortComboBox.GetValue())
            self.serial.baudrate=self.serialBaudComboBox.GetValue()
            try:
                self.serial.open()
            except serial.SerialException, e:
                dlg=wx.MessageDialog(None,str(e),"Serial Port Error",wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self._parent.SetTitle("TW8825(Serial Open)")
                self.serialControlButton.SetLabel("Close")
                if self.thread != None:
                    self.StopThread()
                self.StartThread()
        else:
            if self.serial.isOpen():
                self.serial.close()
                self.serialControlButton.SetLabel("Open")
                self._parent.SetTitle("TW8825(Serial Close)")
                if self.thread != None:
                    self.StopThread()


    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        text = event.data.replace("\r\n","\n")
        self.logger.AppendText(text)
        #text = ''.join([(c >= ' ') and c or '<%d>' % ord(c)  for c in text])
        cmdStr=self.cmdBuffer[self.cmdBufferPopIndex]
        if cmdStr!='' and cmdStr[-1]=='-' :
            if self.cmdBufferPopIndexLast != self.cmdBufferPopIndex:
                self.cmdBufferPopIndexLast = self.cmdBufferPopIndex
            else:
                self.cmdBufferPopIndexLastCount +=1
                if self.cmdBufferPopIndexLastCount==5:
                    self.logger.AppendText("Error:5 time no right answer,give up\n")
                    self.cmdBuffer[self.cmdBufferPopIndex]=''
                    self.cmdBufferPopIndex=(self.cmdBufferPopIndex+1)%self.cmdBufferLen

            # check whether the answer is corresponding to the ask
            if cmdStr[0]=='w' and text[:5]=="W="+cmdStr[1:3]+" ":
                self.cmdBuffer[self.cmdBufferPopIndex]=''
                self.cmdBufferPopIndex = (self.cmdBufferPopIndex+1)%self.cmdBufferLen
                if text[5]>='A' and text[5]<='F':
                    row=ord(text[5])-ord('A')+10
                else:
                    row=int(text[5])
                if text[6]>='A' and text[6]<='F':
                    col=ord(text[6])-ord('A')+10
                else:
                    col=int(text[6])
                self.grid.SetCellValue(row,col,text[5:7])

            elif cmdStr[0]=='r' and text[:5]=="R="+cmdStr[1:3]+" ":
                self.cmdBuffer[self.cmdBufferPopIndex]=''
                self.cmdBufferPopIndex = (self.cmdBufferPopIndex+1)%self.cmdBufferLen
                if text[5]>='A' and text[5]<='F':
                    row=ord(text[5])-ord('A')+10
                else:
                    row=int(text[5])
                if text[6]>='A' and text[6]<='F':
                    col=ord(text[6])-ord('A')+10
                else:
                    col=int(text[6])
                self.grid.SetCellValue(row,col,text[5:7])
            else:
                # let ComPortThread resend this cmd
                self.cmdBuffer[self.cmdBufferPopIndex][-1]='\n'

                '''
        if self.hasGridQuery==1:
            self.page=self.RegPageComboBox.GetValue()
            self.registerIndex=self.grid.labelList[self.grid.lastClickRow]+self.grid.labelList[self.grid.lastClickCol]
            self.gridQueryAck += text
            tempstr=self.gridQueryAck
            if tempstr[-1]!="\n":
                pass
            else:
                print("Debug: tempstr=" + tempstr)
                for ack in tempstr.strip('\n').split("\n"):
                    print("Debug: ack: " + ack + "\n")
                    # ack format: W=FF 02
                    # ack format: R=00 01

                    #print("Debug: ack vs format: " +"*" + ack + "*"+ "W=FF 0"+self.page+"*")
                    if ack[:7] == "W=FF 0"+self.page:
                        print("Debug: get FF\n")
                        self.ackOK=1
                        continue
                    #print("Debug: ack vs format: " +"*" + ack[:5] + "*"+ "R="+self.registerIndex+" "+"*")
                    if ack[:5] == "R="+self.registerIndex+" " and self.ackOK==1:
                        print("Debug: get register value\n")
                        self.grid.SetCellValue(self.grid.lastClickRow,self.grid.lastClickCol,ack[5:])
                        self.ackOK=0
                        self.hasGridQuery=0
                        self.gridQueryAck=""
                        break
            if len(tempstr)>100:
                self.hasGridQuery=0
                self.gridQueryAck=""
                self.ackOK=0
                self.logger.AppendText("Error: grid ask data timeout")
                self.grid.SetCellValue(self.grid.lastClickRow,self.grid.lastClickRow,"XX")
                '''


    def ComPortThread(self):
        """Thread that handles the incomming traffic. Does the basic input
           transformation (newlines) and generates an SerialRxEvent"""
        while self.alive.isSet():               #loop while alive event is true
            text = self.serial.read(1)          #read one, with timout
            if text:                            #check if not timeout
                n = self.serial.inWaiting()     #look if there is more to read
                if n:
                    text = text + self.serial.read(n) #get it
                #newline transformation
                #if self.settings.newline == NEWLINE_CR:
                #    text = text.replace('\r', '\n')
                #elif self.settings.newline == NEWLINE_LF:
                #    pass
                #elif self.settings.newline == NEWLINE_CRLF:
                    text = text.replace('\r\n', '\n')
                event = SerialRxEvent(self.GetId(), text)
                self.GetEventHandler().AddPendingEvent(event)
            # if cmdBuffer[][-1]='-',it means it has been send through serial
            if self.cmdBuffer[self.cmdBufferPopIndex]!='' and self.cmdBuffer[self.cmdBufferPopIndex][-1]!='-':
                self.serial.write(self.cmdBuffer[self.cmdBufferPopIndex])
                self.cmdBuffer[self.cmdBufferPopIndex][-1]='-'

    def StartThread(self):
        """Start the receiver thread"""        
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def StopThread(self):
        """Stop the receiver thread, wait util it's finished."""
        if self.thread is not None:
            self.alive.clear()          #clear alive event for thread
            # TODO: timeout every time
            self.thread.join(1)          #wait until thread has finished,timeout 1 sencond
            self.thread = None

    def readOnePage(self,evt):
        pass
    def logClear(self,evt):
        self.logger.Clear()
        evt.Skip()
    def cmdSend(self,evt):
        if self.serialControlButton.GetLabel()=="Close":
            for cmd in self.cmdBuffer:
                if cmd!='':
                    self.logger.AppendText("cmd Buffer is not emptey")
                    return
            cmdstring=self.cmdBufferBox.GetValue().replace('\n',"\r\n")
            self.serial.write(cmdstring)


    def gridOnCellLeftClick(self,evt):
        #self.grid.OnCellLeftClick(evt) # both gridOnCellLeftClick() and gridOnCellLeftClick() are called
        if self.serialControlButton.GetLabel()=="Close":
            # get current page set
            page=self.RegPageComboBox.GetValue()
            # get register index
            registerIndex=self.grid.labelList[evt.GetRow()]+self.grid.labelList[evt.GetCol()]
            self.grid.SetCellValue(evt.GetRow(),evt.GetCol(),"")
            # serial send
            cmdStr="wFF0"+page+"\r\n"
            self.cmdBuffer[self.cmdBufferPushIndex]=cmdStr
            self.cmdBufferPushIndex =(self.cmdBufferPushIndex +1)% self.cmdBufferLen
            self.logger.AppendText("grid Send: " +cmdStr)
            cmdStr="r"+registerIndex+"\r\n"
            self.cmdBuffer[self.cmdBufferPushIndex]=cmdStr
            self.cmdBufferPushIndex =(self.cmdBufferPushIndex +1)% self.cmdBufferLen
            self.logger.AppendText("grid Send: " +cmdStr)

            #self.logger.AppendText("grid Send: \n" +cmdStr)
            #self.serial.write(cmdStr)
            '''
            if self.hasGridQuery ==0:
                self.hasGridQuery=1
            else:
                self.logger.AppendText("Error: last click no ack")
                self.gridQueryAck=""
    '''
        evt.Skip()

    def writeRegister(self,regStr,value):
        page=self.RegPageComboBox.GetValue()
        cmdStr="wFF0"+page+"\r\n"+"w"+regStr+value[:2]+"\r\n"
        self.logger.AppendText("grid Send: \n" +cmdStr)
        self.serial.write(cmdStr)

    def gridOnKeyDown(self,evt):
        print("Key Down captured: "+ str(evt.GetKeyCode()))
        keycode=evt.GetKeyCode()
        if (keycode >=48 and keycode <=57) or (keycode >=65 and keycode <=70):
            origContent=self.grid.GetCellValue(self.grid.lastClickRow,self.grid.lastClickCol)
            if len(origContent)==2:
                self.grid.SetCellValue(self.grid.lastClickRow,self.grid.lastClickCol,chr(evt.GetUniChar()))
            else:
                self.grid.SetCellValue(self.grid.lastClickRow,self.grid.lastClickCol,origContent+chr(evt.GetUniChar()))
                if len(origContent)==1 and self.serialControlButton.GetLabel()=="Close":
                    regstr=self.grid.labelList[self.grid.lastClickRow]+self.grid.labelList[self.grid.lastClickCol]
                    val=self.grid.GetCellValue(self.grid.lastClickRow,self.grid.lastClickCol)
                    self.cmdBuffer[self.cmdBufferPushIndex]="w"+regstr+val+"\r\n"
                    self.cmdBufferPushIndex=(self.cmdBufferPushIndex+1)%self.cmdBufferLen
                    #self.writeRegister(regstr,val)

        if(evt.GetKeyCode()==61):   # KEY: =
            if(evt.ControlDown()):
                print("Ctrl + =")
            else:
                print("=")
        if(evt.GetKeyCode()==45):   # KEY: -
            if(evt.ControlDown()):
                print("Ctrl + -")
            else:
                print("-")
        evt.Skip()

    def gridOnKeyUp(self,evt):
        evt.Skip()

    def gridOnCellChange(self,evt):
        row=evt.GetRow()
        col=evt.GetCol()
        value=self.grid.GetCellValue(row,col)
        self.logger.AppendText("Cell content change")
        if len(value) >= 2:
            page=self.RegPageComboBox.GetValue()
            registerIndex=self.grid.labelList[row]+self.grid.labelList[col]
            cmdStr="wFF0"+page+"\r\n"+"w"+registerIndex+value[:2]+"\r\n"
            self.logger.AppendText("grid Send: \n" +cmdStr)
            self.serial.write(cmdStr)
        evt.Skip()

class myFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,title="TW8825 Register Configure Tool", size=(800, 600))
        ser=serial.Serial()
        self.panel = myPanel(self,ser)
        self.panel.Bind(wx.EVT_MOTION, self.OnMove)
        self.posLabel=wx.StaticText(self.panel,label="Pos:", pos=(10, 550))
    def OnMove(self, event):
        pos = event.GetPosition()
        self.posLabel.SetLabel("Pos: %s, %s" % (pos.x, pos.y))

        
def getAvailablePorts():
    if os.name == 'posix':
        portsList= glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')
        return portsList
    if os.name == 'nt':
        import scanwin32
        portsList=[]
        for order,port,desc,hwid in sorted(scanwin32.comports()):
            portsList.append(str(port))
        return portsList
        
if __name__ == "__main__":
    app=wx.App(False)
    frame=myFrame()
    frame.panel.updateAvailablePorts(getAvailablePorts())
    frame.Show()
    app.MainLoop()
