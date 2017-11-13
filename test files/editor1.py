import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

filename = "Untitled"
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
        self.cutText.triggered.connect(self.text.cut)

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


        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newFile)
        self.toolbar.addAction(self.openFile)
        self.toolbar.addAction(self.saveFile)
        self.toolbar.addAction(bulletList)
        self.toolbar.addAction(numList)
        self.toolbar.addAction(self.cutText)
        self.toolbar.addAction(self.copyText)
        self.toolbar.addAction(self.pasteText)
        self.toolbar.addAction(self.undoFunc)
        self.toolbar.addAction(self.redoFunc)

        self.toolbar.addSeparator()

        self.addToolBarBreak()

    def myFormatbar(self):
        textStyle = QtGui.QFontComboBox(self)
        textStyle.currentFontChanged.connect(self.textStyle)

        textSize = QtGui.QComboBox(self)
        textSize.setEditable(True)

        textSize.setMinimumContentsLength(3)
        textSize.activated.connect(self.textSize)

        textSizes = ['6','7','8','9','10','11','12','14','16','18','20',
                    '22','24','26','28','32','36','48','72']

        for i in textSizes:
            textSize.addItem(i)

        fontCol = QtGui.QAction(QtGui.QIcon('fontCol'),'Font Color',self)
        fontCol.triggered.connect(self.textCol)

        hiCol = QtGui.QAction(QtGui.QIcon('hiCol'), 'Highlight text', self)
        hiCol.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(textStyle)
        self.formatbar.addWidget(textSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontCol)
        self.formatbar.addAction(hiCol)

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
        super(Main,self).__init__()
        self.setGeometry(100,100,1030,800)
        self.setWindowTitle("ProPoint - Untitled")
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
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open')
        self.setWindowTitle(self.filename)
        file = open(filename,'r')

        with file:
            content = file.read()
            self.text.setText(content)

    def save_file(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,'Save')
        file = open(filename,'w')
        '''print "hi"
        i = 'U+0009'
        for i in file:
            print "hi"
            cur = self.text.textCursor()
            line_no = cur.blockNumber() + 1
            col_no = cur.columnNumber()
            if(i == '\n'):
                shift = line_no+1
                for shift in range(shift,col_no+1):
                    QtGui.QTextCursor.Right'''

        content = self.text.toPlainText()
        file.write(content)

        file.close()

    def bullet_list(self) :
        cur = self.text.textCursor()
        cur.insertList(QtGui.QTextListFormat.ListDisc)

    def num_list(self):
        cur = self.text.textCursor()
        cur.insertList(QtGui.QTextListFormat.ListDecimal)

    def curPosition(self):
        cur = self.text.textCursor()
        line_no = cur.blockNumber()+1
        col_no = cur.columnNumber()
        self.mystatusbar.showMessage("Line : {} | Column : {}".format(line_no,col_no))
        #return line_no,col_no

    def textStyle(self,font):
        self.text.setCurrentFont(font)

    def textSize(self,fontsize):
        self.text.setFontPointSize(int(fontsize))

    def textCol(self):
        col = QtGui.QColorDialog.getColor()
        self.text.setTextColor(col)

    def highlight(self):
        col = QtGui.QColorDialog.getColor()
        self.text.setTextBackgroundColor(col)



def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


if __name__ =="__main__":
    main()