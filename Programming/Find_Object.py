from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Find(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.initUI()

    def initUI(self):

        self.label1 = QtGui.QLabel("Search for: ", self)
        self.label1.setStyleSheet("font-size: 15px; ")
        self.label1.move(10, 10)

        self.findTextBox = QtGui.QTextEdit(self)
        self.findTextBox.move(10, 40)
        self.findTextBox.resize(250, 25)

        self.src = QtGui.QPushButton("Find", self)
        self.src.move(270, 40)

        self.label2 = QtGui.QLabel("Replace all by: ", self)
        self.label2.setStyleSheet("font-size: 15px; ")
        self.label2.move(10, 80)

        self.replaceTextBox = QtGui.QTextEdit(self)
        self.replaceTextBox.move(10, 110)
        self.replaceTextBox.resize(250, 25)

        self.replaceButton = QtGui.QPushButton("Replace", self)
        self.replaceButton.move(270, 110)

        self.option1 = QtGui.QCheckBox("Case sensitive", self)
        self.option1.move(10, 160)
        self.option1.stateChanged.connect(self.CaseSen)

        self.option2 = QtGui.QCheckBox("Whole words only", self)
        self.option2.move(10, 190)
        self.option2.stateChanged.connect(self.WholeWordOnly)

        self.close = QtGui.QPushButton("Close", self)
        self.close.move(270, 220)
        self.close.clicked.connect(self.Close)

        self.setGeometry(300, 300, 360, 250)

    def CaseSen(self, state):
        global caseSensitive

        if state == QtCore.Qt.Checked:
            caseSensitive = True
        else:
            caseSensitive = False

    def WholeWordOnly(self, state):
        global wholeWord
        print wholeWord

        if state == QtCore.Qt.Checked:
            wholeWord = True
        else:
            wholeWord = False

    def Close(self):
        self.hide()