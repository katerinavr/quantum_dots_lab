import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QAbstractItemView, QGridLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QTableWidget, QMessageBox, QTextEdit, QComboBox, QWidget, \
    QMainWindow, QRadioButton, QGroupBox, QButtonGroup, QTableWidgetItem, QSpacerItem, QSizePolicy, QHeaderView, QFrame, \
    QListWidget, QListWidgetItem, QStyleFactory, QStyledItemDelegate
from PyQt5.QtGui import QIcon, QPainterPath, QRegion, QColor, QPixmap, QPalette, QDoubleValidator, QIntValidator
from PyQt5.QtCore import QRectF, Qt, QSize
import qtawesome as qta

colors = {'main':['#154C73'], 'highlight':['#227DBF', '#195C8B'], 'secondary':['#195C8B'], 'dark':['#103A59'],
          'orange':['#E85B23', '#C44614'], 'green':['#65A219', '#497612'], 'red':['#D03D39', '#AD2D29']}

buttons = {'width':120, 'height':35}
fields = {'width':105, 'height':35}

volumeValidator = QDoubleValidator()
volumeValidator.setDecimals(5)
volumeValidator.setNotation(QDoubleValidator.StandardNotation)

rateValidator = QDoubleValidator()
rateValidator.setDecimals(5)
rateValidator.setNotation(QDoubleValidator.StandardNotation)

delayValidator = QDoubleValidator()
delayValidator.setDecimals(3)
delayValidator.setNotation(QDoubleValidator.StandardNotation)

idValidator = QDoubleValidator()
idValidator.setDecimals(3)
idValidator.setNotation(QDoubleValidator.StandardNotation)


intValidator = QIntValidator()

class Header1Label(QLabel):
    def __init__(self, parent=None, label=''):
        QLabel.__init__(self)

        self.setStyleSheet("QLabel {font-size: 24pt; color: #4B4B4B; background-color: transparent;}")
        self.setText(label)

class Header2Label(QLabel):
    def __init__(self, parent=None, label='', color='black'):
        QLabel.__init__(self)
        self.setStyleSheet("QLabel {font-size: 16pt; font-weight: bold; color: %s}" % color)
        self.setText(label)

class WidgetLabel(QLabel):
    def __init__(self, parent=None, label='', width=None, margin=[0, 0, 0, 0]):
        QLabel.__init__(self)
        self.setStyleSheet("QLabel {font-size: 12pt; color: #4B4B4B; font-weight: bold; background-color: transparent; "
                           "margin: %spx %spx %spx %spx;}"
                           % tuple(margin))
        self.setText(label)
        if width:
            self.setFixedWidth(width)
        # self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


class EditLine(QLineEdit):
    def __init__(self, parent=None, defaulttext='', validator=None):
        QLineEdit.__init__(self)
        self.setStyleSheet("QLineEdit {background-color: transparent; font-size: 13pt; border: none; margin-left: 0px; "
                           "padding-top: 2px; padding-left: 0px; color: #4B4B4B;}")
        # self.setStyleSheet("QLineEdit {background-color: transparent; font-size: 14pt; margin-left: 0px; padding-left: 0px; color: #4B4B4B;}")
        self.setText(defaulttext)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if validator:
            self.setValidator(validator)
        # self.setFixedHeight(fields['height'])

    def focusOutEvent(self, event):
        QLineEdit.focusOutEvent(self, event)
        self.setCursorPosition(0)

class NoEditLine(QLabel):
    def __init__(self, parent=None, text=''):
        QLabel.__init__(self)
        self.setStyleSheet("QLabel {background-color: transparent; font-size: 13pt; border: none; margin-left: 0px; "
                           "padding-left: 0px; color: #4B4B4B;}")
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setText(text)

class UnitsLabel(QLabel):
    def __init__(self, parent=None, label=''):
        QLabel.__init__(self)
        self.setStyleSheet("QLabel {color: #979797; background-color: transparent; font-size: 11pt; border: none; "
                           "padding: 0px 0px 0px 0px;}")
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setContentsMargins(0, 2, 0, 0)
        self.setText(label)

class FilledButton(QPushButton):
    def __init__(self, parent=None, label='', colors=colors['red']):
        QPushButton.__init__(self)
        self.setStyleSheet("QPushButton {background-color: %s; border: 2px solid %s; border-radius: 3px; color: white;}"
                           "QPushButton:pressed {background-color: %s; border: none}" %
                           (colors[0], colors[0], colors[1]))
        self.setFixedWidth(buttons['width'])
        self.setFixedHeight(buttons['height'])
        self.setText(label)

class OutlineButton(QPushButton):
    def __init__(self, parent=None, label=''):
        QPushButton.__init__(self)
        self.setStyleSheet("QPushButton {background-color: white; border: 2px solid %s; color: %s; border-radius: 3px;}"
                           "QPushButton:pressed {background-color: %s; color: white;}" %
                           (colors['dark'][0], colors['dark'][0], colors['dark'][0]))
        self.setFixedWidth(buttons['width'])
        self.setFixedHeight(buttons['height'])
        self.setText(label)

