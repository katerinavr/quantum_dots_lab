import PyQt5.QtWidgets as QtW
import PyQt5.QtGui as QtG
import PyQt5.QtCore as QtC

import sys
import os
import qtawesome as qta


from gui import template
from core import connect

class MainWindow(QtW.QWidget):

    def __init__(self, version, params_object, resources_path, parent=None):
        QtW.QWidget.__init__(self)
        self.params = params_object
        self.resources = resources_path
        self.version = version
        self.colors = template.colors

        self.setWindowTitle("Pump Connector")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtC.Qt.white)
        self.setPalette(p)

        self.createWidgets()
        self.layoutWidgets()


        self.myConnection = connect.Connection(port=str(self.serportCBox.currentText()),
                                          baudrate=self.baudCBox.currentText(), x=self.xCbox.currentIndex(), mode=1)
        self.connected = False


    def createWidgets(self):
        logopath = os.path.abspath(os.path.join(self.resources, 'logo-with-tagline@450px.png'))
        logo = QtG.QPixmap(logopath)
        self.logoLbl = QtW.QLabel()
        self.logoLbl.setPixmap(logo)
        self.logoLbl.setAlignment(QtC.Qt.AlignCenter)

        portinfo = connect.getOpenPorts()
        portlist = connect.parsePortName(portinfo)
        portlist = portinfo
        self.serportLbl = template.WidgetLabel(label='Serial Port')
        self.serportCBox = template.CComboBox(itemlist=portlist, width=115)

        self.baudLbl = template.WidgetLabel(label='Baud Rate')
        self.baudCBox = template.CComboBox(itemlist=['9600', '38400'], currentindex=1, width=85)

        self.connectLbl = template.WidgetLabel(label='Disconnected', color=self.colors['red'][0])
        self.connectBtn = template.OutlineButton(label='Connect')
        self.connectBtn.clicked.connect(lambda:self.connect())


        self.stopBtn = template.CPushButton(label='Stop', color_scheme=self.colors['red'])
        self.stopBtn.clicked.connect(lambda:self.stop())
        self.pauseBtn = template.CPushButton(label='Pause', color_scheme=self.colors['orange'])
        self.pauseBtn.clicked.connect(lambda:self.pause())
        self.startBtn = template.CPushButton(label='Start', color_scheme=self.colors['green'])
        self.startBtn.clicked.connect(lambda:self.start())

        self.xLbl = template.WidgetLabel(label='[x]')
        self.xCbox = template.CComboBox(itemlist=['Single Pump', 'Pump Channel 1', 'Pump Channel 2', 'Cycle Mode'], currentindex=0, width=130)
        self.xCbox.currentIndexChanged.connect(lambda:self.xmodeChange())

        self.modeLbl = template.WidgetLabel(label='Flow Rate')
        #self.serportCBox = template.CComboBox(itemlist=portlist, width=115)
        self.modeCbox = template.CComboBox(itemlist=portlist, width=115)
        # template.CComboBox(itemlist=['Blank', 'Basic', 'Programmable'])
        #self.modeCbox.currentIndexChanged.connect(lambda:self.xmodeChange())

    def layoutWidgets(self):
        hbox_main = QtW.QHBoxLayout(self)

        vbox_conn = QtW.QVBoxLayout()
        vbox_conn.setContentsMargins(0, 0, 0, 0)
        vbox_conn.setSpacing(0)

        vbox_conn.addWidget(self.logoLbl)
        vbox_conn.addSpacing(20)

        grid_link = QtW.QGridLayout()
        grid_link.setHorizontalSpacing(6)
        grid_link.setVerticalSpacing(2)

        grid_link.addItem(QtW.QSpacerItem(0, 8, QtW.QSizePolicy.Fixed, QtW.QSizePolicy.Fixed), 1, 0, 1, 6)
        grid_link.addWidget(self.serportLbl, 2, 0, 1, 1)
        grid_link.addWidget(self.serportCBox, 3, 0, 1, 1)
        grid_link.addWidget(self.baudLbl, 2, 1, 1, 1)
        grid_link.addWidget(self.baudCBox, 3, 1, 1, 1)
        grid_link.addWidget(self.connectLbl, 2, 2, 1, 1)
        grid_link.addWidget(self.connectBtn, 3, 2, 1, 1)
        grid_link.addItem(QtW.QSpacerItem(0, 0, QtW.QSizePolicy.MinimumExpanding, QtW.QSizePolicy.Fixed), 2, 3, 2, 1)
        grid_link.addWidget(self.xLbl, 4, 0, 1, 1)
        grid_link.addWidget(self.xCbox, 5, 0, 1, 1)
        grid_link.addWidget(self.modeLbl, 4, 1, 1, 1)
        grid_link.addWidget(self.modeCbox, 5, 1, 1, 1)


        vbox_conn.addLayout(grid_link)

        vbox_conn.addSpacing(16)

        vbox_conn.addSpacing(8)



        vbox_conn.addSpacing(8)

        vbox_conn.addSpacing(20)

        hbox_control = QtW.QHBoxLayout()
        hbox_control.addStretch(1)
        hbox_control.addWidget(self.stopBtn)
        hbox_control.addSpacing(6)
        hbox_control.addWidget(self.pauseBtn)
        hbox_control.addSpacing(6)
        hbox_control.addWidget(self.startBtn)
        hbox_control.addStretch(1)

        vbox_conn.addLayout(hbox_control)

        hbox_main.addLayout(vbox_conn)
        hbox_main.addSpacing(6)


    def start(self):
        if self.connected:
            print("Start")
            self.myConnection.startPump()


    def stop(self):
        if self.connected:
            print("Stop")
            self.myConnection.stopPump()

    def pause(self):
        if self.connected:
            print("Pause")
            self.myConnection.pausePump()

    def xmodeChange(self):
        try:
            self.myConnection.mode = 1
            self.myConnection.x = self.xCbox.currentIndex()
        except Exception as e:
            print(e)

    def connect(self):
        if not self.connected:
            com = str(self.serportCBox.currentText())
            baud = str(self.baudCBox.currentText())
            try:
                self.myConnection.baudrate = baud
                self.myConnection.port = com
                self.myConnection.openConnection()
                self.connectLbl.setText("Connected")
                self.connectBtn.setText("Disconnect")
                self.connected = True
            except TypeError as e:
                print(e)
        else:
            self.myConnection.closeConnection()
            self.connectLbl.setText("Disconnected")
            self.connectBtn.setText("Connect")
            self.connected = False

