import sys
import threading

import PyQt4
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
import rethinkdb as r
from PyQt4.QtGui import QPushButton


class Main( QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.filename = " "
        self.win_features()



    def myToolbar(self):

        self.newFile = QtGui.QAction(QtGui.QIcon("new_logo"),'New',self)
        self.newFile.setStatusTip(' New ')
        self.newFile.setShortcut('Ctrl+N')
        self.newFile.triggered.connect(self.new_file)

        self.openFile = QtGui.QAction(QtGui.QIcon('open'), 'Open', self)
        self.openFile.setStatusTip(' Open ')
        self.openFile.setShortcut('Ctrl+O')
        self.openFile.triggered.connect(self.open_file)

        self.saveFile = QtGui.QAction(QtGui.QIcon('save_logo'), 'Save', self)
        self.saveFile.setStatusTip('Create a new document')
        self.saveFile.setShortcut('Ctrl+S')
        self.saveFile.triggered.connect(self.save_file)

        self.cutText = QtGui.QAction(QtGui.QIcon('cut'), 'Cut', self)
        self.cutText.setStatusTip('Cut')
        self.cutText.setShortcut('Ctrl+X')
        self.cutText.triggered.connect(self.text.copy)

        self.copyText = QtGui.QAction(QtGui.QIcon('copy'), 'Copy', self)
        self.copyText.setStatusTip('Copy')
        self.copyText.setShortcut('Ctrl+C')
        self.copyText.triggered.connect(self.text.copy)

        self.pasteText = QtGui.QAction(QtGui.QIcon('paste'), 'Paste', self)
        self.pasteText.setStatusTip('Paste')
        self.pasteText.setShortcut('Ctrl+V')
        self.pasteText.triggered.connect(self.text.paste)

        self.undoFunc = QtGui.QAction(QtGui.QIcon('Undo'), 'Undo', self)
        self.undoFunc.setStatusTip('Undo')
        self.undoFunc.setShortcut('Ctrl+Z')
        self.undoFunc.triggered.connect(self.text.undo)

        self.redoFunc = QtGui.QAction(QtGui.QIcon('Redo'), 'Redo', self)
        self.redoFunc.setStatusTip('Redo')
        self.redoFunc.setShortcut('Ctrl+Y')
        self.redoFunc.triggered.connect(self.text.redo)

        bulletList = QtGui.QAction(QtGui.QIcon('bullet'), 'Bulleted List', self)
        bulletList.setStatusTip('Bulleted List')
        bulletList.setShortcut('Ctrl+Shift+B')
        bulletList.triggered.connect(self.bullet_list)

        numList = QtGui.QAction(QtGui.QIcon('numbered'), 'Numbered List', self)
        numList.setStatusTip('Numbered List')
        numList.setShortcut('Ctrl+Shift+L')
        numList.triggered.connect(self.num_list)

        pb = QtGui.QAction(QtGui.QIcon('logo1'), 'send', self)
        pb.setStatusTip('send')
        pb.setShortcut('Ctrl+Shift+k')
        pb.triggered.connect(self.send_btn)

        rb = QtGui.QAction(QtGui.QIcon('logo1'), 'send', self)
        rb.setStatusTip('recieve')
        rb.setShortcut('Ctrl+Shift+g')
        rb.triggered.connect(self.get_btn)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newFile)
        self.toolbar.addAction(self.openFile)
        self.toolbar.addAction(self.saveFile)
        self.toolbar.addAction(bulletList)
        self.toolbar.addAction(numList)
        self.toolbar.addAction(pb)
        self.toolbar.addAction(rb)
        self.toolbar.addAction(self.cutText)
        self.toolbar.addAction(self.copyText)
        self.toolbar.addAction(self.pasteText)
        self.toolbar.addAction(self.undoFunc)
        self.toolbar.addAction(self.redoFunc)

        self.toolbar.addSeparator()

        self.addToolBarBreak()

    def myFormatbar(self):
        self.formatbar = self.addToolBar("Format")

    def myMenubar(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(self.newFile)
        file.addAction(self.openFile)
        file.addAction(self.saveFile)

        edit.addAction(self.cutText)
        edit.addAction(self.copyText)
        edit.addAction(self.pasteText)
        edit.addAction(self.undoFunc)
        edit.addAction(self.redoFunc)


    def win_features(self):
        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("ProPoint")
        self.setWindowIcon(QtGui.QIcon('logo1.png'))

        self.text = QtGui.QTextEdit(self)
        self.setCentralWidget(self.text)
        self.myToolbar()
        self.myFormatbar()
        self.myMenubar()
        self.mystatusbar = self.statusBar()
        self.text.cursorPositionChanged.connect(self.curPosition)


    def new_file(self):
        temp1 = Main(self)
        temp1.show()

    def open_file(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", ".", "(.*writer)")
        if self.filename:
            with open(self.filename, "rt") as file:
                self.text.setText(file.read())

    def save_file(self):
        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, "Save")

        if not self.filename.endswith(".wx"):
            self.filename += ".wx"

        with open(self.filename, "wt") as file:
            file.write(self.text.toHtml())

    def bullet_list(self) :
        cur = self.text.textCursor()
        cur.insertList(QtGui.QTextListFormat.ListDisc)

    def num_list(self):
        cur = self.text.textCursor()
        cur.insertList(QtGui.QTextListFormat.ListDecimal)

    def curPosition(self):

        global data
        data = str( self.text.toPlainText())
        print data
        self.send_btn(data)

        global cur
        cur = self.text.textCursor()
        line_no = cur.blockNumber()+1
        col_no = cur.columnNumber()
        self.mystatusbar.showMessage("Line : {} | Column : {}".format(line_no,col_no))



    def send_btn(self, data):
        r.connect( "localhost", 28015).repl()
        list=r.db('test').table_list().run()
        if "proPoint" in list:
            print("table exists")
            r.table("proPoint").get(2).update({
                "value" : data
            }).run()
            print("updated")
        else:
            r.db("test").table_create("proPoint").run()
            r.table("proPoint").insert({
                "id" : 2,
                "value" : "robin"
            }).run()
            print("inserted")
        print("finished")

    def get_btn(self):
        r.connect( "localhost", 28015).repl()
        var=r.db('test').table('proPoint').get(2).run()
        print(var)
        var1 = QString(var['value'])
        self.text.setText(var1)
        #cur = self.text.QTextCursor.End

def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


if __name__ =="__main__":
    main()