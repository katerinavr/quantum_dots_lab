import PyQt5.QtWidgets as QtW
import PyQt5.QtGui as QtG
import PyQt5.QtCore as QtC

import sys
import qtawesome as qta

colors = {'main':['#154C73', '#154C73'], 'dark':['#103A59', '#103A59'], 'secondary':['#195C8B', '#195C8B'],
          'highlight': ['#227DBF', '#195C8B'], 'orange':['#E85B23', '#C44614'], 'green':['#65A219', '#497612'],
          'red':['#D03D39', '#AD2D29']}

buttons = {'width':110, 'height':35}
fields = {'width':105, 'height':35}

class CLabel(QtW.QLabel):
    def __init__(self, parent=None, label='', alignment='left', margin=(0, 0, 0, 0), padding=(0, 0, 0, 0),
                 color='#4B4B4B', bcolor='transparent', fontsize='24', fontweight='normal', debug=False):
        QtW.QLabel.__init__(self, parent)

        styleparams = [fontsize] + [fontweight] + [color] + [bcolor] + list(margin) + list(padding) +['none']

        if debug:
            styleparams[-1] = '1px solid red'

        self.setStyleSheet("QLabel {font-size: %spt; font-weight: %s; color: %s; background-color: %s;"
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx; border: %s;}"
                           % tuple(styleparams))
        self.setText(label)
        if alignment == 'left':
            self.setAlignment(QtC.Qt.AlignLeft | QtC.Qt.AlignVCenter)
        elif alignment == 'right':
            self.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignVCenter)
        elif alignment == 'center':
            self.setAlignment(QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter)

class Header1Label(CLabel):
    def __init__(self, parent=None, **kwargs):
        CLabel.__init__(self, parent, **kwargs)

class Header2Label(CLabel):
    def __init__(self, parent=None, color='black', fontsize='16', fontweight='bold', **kwargs):
        CLabel.__init__(self, parent, color=color, fontsize=fontsize, fontweight=fontweight, **kwargs)

class WidgetLabel(CLabel):
    def __init__(self, parent=None, fontsize='12', fontweight='bold', **kwargs):
        CLabel.__init__(self, parent, fontsize=fontsize, fontweight=fontweight, **kwargs)

class UnitsLabel(CLabel):
    def __init__(self, parent=None, alignment='right', color='#979797', fontsize='11', fontweight='normal', **kwargs):
        CLabel.__init__(self, parent, alignment=alignment, color=color, fontsize=fontsize, fontweight=fontweight, **kwargs)

class ValueDisplay(CLabel):
    def __init__(self, parent=None, fontsize='13', **kwargs):
        CLabel.__init__(self, parent, fontsize=fontsize, **kwargs)



class CLineEdit(QtW.QLineEdit):
    def __init__(self, parent=None, defaulttext='', validator=None, alignment='right',
                 margin=(0, 0, 0, 0), padding=(0, 0, 0, 0), color='#4B4B4B', bcolor='transparent', fontsize='13',
                 fontweight='normal', debug=False):
        QtW.QLineEdit.__init__(self, parent)

        styleparams = [fontsize] + [fontweight] + [color] + [bcolor] + list(margin) + list(padding) + ['none']

        if debug:
            styleparams[-1] = '1px solid black'

        self.setStyleSheet("QLineEdit {font-size: %spt; font-weight: %s; color: %s; background-color: %s;"
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx; border: %s;}"
                           % tuple(styleparams))

        self.setText(defaulttext)
        if alignment == 'left':
            self.setAlignment(QtC.Qt.AlignLeft | QtC.Qt.AlignVCenter)
        elif alignment == 'right':
            self.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignVCenter)
        elif alignment == 'center':
            self.setAlignment(QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter)

        if validator:
            self.setValidator(validator)

    def focusOutEvent(self, event):
        QtW.QLineEdit.focusOutEvent(self, event)
        self.setCursorPosition(0)