class IconButton(QPushButton):
    def __init__(self, size=22, parent=None, icon=None, margin=(0,0,0,0), rotate=False, color_scheme=colors['highlight']):
        QPushButton.__init__(self)
        self.icon = icon
        self.rotate = rotate
        self.color = color_scheme
        # self.icon = qta.icon(icon, color=colors['highlight'][0], color_active=colors['highlight'][1])
        qicon = qta.icon(self.icon, color=self.color[0])
        self.setContentsMargins(0, 0, 0, 0)
        self.setIcon(qicon)
        self.setIconSize(QSize(size, size))
        self.setStyleSheet("QPushButton {background-color: transparent; border: none; margin: %spx %spx %spx %spx;}" % tuple(margin))
        # self.setFixedSize(size+2, size+2)

    def mousePressEvent(self, event):
        QPushButton.mousePressEvent(self, event)
        if self.rotate:
            qicon = qta.icon(self.icon, color=self.color[1], animation=qta.Spin(self))
        else:
            qicon = qta.icon(self.icon, color=self.color[1])
        self.setIcon(qicon)


    def mouseReleaseEvent(self, event):
        QPushButton.mouseReleaseEvent(self, event)
        qicon = qta.icon(self.icon, color=self.color[0])
        self.setIcon(qicon)


class RadioButtons(QWidget):
    def __init__(self, parent=None, radiolist=[]):
        QWidget.__init__(self)
        self.setStyleSheet("QWidget {background-color: transparent; border: none;}")
        self.setContentsMargins(0, 0, 0, 0)
        self.buttons = []
        for i, button in enumerate(radiolist):
            b = QRadioButton(button)
            b.setStyleSheet("QRadioButton {font-size: 11px; background-color: transparent; color: #7F7F7F; border-style: none; padding-top: 0px;}"
                            "QRadioButton:indicator:unchecked {background-color: #D8D8D8; border: 3px solid #D8D8D8; border-radius: 7px; width: 8px; height: 8px;}"
                            "QRadioButton:indicator:checked {background-color: %s; border: 3px solid #D8D8D8; border-radius: 7px; width: 8px; height: 8px;}" % colors['secondary'][0])
            # b.setFixedHeight(40)
            self.buttons.append(b)
        self.buttons[0].setChecked(True)
        self.radiogroup = QButtonGroup()

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        for i in range(len(self.buttons)):
            vbox.addWidget(self.buttons[i])
            self.radiogroup.addButton(self.buttons[i], i)
        # vbox.addStretch(1)

class ComboBox(QComboBox):
    def __init__(self, parent=None, itemlist=[], valueindex=1, width=None, margin=[0, 0, 0, 0]):
        QComboBox.__init__(self)
        self.setItemDelegate(QStyledItemDelegate(self))
        self.setStyleSheet("QComboBox {padding-left: 8px; background-color: white; border: 1px solid #A2A2A2; "
                           "border-radius: 3px; margin: %spx %spx %spx %spx;}"
                           "QComboBox:down-arrow {image: url(../static/icons/combo-down.png)}"
                           "QComboBox:drop-down:button {background-color: transparent; padding-right: 16px;}"
                           "QListView {background-color: white; border: 1px solid #A2A2A2; border-radius: 3px; outline: none;}"
                           "QListView:item {min-height: %spx;}"
                           "QListView:item:selected:text {border-style: none;}"
                           "QListView:item:selected {padding-left: 5px; background-color: %s; border-style: none;}"
                           "QListView:item:!selected {padding-left: 5px;}"
                           % (margin[0], margin[1], margin[2], margin[3], fields['height'], colors['highlight'][0]))
        #self.setItemIcon(qta.icon('ei.chevron-down', color=colors['highlight'][0], color_active=colors['highlight'][1]))
        if not width:
            width = fields['width']
        self.setFixedWidth(width)
        self.setFixedHeight(fields['height'])
        self.addItems(itemlist)
        self.setCurrentIndex(valueindex)

class EditLineWithUnits(QGroupBox):
    def __init__(self, unittext, edittext, parent=None, width=None, units=True, validator=None):
        QGroupBox.__init__(self)
        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.white)
        # self.setPalette(p)
        self.setStyleSheet("QGroupBox {background-color: white; border: 1px solid #A2A2A2; border-radius: 3px;}")
        self.setContentsMargins(0, 0, 0, 0)
        if not width:
            width = fields['width']
        self.setFixedWidth(width)
        self.setFixedHeight(fields['height'])
        self.qedit = EditLine(defaulttext=edittext, validator=validator)
        self.units = UnitsLabel(label=unittext)
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(8, 0, 8, 0)
        self.hbox.setSpacing(0)
        self.hbox.addWidget(self.qedit)
        if units:
            self.hbox.addWidget(self.units)
        else:
            self.qedit.setAlignment(Qt.AlignCenter)

class NoEditLineWithUnits(QGroupBox):
    def __init__(self, unittext, text, parent=None, width=None, units=True):
        QGroupBox.__init__(self)
        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), Qt.white)
        # self.setPalette(p)
        self.setStyleSheet("QGroupBox {background-color: white; border: none}")
        self.setContentsMargins(0, 0, 0, 0)
        if not width:
            width = fields['width']
        self.setFixedWidth(width)
        self.setFixedHeight(fields['height'])
        self.label = NoEditLine(text=text)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.units = UnitsLabel(label=unittext)
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(8, 0, 8, 0)
        self.hbox.addWidget(self.label)
        if units:
            self.hbox.addWidget(self.units)
        # else:
        #     self.qedit.setAlignment(Qt.AlignCenter)

