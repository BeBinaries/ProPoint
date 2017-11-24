from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Share(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.initUI()

    def initUI(self):
        self.label1 = QtGui.QLabel("User Name: ", self)
        self.label1.setStyleSheet("font-size: 15px; ")
        self.label1.move(10, 10)

        self.userTextBox = QtGui.QTextEdit(self)
        self.userTextBox.move(10, 40)
        self.userTextBox.resize(250, 25)

        self.label2 = QtGui.QLabel("Document Name: ", self)
        self.label2.setStyleSheet("font-size: 15px; ")
        self.label2.move(10, 80)

        self.docTextBox = QtGui.QTextEdit(self)
        self.docTextBox.move(10, 110)
        self.docTextBox.resize(250, 25)

        self.label3 = QtGui.QLabel("Key: ", self)
        self.label3.setStyleSheet("font-size: 15px; ")
        self.label3.move(10, 150)

        self.kTextBox = QtGui.QTextEdit(self)
        self.kTextBox.move(10, 180)
        self.kTextBox.resize(250, 25)

        self.share = QtGui.QPushButton("Share", self)
        self.share.move(180, 220)

        self.close = QtGui.QPushButton("Close", self)
        self.close.move(270, 220)
        self.close.clicked.connect(self.Close)

        self.setGeometry(300, 300, 360, 250)

    def Close(self):
        self.hide()