class CPushButton(QtW.QPushButton):
    def __init__(self, parent=None, label='', uppercase=True, color='white', press_color='white', bcolor=colors['red'][0],
                 press_bcolor=colors['red'][1], borderwidth='2', borderstyle='solid', bordercolor=colors['red'][0],
                 press_bordercolor=colors['red'][1], borderradius='3', margin=(0, 0, 0, 0),
                 padding=(0, 0, 0, 0), fontsize='13', fontweight='normal', width=buttons['width'],
                 height=buttons['height'], color_scheme=None):
        QtW.QPushButton.__init__(self, parent)


        if color_scheme:
            bcolor = color_scheme[0]
            bordercolor = color_scheme[0]
            press_bcolor = color_scheme[1]
            press_bordercolor = color_scheme[1]

        styleparams = [fontsize] + [fontweight] + [color] + [bcolor] + [borderwidth] + [borderstyle] + [bordercolor] + \
                      [borderradius] + list(margin) + list(padding) + [press_bcolor] + [press_color] + [press_bordercolor]

        self.setStyleSheet("QPushButton {font-size: %spx; font-weight: %s; color: %s; background-color: %s; "
                           "border: %spx %s %s; border-radius: %spx; margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
                           "QPushButton:pressed {background-color: %s; color: %s; border-color: %s;}"
                           "QToolTip {background-color: #103B59; border: 2px solid #103B59; border-radius: 3px; "
                           "font-size: 13px; color: white; padding: 3px 3px 3px 3px;}"
                           % tuple(styleparams))

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        if uppercase:
            self.setText(label.upper())
        else:
            self.setText(label)

class OutlineButton(CPushButton):
    def __init__(self, parent=None, color=colors['dark'][0],
                 bcolor='white', press_bcolor=colors['dark'][0], bordercolor=colors['dark'][0],
                 press_bordercolor=colors['dark'][1], **kwargs):
        CPushButton.__init__(self, parent, color=color, bcolor=bcolor, bordercolor=bordercolor, press_bcolor=press_bcolor,
                             press_bordercolor=press_bordercolor, **kwargs)


class IconButton(QtW.QPushButton):
    def __init__(self, iconname, parent=None, rotate=False, iconsize=32, bcolor='transparent',
                 iconcolor=colors['highlight'][0], press_iconcolor=colors['highlight'][1], borderwidth='0',
                 borderstyle='solid', borderradius='3', bordercolor='black', press_bcolor='transparent',
                 press_bordercolor='black', margin=(0, 0, 0, 0), padding=(0, 0, 0, 0),
                 width=buttons['height'], height=buttons['height'], debug=False):
        QtW.QPushButton.__init__(self, parent)

        styleparams = [bcolor] + [borderwidth] + [borderstyle] + [bordercolor] + [borderradius] + \
                      list(margin) + list(padding) + [press_bcolor] + [borderwidth] + [borderstyle] + \
                      [press_bordercolor]

        if debug:
            styleparams[1] = '2'

        self.setStyleSheet("QPushButton {background-color: %s; border: %spx %s %s; border-radius: %spx;"
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
                           "QPushButton:pressed {background-color: %s; border: %spx %s %s;}"
                           % tuple(styleparams))

        self.iconname = iconname
        self.rotate = rotate
        self.iconcolor = iconcolor
        self.press_iconcolor = press_iconcolor
        if self.rotate:
            icon = qta.icon(self.iconname, scale_factor=0.8, color=self.iconcolor)
        else:
            icon = qta.icon(self.iconname, scale_factor=1.0, color=self.iconcolor)
        self.setIcon(icon)
        self.setIconSize(QtC.QSize(iconsize, iconsize))
        self.setFixedHeight(height)
        self.setFixedWidth(width)

    def mousePressEvent(self, event):
        QtW.QPushButton.mousePressEvent(self, event)
        if self.rotate:
            icon = qta.icon(self.iconname, scale_factor=0.8, color=self.press_iconcolor, animation=qta.Spin(self))
        else:
            icon = qta.icon(self.iconname, scale_factor=1.0, color=self.press_iconcolor)
        self.setIcon(icon)

    def mouseReleaseEvent(self, event):
        QtW.QPushButton.mouseReleaseEvent(self, event)
        if self.rotate:
            icon = qta.icon(self.iconname, scale_factor=0.8, color=self.iconcolor)
        else:
            icon = qta.icon(self.iconname, scale_factor=1.0, color=self.iconcolor)
        self.setIcon(icon)