class ButtonBox(QGroupBox):
    def __init__(self, label='', buttonlabel='', colors=None):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QGroupBox {background-color: transparent; border: none;}")
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0,0,0,0)
        if label:
            self.label = WidgetLabel(label=label)
            vbox.addWidget(self.label)
        if colors:
            self.button = FilledButton(label=buttonlabel, colors=colors)
        else:
            self.button = OutlineButton(label=buttonlabel)
        vbox.addWidget(self.button)
        # vbox.addStretch(1)

class ComboBoxGroup(QGroupBox):
    def __init__(self, parent=None, label='', itemlist=[], value=None, width=None, margin=[0, 0, 0, 0]):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QGroupBox {background-color: transparent; border: none;}")
        # self.setStyleSheet("QGroupBox {background-color: transparent; border: 1px solid #A2A2A2; border-radius: 3px; padding-left: 0px;}")
        self.label = WidgetLabel(label=label, margin=margin)
        valueindex = 1
        if value:
            valueindex = itemlist.index(value)
            if valueindex == -1:
                valueindex = 1
        self.combobox = ComboBox(valueindex=valueindex, itemlist=itemlist, width=width, margin=margin)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0,0,0,0)
        vbox.addWidget(self.label)
        vbox.addWidget(self.combobox)
        vbox.addStretch(1)

class EditLineGroup(QGroupBox):
    def __init__(self, parent=None, label='', unittext='', edittext='', width=None, units=True, validator=None):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QGroupBox {background-color: transparent; border: none;}")
        # self.setStyleSheet("QGroupBox {background-color: transparent; border: 1px solid #A2A2A2; border-radius: 3px; padding-left: 0px;}")
        self.label = WidgetLabel(label=label)
        self.edit = EditLineWithUnits(unittext=unittext, edittext=edittext, width=width, units=units, validator=validator)
        # self.edit.setStyleSheet("QWidget {background-color: white; border: 1px solid #A2A2A2; border-radius: 3px; padding-left: 0px;}")
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0,0,0,0)
        vbox.addWidget(self.label)
        vbox.addWidget(self.edit)
        vbox.addStretch(1)

class NoEditLineGroup(QGroupBox):
    def __init__(self, parent=None, grouplabel='', label=[], unittext='', text=[], width=[]):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        # self.setStyleSheet("QGroupBox {background-color: transparent; border: 1px;}")
        self.setStyleSheet("QGroupBox {background-color: transparent; border: 1px solid #A2A2A2; border-radius: 3px; padding-left: 0px;}")
        self.grouplabel = QLabel(grouplabel)
        self.grouplabel.setStyleSheet("QLabel {font-size: 14pt; font-weight: bold;}")
        self.grouplabel.setAlignment(Qt.AlignCenter)
        self.label = []
        self.field = []
        for i in range(len(label)):
            self.label.append(WidgetLabel(label=label[i]))
            self.field.append(NoEditLineWithUnits(unittext=unittext, text=text[i]))

        vbox = QVBoxLayout(self)
        # vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.grouplabel)
        for i in range(len(self.label)):
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.addWidget(self.label[i])
            hbox.addWidget(self.field[i])
            vbox.addLayout(hbox)

class RadioButtonsGroup(QGroupBox):
    def __init__(self, parent=None, label='', radiolist=[]):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QGroupBox {background-color: transparent; border: none;}")
        # self.setStyleSheet("QGroupBox {background-color: transparent; border: 1px solid #A2A2A2; border-radius: 3px; padding-left: 0px;}")
        self.label = WidgetLabel(label=label)
        self.buttons = RadioButtons(radiolist=radiolist)
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0,0,0,0)
        if label:
            vbox.addWidget(self.label)
        vbox.addWidget(self.buttons)
        vbox.addStretch(1)

class RowGroup(QGroupBox):
    def __init__(self, parent=None, step=0, steplist=['1', '2', '3', '4', '34'], volume='14.5', volumeunit='mL', rate='2',
                 rateunit='mL/min', delay='0.25', timeunit='min', color='#FAFAFA'):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QGroupBox {background-color: %s; border: 1px solid %s; border-radius: 3px;}" % (color, color))

        self.addButton = IconButton(icon='ei.plus', margin=[0, 0, 0, 0])
        self.stepGroup = ComboBox(valueindex=step, itemlist=steplist, width=60)
        self.volumeGroup = EditLineWithUnits(unittext=volumeunit, edittext=volume, validator=volumeValidator)
        self.rate1Group = EditLineWithUnits( unittext=rateunit, edittext=rate, validator=rateValidator, width=115)
        self.rate2Group = EditLineWithUnits( unittext=rateunit, edittext=rate, validator=rateValidator, width=115)
        self.delayGroup = EditLineWithUnits( unittext=timeunit, edittext=delay, validator=delayValidator, width=79)
        self.movementGroup = RadioButtons(radiolist=['Infuse', 'Withdraw'])
        self.trashButton = IconButton(icon='ei.trash', margin=[0, 0, 0, 0])

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.addButton)
        hbox.addWidget(self.stepGroup)
        hbox.addSpacing(6)
        hbox.addWidget(self.volumeGroup)
        hbox.addSpacing(6)
        hbox.addWidget(self.rate1Group)
        hbox.addSpacing(6)
        hbox.addWidget(self.rate2Group)
        hbox.addSpacing(6)
        hbox.addWidget(self.delayGroup)
        hbox.addSpacing(6)
        hbox.addWidget(self.movementGroup)
        hbox.addSpacing(6)
        hbox.addWidget(self.trashButton)

