#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, time
from PyQt4 import QtCore, QtGui
from pymouse import PyMouse

class TimerWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TimerWindow, self).__init__(parent)
        self.label = QtGui.QLabel()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        font=QtGui.QFont()
        font.setPixelSize(60)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.stopButton = QtGui.QPushButton("&Stop")
        self.stopButton.setFixedWidth(60)
        self.stopButton.setStyleSheet("margin-bottom: 10px;padding: 4px;")
        self.stopButton.clicked.connect(self.stop)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.stopButton, alignment=QtCore.Qt.AlignHCenter)
        
        self.setLayout(layout)
        self.resize(400, 400)

    def run(self, sec, countdown):
        self.sec = sec
        self.countdown = countdown
        self.countdown3Init()

    def stop(self):
        self.timer.stop()
        self.config_window = ConfigWindow()
        self.config_window.move(self.pos())
        self.config_window.show()
        self.close()
            
    def mainUpdateInit(self):
        self.setStyleSheet("\
        QPushButton {background-color:#fff; color:#49f;}\
        TimerWindow {background-color:#fff; border-bottom:10px solid #49f}\
        QLabel {color:#777;}")
        self.now = self.sec
        self.mainUpdate()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.mainUpdate)
        self.timer.start(1000)

    def mainUpdate(self):
        self.label.setText(str(self.now))
        self.now -= 1
        if self.now == -1:
            self.timer.stop()
            if self.countdown:
                self.countdown3Init()
            else:
                self.mainUpdateInit()
        elif self.now == 60:
            self.setStyleSheet("\
            QPushButton {background-color:#fff; color:#af0;}\
            TimerWindow {background-color:#af0;}\
            QLabel {color:#fff;}")
        elif self.now == 29:
            self.setStyleSheet("\
            QPushButton {background-color:#fff; color:#49f;}\
            TimerWindow {background-color:#49f;}\
            QLabel {color:#fff;}")
        elif self.now == 19:
            self.setStyleSheet("\
            QPushButton {background-color:#fff; color:#fa0;}\
            TimerWindow {background-color:#fa0;}\
            QLabel {color:#fff;}")
        elif self.now == 9:
            self.setStyleSheet("\
            QPushButton {background-color:#fff; color:#f00;}\
            TimerWindow {background-color:#f00;}\
            QLabel {color:#fff;}")
        elif self.now == 2:
            self.setStyleSheet("\
            QPushButton {background-color:#fff; color:#700;}\
            TimerWindow {background-color:#700}\
            QLabel {color:#fff;}")

    def countdown3Init(self):
        self.setStyleSheet("background-color:#222;color:#eee;")
        self.now = 3
        self.countdown3()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.countdown3)
        self.timer.start(1000)
        
    def countdown3(self):
        self.label.setText(str(self.now))
        self.now -= 1
        if self.now == -1:
            self.timer.stop()
            # Call main loop
            self.mainUpdateInit()


class ConfigWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        layout = QtGui.QGridLayout()
        self.radio_buttons = QtGui.QButtonGroup(parent)
        r10 = QtGui.QRadioButton("&10 Sec")
        r15 = QtGui.QRadioButton("1&5 Sec")
        r30 = QtGui.QRadioButton("&30 Sec")
        r45 = QtGui.QRadioButton("&45 Sec")
        r60 = QtGui.QRadioButton("&60 Sec")
        r90 = QtGui.QRadioButton("&90 Sec")
        
        self.radio_buttons.addButton(r10)
        self.radio_buttons.addButton(r15)
        self.radio_buttons.addButton(r30)
        self.radio_buttons.addButton(r45)
        self.radio_buttons.addButton(r60)
        self.radio_buttons.addButton(r90)
        layout.addWidget(r10, 0, 0)
        layout.addWidget(r15, 0, 1)
        layout.addWidget(r30, 0, 2)
        layout.addWidget(r45, 1, 0)
        layout.addWidget(r60, 1, 1)
        layout.addWidget(r90, 1, 2)
        r30.setChecked(True)
        
        self.countdown = QtGui.QCheckBox("&Countdown")
        layout.addWidget(self.countdown, 2, 0, 1, 3)

        startButton = QtGui.QPushButton("&Start")
        layout.addWidget(startButton, 3, 2)
        startButton.clicked.connect(self.positionSelector)
        startButton.setDefault(True)
        
        quitButton = QtGui.QPushButton("&Quit")
        layout.addWidget(quitButton, 3, 0)
        quitButton.clicked.connect(self.close)
        
        self.setWindowTitle("Posemaniac Timer")
        self.setLayout(layout)

        self.setStyleSheet('''
        background-color: #fff;
        color: #666;
        ''')

    def positionSelector(self):
        r = self.radio_buttons.checkedId()
        if r == -2:
            sec = 10
        elif r == -3:
            sec = 15
        elif r == -4:
            sec = 30
        elif r == -5:
            sec = 45
        elif r == -6:
            sec = 60
        elif r == -7:
            sec = 90

        if self.countdown.checkState() == 2:
            countdown = True
        else:
            countdown = False
        
        self.position_selection_ui = PositionSelectionUI(sec, countdown, self.pos())
        self.close()            # 不太確定會不會有問題

class PositionSelectionUI (QtGui.QWidget):
    def __init__ (self, sec, countdown, configWindowPos, parent = None):
        self.sec = sec
        self.countdown = countdown

        # Create TimerWindow Instance
        self.timer_window = TimerWindow()
        self.timer_window.move(configWindowPos)
        
        super(PositionSelectionUI, self).__init__(parent)
        self.setWindowOpacity(0.7)
        self.setStyleSheet("background-color:rgba(0,0,0,180)")
        # Init QLabel
        self.label = PositionSelectionUILabel(self)
        # Init QLayout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label)
        layout.setMargin(0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.show()
        self.showFullScreen()

    def callTimerAndRun(self):
        # parent is ConfigWindow
        self.timer_window.show()
        # this will remove minimized status 
        # and restore window with keeping maximized/normal state
        self.timer_window.setWindowState(self.timer_window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # this will activate the window
        self.timer_window.activateWindow()
        self.timer_window.run(self.sec, self.countdown)
        self.close()

class PositionSelectionUILabel (QtGui.QLabel):
    def __init__ (self, parent = None):
        super(PositionSelectionUILabel, self).__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)
        self.setTextLabelPosition(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def mouseMoveEvent (self, event):
        self.setTextLabelPosition(event.x(), event.y())
        QtGui.QWidget.mouseMoveEvent(self, event)

    def mousePressEvent (self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.parent.hide()
            pos=event.pos()
            mouse = PyMouse()
            
            time.sleep(0.2)
            mouse.click(pos.x(), pos.y())

            # parent is PositionSelectionUI
            self.parent.callTimerAndRun()

        QtGui.QWidget.mousePressEvent(self, event)
        
    def setTextLabelPosition (self, x, y):
        self.x, self.y = x, y
        self.setText('Please click at START button on Posemaniacs page. ( %d : %d )' % (self.x, self.y))
        

        
app = QtGui.QApplication(sys.argv)
config_window = ConfigWindow()
config_window.show()

app.exec_()