class CRadioButtons(QtW.QWidget):
    def __init__(self, parent=None, radiolist=[], color='#7F7F7F', bcolor='transparent', borderwidth='0',
                 borderstyle='solid', bordercolor='black', borderradius='3', margin=(0, 0, 0, 0), padding=(0, 0, 0, 0),
                 fontsize='11', fontweight='normal', btncolor=colors['secondary'][0], btnsize='8'):
        QtW.QWidget.__init__(self, parent)

        stylesheet = [bcolor] + [borderwidth] + [borderstyle] + [bordercolor] + [borderradius] + list(margin) + \
                     list(padding)
        self.setStyleSheet("QWidget {background-color: %s; border: %spx %s %s; border-radius: %s; "
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
                           % tuple(stylesheet))
        self.buttons = []

        btnstylesheet = [fontsize] + [bcolor] + [color] + [str(int(btnsize)-1)] + [btnsize] + [btnsize] + [btncolor] + \
                        [str(int(btnsize)-1)] + [btnsize] + [btnsize]

        for i, button in enumerate(radiolist):
            btn = QtW.QRadioButton(button)
            btn.setStyleSheet("QRadioButton {font-size: %spx; background-color: %s; color: %s; padding: 0px; margin: 0px;}"
                              "QRadioButton:indicator:unchecked {background-color: #D8D8D8; border: 3px solid #D8D8D8; "
                              "border-radius: %spx; width: %spx; height: %spx;}"
                              "QRadioButton:indicator:checked {background-color: %s; border: 3px solid #D8D8D8; "
                              "border-radius: %spx; width: %spx; height: %spx;}"
                              % tuple(btnstylesheet))
            self.buttons.append(btn)
        self.buttons[0].setChecked(True)
        self.radiogroup = QtW.QButtonGroup()

        vbox = QtW.QVBoxLayout(self)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        for i in range(len(self.buttons)):
            vbox.addSpacing(6)
            vbox.addWidget(self.buttons[i])
            self.radiogroup.addButton(self.buttons[i], i)

class CComboBox(QtW.QComboBox):
    def __init__(self, parent=None, itemlist=[], currentindex=0, width=fields['width'], height=fields['height'],
                 margin=(0, 0, 0, 0), padding=(0, 0, 0, 8), selectcolor=colors['highlight'][0]):
        QtW.QComboBox.__init__(self, parent)
        self.setItemDelegate(QtW.QStyledItemDelegate(self))

        stylesheet = list(margin) + list(padding) + [height] + [selectcolor]

        self.setStyleSheet("QComboBox {background-color: white; border: 1px solid #A2A2A2;"
                           "border-radius: 3px; margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
                           "QComboBox:down-arrow {image: url(./static/icons/combo-down.png)}"
                           "QComboBox:drop-down:button {background-color: transparent; padding-right: 16px;}"
                           "QListView {background-color: white; border: 1px solid #A2A2A2; border-radius: 3px; outline: none;}"
                           "QListView:item {min-height: %spx;}"
                           "QListView:item:selected {padding-left: 5px; background-color: %s; border-style: none;}"
                           "QListView:item:!selected {padding-left: 5px;}"
                           "QListView:item:selected:text {border-style: none;}"
                           % tuple(stylesheet))
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.addItems(itemlist)
        self.setCurrentIndex(currentindex)

class LineEditwLblGroup(QtW.QGroupBox):
    def __init__(self, parent=None, width=fields['width'], height=fields['height'], margin=(0, 0, 0, 0),
                 padding=(0, 0, 0, 0), units=True, lineedit_options = {}, unitlabel_options = {}):
        QtW.QGroupBox.__init__(self, parent)

        stylesheet = list(margin) + list(padding)

        self.setStyleSheet("QGroupBox {background-color: white; border: 1px solid #A2A2A2; border-radius: 3px;"
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx}"
                           % tuple(stylesheet))

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.lineEdit = CLineEdit(**lineedit_options)



        self.hbox = QtW.QHBoxLayout(self)
        self.hbox.setSpacing(0)
        self.hbox.addWidget(self.lineEdit)

        if units:
            self.unitLbl = UnitsLabel(**unitlabel_options)
            self.hbox.addWidget(self.unitLbl)

class ValuewLblGroup(QtW.QGroupBox):
    def __init__(self, parent=None, width=fields['width'], height=fields['height'], margin=(0, 0, 0, 0),
                 padding=(0, 0, 0, 0), value_options = {}, unitlabel_options = {}):
        QtW.QGroupBox.__init__(self, parent)

        stylesheet = list(margin) + list(padding)

        self.setStyleSheet("QGroupBox {background-color: transparent; border: none; "
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
                           % tuple(stylesheet))

        # self.setFixedWidth(width)
        self.setFixedHeight(height)

        self.valueLbl = ValueDisplay(**value_options)
        self.unitLbl = UnitsLabel(**unitlabel_options)

        self.hbox = QtW.QHBoxLayout(self)
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.valueLbl)
        self.hbox.addSpacing(2)
        self.hbox.addWidget(self.unitLbl)