class StepTable(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.setDragDropOverwriteMode(False)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setStyleSheet("QTableWidget {margin: 0px 0px 0px 0px;}")

# class StepList(QListWidget):
#     def __init__(self, parent=None):
#         QListWidget.__init__(self, parent)
#         self.setDragDropMode(QAbstractItemView.InternalMove)
#         self.setSelectionMode(QAbstractItemView.ExtendedSelection)
#         self.setAcceptDrops(True)
#         self.setDropIndicatorShown(True)
#
#     def dropEvent(self, event):
#         # print("Dropping")
#         QListWidget.dropEvent(self, event)




    # def dropEvent(self, event):
    #     if event.source() == self:
    #         rows = set([mi.row() for mi in self.selectedIndexes()])
    #         targetRow = self.indexAt(event.pos()).row()
    #         rows.discard(targetRow)
    #         rows = sorted(rows)
    #         if not rows:
    #             return
    #         if targetRow == -1:
    #             targetRow = self.rowCount()
    #         for _ in range(len(rows)):
    #             self.insertRow(targetRow)
    #         rowMapping = dict()  # Src row to target row.
    #         for idx, row in enumerate(rows):
    #             if row < targetRow:
    #                 rowMapping[row] = targetRow + idx
    #             else:
    #                 rowMapping[row + len(rows)] = targetRow + idx
    #         colCount = self.columnCount()
    #         for srcRow, tgtRow in sorted(rowMapping.items()):
    #             for col in range(0, colCount):
    #                 self.setItem(tgtRow, col, self.takeItem(srcRow, col))
    #         for row in reversed(sorted(rowMapping.keys())):
    #             self.removeRow(row)
    #         event.accept()
    #         return

class GuiGroup(QGroupBox):
    def __init__(self, hbar_top=None, hbar_bottom=None, title='', groupbox=[]):
        QGroupBox.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("QGroupBox {background-color: transparent; border: none;}")
        vbox = QVBoxLayout(self)
        if hbar_top:
            self.hbar_top = QFrame()
            self.hbar_top.setFrameShape(QFrame.HLine)
            vbox.addWidget(self.hbar_top)
        if title:
            self.title = Header1Label(label=title)
            vbox.addWidget(self.title)
        if groupbox:
            self.groupbox = groupbox
            for i in self.groupbox:
                try:
                    vbox.addWidget(i)
                except:
                    vbox.addLayout(i)
        if hbar_bottom:
            self.hbar_bottom = QFrame()
            self.hbar_bottom.setFrameShape(QFrame.HLine)
            vbox.addWidget(self.hbar_bottom)


# class TableGroup(QGroupBox):
#     def


class Example(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        start = FilledButton(label='START', colors=colors['green'])
        stop = FilledButton(label="STOP", colors=colors['red'])
        pause = FilledButton(label="PAUSE", colors=colors['orange'])
        reset = OutlineButton(label="RESET CONNECTION")
        send = FilledButton(label="SEND STEPS", colors=colors['highlight'])
        combo = ComboBoxGroup(label="Flow Rate Units:", itemlist=['mL/min', 'mL/hr', 'μL/min', 'μL/hr'])
        editable = EditLineGroup(label='Transfer Volume:', unittext='mL', edittext='14.5')
        editable2 = EditLineGroup(label='Rate:', unittext='mL/min', edittext='14.5')
        barbutton = IconButton(icon='fa.bars')
        headerlabel = Header1Label(label='Step Parameters')
        header2label = Header2Label(label='Step 1')
        trashbutton = IconButton(icon='fa.trash')
        radiobuttons = RadioButtonsGroup(label='Movement Mode:', radiolist=['Infuse', 'Withdraw'])

        row1 = RowGroup(steplabel='Step 1', volume='14.5', volumeunit='mL', rate='2', rateunit='mL/min', color='#FAFAFA')
        row2 = RowGroup(steplabel='Step 2', volume='12.0', volumeunit='μL', rate='2', rateunit='μL/hr', color='#EFEFEF')

        vbox = QVBoxLayout(self)
        vbox.addWidget(headerlabel)
        vbox.addWidget(header2label)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(stop)
        hbox1.addWidget(pause)
        hbox1.addWidget(start)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(reset)
        hbox2.addWidget(send)
        vbox.addLayout(hbox2)

        # vbox.addWidget(combo)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(combo)
        hbox3.addWidget(editable)
        hbox3.addWidget(editable2)
        hbox3.addWidget(radiobuttons)
        vbox.addLayout(hbox3)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(barbutton)
        hbox4.addWidget(trashbutton)
        vbox.addLayout(hbox4)

        vbox.addWidget(row1)
        vbox.addWidget(row2)


class Example2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setMinimumWidth(750)
        self.setMinimumHeight(300)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        self.table = StepTable()
        self.table.setRowCount(3)
        self.table.setColumnCount(1)
        # self.table.resizeColumnsToContents()
        self.table.verticalHeader().setDefaultSectionSize(100)
        self.table.setColumnWidth(0, 100)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()

        row1 = RowGroup(steplabel='Step 1', volume='14.5', volumeunit='mL', rate='2', rateunit='mL/min',color='#FAFAFA')
        row2 = RowGroup(steplabel='Step 2', volume='12.0', volumeunit='μL', rate='3.42', rateunit='μL/hr', color='#EFEFEF')
        row3 = RowGroup(steplabel='Step 3', volume='14.5', volumeunit='mL', rate='10', rateunit='mL/hr', color='#FAFAFA')
        self.table.setCellWidget(0, 0, row1)
        self.table.setCellWidget(1, 0, row2)
        self.table.setCellWidget(2, 0, row3)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.table)


class Example3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        # self.setFixedWidth(1175)



        hbox1 = QHBoxLayout(self)
        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)

        # hbox7 = QHBoxLayout()
        #
        # hbox7.addStretch(1)
        # hbox7.addWidget(self.loadButton)
        # hbox7.addWidget(self.saveButton)
        # hbox7.addStretch(1)
        # vbox1.addLayout(hbox7)

        # ## Pump Mode
        # self.pumpmode = RadioButtonsGroup(radiolist=['Basic', 'Multi-Step'])
        # self.pumpmodegroup = GuiGroup(hbar_bottom=True, title='Pump Mode', groupbox=[self.pumpmode])
        # vbox1.addWidget(self.pumpmodegroup)

        ## Settings
        hbox2 = QHBoxLayout()
        self.rateunits = ComboBoxGroup(label='Rate Units', itemlist=['mL/min', 'mL/hr', 'μL/min', 'μL/hr'], value='mL/hr', width=85)
        self.syringeid = EditLineGroup(label='Syringe ID', unittext='mm', edittext='14.5', validator=idValidator)
        self.syringevol = EditLineGroup(label='Syringe Volume', unittext='mL', edittext='30', validator=volumeValidator)
        self.syringebtn = ButtonBox(label=' ', buttonlabel='SYRINGES', colors=colors['highlight'])
        self.loadButton = IconButton(icon='ei.folder-open', size=32, margin=[22, 0, 0, 0])
        self.saveButton = IconButton(icon='ei.hdd', size=32, margin=[22, 0, 0 , 0])
        self.pumpmodel = ComboBoxGroup(label='Pump Model',
                                       itemlist=['Fusion 100', 'Fusion 200', 'Fusion 400', 'Nexus 3000', 'Nexus 6000'],
                                       width=115)


        hbox2.addWidget(self.syringeid)
        hbox2.addWidget(self.syringevol)
        hbox2.addWidget(self.syringebtn)
        # hbox2.addStretch(1)
        hbox2.addSpacing(10)
        hbox2.addWidget(self.rateunits)
        hbox2.addWidget(self.pumpmodel)
        # hbox2.addStretch(1)
        hbox2.addWidget(self.loadButton)
        hbox2.addWidget(self.saveButton)
        # hbox2.addWidget(self.terminalButton)
        # hbox2.addStretch(1)

        self.settingsgroup = GuiGroup(hbar_bottom=False, title='Settings', groupbox=[hbox2])
        vbox1.addWidget(self.settingsgroup)

        ## Step Parameters
        self.table = StepTable()
        self.table.setContentsMargins(0, 0, 0, 0)
        self.table.setRowCount(5)
        self.table.setColumnCount(1)
        self.table.setFixedWidth(680)
        # self.table.resizeColumnsToContents()
        self.table.verticalHeader().setDefaultSectionSize(53)
        self.table.setFixedHeight(214)
        # self.table.setColumnWidth(0, 100)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()

        row1 = RowGroup(step=0, volume='14.5', volumeunit='mL', rate='2', rateunit='mL/min', delay='1',
                        color='#FAFAFA')
        row2 = RowGroup(step=1, volume='12.0', volumeunit='μL', rate='3.42', rateunit='μL/hr', delay='0.25',
                        color='#EFEFEF')
        row3 = RowGroup(step=2, volume='14.5', volumeunit='mL', rate='10', rateunit='mL/hr', delay='0.5',
                        color='#FAFAFA')
        row4 = RowGroup(step=3, volume='14.5', volumeunit='mL', rate='10', rateunit='mL/hr', delay='0.75',
                        color='#FAFAFA')
        row5 = RowGroup(step=4, volume='14.5', volumeunit='mL', rate='10', rateunit='mL/hr', delay='0.75',
                        color='#FAFAFA')
        self.table.setCellWidget(0, 0, row1)
        self.table.setCellWidget(1, 0, row2)
        self.table.setCellWidget(2, 0, row3)
        self.table.setCellWidget(3, 0, row4)
        self.table.setCellWidget(4, 0, row5)


        self.stepLbl = WidgetLabel(label='Step', width=60)
        self.volumeLbl = WidgetLabel(label='Target Volume', width=105)
        self.rate1Lbl = WidgetLabel(label='Flow Rate 1', width=115)
        self.rate2Lbl = WidgetLabel(label='Flow Rate 2', width=115)
        self.delayLbl = WidgetLabel(label='Start Delay', width=79)
        self.moveLbl = WidgetLabel(label='Direction', width=70)

        hbox7 = QHBoxLayout()
        hbox7.setContentsMargins(49, 0, 0, 0)
        # hbox7.addStretch(1)
        hbox7.addWidget(self.stepLbl)
        hbox7.addSpacing(6)
        hbox7.addWidget(self.volumeLbl)
        hbox7.addSpacing(6)
        hbox7.addWidget(self.rate1Lbl)
        hbox7.addSpacing(6)
        hbox7.addWidget(self.rate2Lbl)
        hbox7.addSpacing(6)
        hbox7.addWidget(self.delayLbl)
        hbox7.addSpacing(6)
        # hbox7.addWidget(self.moveLbl)
        hbox7.addStretch(1)

        tblvbox = QVBoxLayout()
        tblvbox.setSpacing(0)
        tblvbox.setContentsMargins(0, 0, 0, 0)
        tblvbox.addLayout(hbox7)
        tblvbox.addSpacing(2)
        tblvbox.addWidget(self.table)

        self.tablegroup = GuiGroup(title='Step Parameters', groupbox=[tblvbox])
        vbox1.addWidget(self.tablegroup)

        ## Step Buttons
        self.addButton = ButtonBox(label='', buttonlabel='ADD STEP')
        self.resetButton = ButtonBox(label='', buttonlabel='RESET STEPS')

        self.sendButton = ButtonBox(label='', buttonlabel='SEND STEPS', colors=colors['highlight'])
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.addButton)
        hbox3.addWidget(self.resetButton)

        hbox3.addWidget(self.sendButton)
        hbox3.addStretch(1)
        vbox1.addLayout(hbox3)
        vbox1.addStretch(1)

        vbox2 = QVBoxLayout()


        # Logo
        self.logoLabel = QLabel()
        self.logo = QPixmap('../static/logo-with-tagline@450px.png')
        self.logoLabel.setPixmap(self.logo)
        self.logoLabel.setAlignment(Qt.AlignCenter)
        vbox2.addWidget(self.logoLabel)

        vbox2.addStretch(1)

        # self.pumpmodel = ComboBoxGroup(label='Pump Model', itemlist=['Fusion 100', 'Fusion 200', 'Fusion 400', 'Nexus 3000', 'Nexus 6000'], width=124, margin=[0, 0, 0, 9])
        # vbox2.addSpacing(6)
        # vbox2.addWidget(self.pumpmodel)


        ## Data Link
        hbox4 = QHBoxLayout()
        self.port = ComboBoxGroup(label='Serial Port', itemlist=['COM1', 'COM2', 'ABCDEFGH'], width=115)
        self.baud = ComboBoxGroup(label='Baud Rate', itemlist=['9600', '38400'], width=85)
        self.resetbox = ButtonBox(label="<font color='red'>Connection Lost</font>", buttonlabel='DISCONNECT')
        # self.openterm = ButtonBox(label=' ', buttonlabel='REFRESH', colors=colors['highlight'])
        self.terminalButton = IconButton(icon='ei.screen', size=32, margin=[22, 0, 0, 0])
        # self.terminalButton.setDisabled(True)
        self.refreshButton = IconButton(icon='ei.refresh', size=32, margin=[22, 0, 0, 0], rotate=True)
        hbox4.addWidget(self.port)
        hbox4.addWidget(self.baud)
        hbox4.addWidget(self.resetbox)
        hbox4.addStretch(1)
        hbox4.addWidget(self.refreshButton)
        hbox4.addWidget(self.terminalButton)


        self.datalinkgroup = GuiGroup(hbar_bottom=False, title='Data Link', groupbox=[hbox4])
        vbox2.addWidget(self.datalinkgroup)

        ## Status

        # hbox5 = QHBoxLayout()
        self.timestatus = NoEditLineGroup(grouplabel='Time', label=['Elapsed:', 'Total:'], text=['01:55', '02:00'], unittext='mm:ss')
        self.volumestatus = NoEditLineGroup(grouplabel='Volume', label=['Transferred:', 'Total:'], text=['2', '3'], unittext='mL')
        self.status = Header2Label(label="Running (Step 20)", color='green')
        self.status.setAlignment(Qt.AlignCenter)
        # self.timeelapsed = NoEditLineGroup(label='Time Elapsed:', text='00:05', unittext='hh:mm')
        # self.timeremain = NoEditLineGroup(label='Time Remaining:', text='01:55', unittext='hh:mm')
        # self.volumetrans = NoEditLineGroup(label='Volume Transferred:', text='2', unittext='mL')
        # self.volumeremain = NoEditLineGroup(label='Volume Remaining:', text='3', unittext='mL')
        # hbox5.addWidget(self.timeremain)
        # hbox5.addWidget(self.timeelapsed)
        # hbox5.addWidget(self.volumeremain)
        # hbox5.addWidget(self.volumetrans)
        # hbox5.addStretch(1)

        gridbox = QGridLayout()
        gridbox.addWidget(self.status, 0, 0, 1, 2)
        gridbox.addWidget(self.timestatus, 1, 0)
        gridbox.addWidget(self.volumestatus, 1, 1)
        # gridbox.addWidget(self.timeremain, 0, 0)
        # gridbox.addWidget(self.timeelapsed, 1, 0)
        # gridbox.addWidget(self.volumeremain, 0, 1)
        # gridbox.addWidget(self.volumetrans, 1, 1)
        # self.status = NoEditLineGroup(label='', text='Running (Step 20)', unittext='', width=498)

        # vbox2.addWidget(self.statusgroup)

        ## Controls
        self.stopbutton = ButtonBox(label='', buttonlabel='STOP', colors=colors['red'])
        self.pausebutton = ButtonBox(label='', buttonlabel='PAUSE', colors=colors['orange'])
        self.startbutton = ButtonBox(label='', buttonlabel='START', colors=colors['green'])
        hbox6 = QHBoxLayout()
        hbox6.addStretch(1)
        hbox6.addWidget(self.stopbutton)
        hbox6.addWidget(self.pausebutton)
        hbox6.addWidget(self.startbutton)
        hbox6.addStretch(1)
        # self.controlgroup = GuiGroup(title='', groupbox=[hbox6])
        self.statusgroup = GuiGroup(hbar_bottom=False, title='Pump Status & Control', groupbox=[gridbox, hbox6])
        vbox2.addWidget(self.statusgroup)




        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("color: %s;" % colors['highlight'][1])
        hbox1.addWidget(separator)
        hbox1.addLayout(vbox1)


class Example4(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        # self.setFixedWidth(1175)

        hbox1 = QHBoxLayout(self)
        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)

        # hbox7 = QHBoxLayout()
        #
        # hbox7.addStretch(1)
        # hbox7.addWidget(self.loadButton)
        # hbox7.addWidget(self.saveButton)
        # hbox7.addStretch(1)
        # vbox1.addLayout(hbox7)

        # ## Pump Mode
        # self.pumpmode = RadioButtonsGroup(radiolist=['Basic', 'Multi-Step'])
        # self.pumpmodegroup = GuiGroup(hbar_bottom=True, title='Pump Mode', groupbox=[self.pumpmode])
        # vbox1.addWidget(self.pumpmodegroup)

        ## Settings
        hbox2 = QHBoxLayout()
        self.rateunits = ComboBoxGroup(label='Flow-Rate Units', itemlist=['mL/min', 'mL/hr', 'μL/min', 'μL/hr'], value='mL/hr')
        self.syringeid = EditLineGroup(label='Syringe ID', unittext='mm', edittext='14.5')
        self.syringevol = EditLineGroup(label='Syringe Volume', unittext='mL', edittext='30')
        self.syringebtn = ButtonBox(label=' ', buttonlabel='SYRINGES', colors=colors['highlight'])
        self.loadButton = IconButton(icon='ei.folder-open', size=32, margin=[22, 0, 0, 0])
        self.saveButton = IconButton(icon='ei.hdd', size=32, margin=[22, 0, 0 , 0])


        hbox2.addWidget(self.syringeid)
        hbox2.addWidget(self.syringevol)
        hbox2.addWidget(self.syringebtn)
        hbox2.addStretch(1)
        hbox2.addWidget(self.rateunits)
        hbox2.addStretch(1)
        hbox2.addWidget(self.loadButton)
        hbox2.addWidget(self.saveButton)
        # hbox2.addWidget(self.terminalButton)
        # hbox2.addStretch(1)

        self.settingsgroup = GuiGroup(hbar_bottom=False, title='Settings', groupbox=[hbox2])
        vbox1.addWidget(self.settingsgroup)

        ## Step Parameters
        self.table = StepTable()
        self.table.setRowCount(4)
        self.table.setColumnCount(1)
        self.table.setFixedWidth(685)
        # self.table.resizeColumnsToContents()
        self.table.verticalHeader().setDefaultSectionSize(66)
        self.table.setFixedHeight(212)
        # self.table.setColumnWidth(0, 100)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()

        row1 = RowGroup(step='1', volume='14.5', volumeunit='mL', rate='2', rateunit='mL/min', delay='1',
                        color='#FAFAFA')
        row2 = RowGroup(step='2', volume='12.0', volumeunit='μL', rate='3.42', rateunit='μL/hr', delay='0.25',
                        color='#EFEFEF')
        row3 = RowGroup(step='3', volume='14.5', volumeunit='mL', rate='10', rateunit='mL/hr', delay='0.5',
                        color='#FAFAFA')
        row4 = RowGroup(step='34', volume='14.5', volumeunit='mL', rate='10', rateunit='mL/hr', delay='0.75',
                        color='#FAFAFA')
        self.table.setCellWidget(0, 0, row1)
        self.table.setCellWidget(1, 0, row2)
        self.table.setCellWidget(2, 0, row3)
        self.table.setCellWidget(3, 0, row4)
        self.tablegroup = GuiGroup(title='Step Parameters', groupbox=[self.table])
        vbox1.addWidget(self.tablegroup)

        ## Step Buttons
        self.addButton = ButtonBox(label='', buttonlabel='ADD STEP')
        self.resetButton = ButtonBox(label='', buttonlabel='RESET STEPS')

        self.sendButton = ButtonBox(label='', buttonlabel='SEND STEPS', colors=colors['highlight'])
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.addButton)
        hbox3.addWidget(self.resetButton)

        hbox3.addWidget(self.sendButton)
        hbox3.addStretch(1)
        vbox1.addLayout(hbox3)
        vbox1.addStretch(1)

        vbox2 = QVBoxLayout()


        # Logo
        self.logoLabel = QLabel()
        self.logo = QPixmap('../static/logo-with-tagline@450px.png')
        self.logoLabel.setPixmap(self.logo)
        self.logoLabel.setAlignment(Qt.AlignCenter)
        vbox2.addWidget(self.logoLabel)

        vbox2.addStretch(1)

        ## Data Link
        hbox4 = QHBoxLayout()
        self.port = ComboBoxGroup(label='Serial Port:', itemlist=['COM1', 'COM2', 'COM3'])
        self.baud = ComboBoxGroup(label='Baud Rate:', itemlist=['9600', '38400'])
        self.resetbox = ButtonBox(label="<font color='green'>Connected</font>", buttonlabel='DISCONNECT')
        # self.openterm = ButtonBox(label=' ', buttonlabel='REFRESH', colors=colors['highlight'])
        self.terminalButton = IconButton(icon='ei.screen', size=32, margin=[22, 0, 0, 0])
        self.refreshButton = IconButton(icon='ei.refresh', size=32, margin=[22, 0, 0, 0])
        hbox4.addWidget(self.port)
        hbox4.addWidget(self.baud)
        hbox4.addWidget(self.resetbox)
        hbox4.addStretch(1)
        hbox4.addWidget(self.terminalButton)
        hbox4.addWidget(self.refreshButton)

        self.datalinkgroup = GuiGroup(hbar_bottom=False, title='Data Link', groupbox=[hbox4])
        vbox2.addWidget(self.datalinkgroup)

        ## Status

        # hbox5 = QHBoxLayout()
        self.timestatus = NoEditLineGroup(grouplabel='Time', label=['Elapsed:', 'Total:'], text=['01:55', '02:00'], unittext='mm:ss')
        self.volumestatus = NoEditLineGroup(grouplabel='Volume', label=['Transferred:', 'Total:'], text=['2', '3'], unittext='mL')
        self.status = Header2Label(label="Running (Step 20)", color='green')
        self.status.setAlignment(Qt.AlignCenter)
        # self.timeelapsed = NoEditLineGroup(label='Time Elapsed:', text='00:05', unittext='hh:mm')
        # self.timeremain = NoEditLineGroup(label='Time Remaining:', text='01:55', unittext='hh:mm')
        # self.volumetrans = NoEditLineGroup(label='Volume Transferred:', text='2', unittext='mL')
        # self.volumeremain = NoEditLineGroup(label='Volume Remaining:', text='3', unittext='mL')
        # hbox5.addWidget(self.timeremain)
        # hbox5.addWidget(self.timeelapsed)
        # hbox5.addWidget(self.volumeremain)
        # hbox5.addWidget(self.volumetrans)
        # hbox5.addStretch(1)

        gridbox = QGridLayout()
        gridbox.addWidget(self.status, 0, 0, 1, 2)
        gridbox.addWidget(self.timestatus, 1, 0)
        gridbox.addWidget(self.volumestatus, 1, 1)
        # gridbox.addWidget(self.timeremain, 0, 0)
        # gridbox.addWidget(self.timeelapsed, 1, 0)
        # gridbox.addWidget(self.volumeremain, 0, 1)
        # gridbox.addWidget(self.volumetrans, 1, 1)
        # self.status = NoEditLineGroup(label='', text='Running (Step 20)', unittext='', width=498)

        # vbox2.addWidget(self.statusgroup)

        ## Controls
        self.stopbutton = ButtonBox(label='', buttonlabel='STOP', colors=colors['red'])
        self.pausebutton = ButtonBox(label='', buttonlabel='PAUSE', colors=colors['orange'])
        self.startbutton = ButtonBox(label='', buttonlabel='START', colors=colors['green'])
        hbox6 = QHBoxLayout()
        hbox6.addStretch(1)
        hbox6.addWidget(self.stopbutton)
        hbox6.addWidget(self.pausebutton)
        hbox6.addWidget(self.startbutton)
        hbox6.addStretch(1)
        # self.controlgroup = GuiGroup(title='', groupbox=[hbox6])
        self.statusgroup = GuiGroup(hbar_bottom=False, title='Pump Status & Control', groupbox=[gridbox, hbox6])
        vbox2.addWidget(self.statusgroup)




        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("color: %s;" % colors['highlight'][1])
        hbox1.addWidget(separator)
        hbox1.addLayout(vbox1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # app.setStyle('Fusion')
    app.setStyle(QStyleFactory.create('fusion'))
    ex = Example3()
    ex.show()
    sys.exit(app.exec_())