class StatusGroup(QtW.QGroupBox):
    def __init__(self, parent=None, title='', value_label=[], value_options=[], unitlabel_options=[],
                 margin=(0, 0, 0, 0), padding=(0, 0, 0, 0)):
        QtW.QGroupBox.__init__(self, parent)

        stylesheet = list(margin) + list(padding)

        self.setStyleSheet("QGroupBox {background-color: transparent; border: 1px solid #A2A2A2; border-radius: 3px;"
                           "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
                           % tuple(stylesheet))

        self.titleLbl = Header2Label(label=title, alignment='center')

        self.value_dict = {}

        for i, item in enumerate(value_label):
            item_dict = {}
            label = WidgetLabel(label=item)
            value = ValuewLblGroup(value_options=value_options[i], unitlabel_options=unitlabel_options[i])
            item_dict['Label'] = label
            item_dict['Value'] = value
            self.value_dict[i] = item_dict

        grid = QtW.QGridLayout(self)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        grid.addWidget(self.titleLbl, 0, 0, 1, 3)
        for i in self.value_dict.keys():
            grid.addWidget(self.value_dict[i]['Label'], i+1, 0, 1, 1)
            grid.addItem(QtW.QSpacerItem(0, 20, QtW.QSizePolicy.MinimumExpanding, QtW.QSizePolicy.MinimumExpanding), i+1, 1, 1, 1)
            grid.addWidget(self.value_dict[i]['Value'], i+1, 2, 1, 1)

class CSpinBox(QtW.QSpinBox):
    def __init__(self, parent=None, title='', height=fields['height'], width=fields['width'],
                 margin=(0, 0, 0, 0), padding=(0, 15, 0, 0)):
        QtW.QSpinBox.__init__(self, parent)

        # stylesheet = list(margin) + list(padding)
        #
        # self.setStyleSheet("QSpinBox {background-color: white; border: 1px solid #A2A2A2; border-radius: 3px; "
        #                    "margin: %spx %spx %spx %spx; padding: %spx %spx %spx %spx;}"
        #                    "QSpinBox:up-arrow {border-left: "
        #                    % tuple(stylesheet))
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setRange(1, 99)


class Example(QtW.QWidget):
    def __init__(self, parent=None):
        QtW.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtC.Qt.white)
        self.setPalette(p)

        vbox = QtW.QVBoxLayout(self)

        header1Lbl = Header1Label(label='Header1Label')
        vbox.addWidget(header1Lbl)

        header2Lbl = Header2Label(label='Header2Label')
        vbox.addWidget(header2Lbl)

        widgetLbl = WidgetLabel(label='WidgetLabel')
        vbox.addWidget(widgetLbl)

        unitsLbl = UnitsLabel(label='mL/min')
        vbox.addWidget(unitsLbl)

        noeditLine = ValueDisplay(label='2.0')
        vbox.addWidget(noeditLine)

        lineedit = CLineEdit(defaulttext='4.02')
        vbox.addWidget(lineedit)

        pushBtn = CPushButton(label='FilledBtn')
        vbox.addWidget(pushBtn)

        outlineBtn = OutlineButton(label='OutlineBtn')
        vbox.addWidget(outlineBtn)

        iconBtn = IconButton(iconname='ei.refresh', rotate=True)
        vbox.addWidget(iconBtn)

        radioBtn = CRadioButtons(radiolist=['Infuse', 'Withdraw'])
        vbox.addWidget(radioBtn)

        combobox = CComboBox(itemlist=['Fusion 100', 'Fusion 200', 'Fusion 400', 'Nexus 3000'], currentindex=2)
        vbox.addWidget(combobox)

        lineedit_options = {'defaulttext': '34.56'}
        unitlabel_options = {'label': 'mL/min', 'padding':(2, 0, 0, 0)}
        lineeditwlbl = LineEditwLblGroup(lineedit_options=lineedit_options, unitlabel_options=unitlabel_options)
        vbox.addWidget(lineeditwlbl)

        spinbox = CSpinBox(width=50)
        vbox.addWidget(spinbox)


if __name__ == '__main__':

    app = QtW.QApplication(sys.argv)
    if hasattr(QtC.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtC.Qt.AA_UseHighDpiPixmaps)
    app.setStyle(QtW.QStyleFactory.create('fusion'))
    test = Example()
    test.show()
    sys.exit(app.exec_())
