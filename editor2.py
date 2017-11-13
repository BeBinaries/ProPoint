import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qt
import rethinkdb as r
from PyQt4.QtGui import QPushButton


filename = "Untitled"
caseSensitive = False
wholeWord = False


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




class Main( QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
       # self.filename = " ProPoint - Share your Projects "
        self.win_features()

    def myToolbar(self):

        self.newFile = QtGui.QAction(QtGui.QIcon("res/new_logo"),'New',self)
        self.newFile.setStatusTip(' New ')
        self.newFile.setShortcut('Ctrl+N')
        self.newFile.triggered.connect(self.new_file)

        self.openFile = QtGui.QAction(QtGui.QIcon('res/open'), 'Open', self)
        self.openFile.setStatusTip(' Open ')
        self.openFile.setShortcut('Ctrl+O')
        self.openFile.triggered.connect(self.open_file)

        self.saveFile = QtGui.QAction(QtGui.QIcon('res/save_logo'), 'Save', self)
        self.saveFile.setStatusTip('Create a new document')
        self.saveFile.setShortcut('Ctrl+S')
        self.saveFile.triggered.connect(self.save_file)

        self.cutText = QtGui.QAction(QtGui.QIcon('res/cut'), 'Cut', self)
        self.cutText.setStatusTip('Cut')
        self.cutText.setShortcut('Ctrl+X')
        self.cutText.triggered.connect(self.text.cut)

        self.copyText = QtGui.QAction(QtGui.QIcon('res/copy'), 'Copy', self)
        self.copyText.setStatusTip('Copy')
        self.copyText.setShortcut('Ctrl+C')
        self.copyText.triggered.connect(self.text.copy)

        self.pasteText = QtGui.QAction(QtGui.QIcon('res/paste'), 'Paste', self)
        self.pasteText.setStatusTip('Paste')
        self.pasteText.setShortcut('Ctrl+V')
        self.pasteText.triggered.connect(self.text.paste)

        self.undoFunc = QtGui.QAction(QtGui.QIcon('res/Undo'), 'Undo', self)
        self.undoFunc.setStatusTip('Undo')
        self.undoFunc.setShortcut('Ctrl+Z')
        self.undoFunc.triggered.connect(self.text.undo)

        self.redoFunc = QtGui.QAction(QtGui.QIcon('res/Redo'), 'Redo', self)
        self.redoFunc.setStatusTip('Redo')
        self.redoFunc.setShortcut('Ctrl+Y')
        self.redoFunc.triggered.connect(self.text.redo)

        findAction = QtGui.QAction(QtGui.QIcon('res/find'), "Find", self)
        findAction.setStatusTip("Find")
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self.Find)

        rb = QtGui.QAction(QtGui.QIcon('res/recieve'), 'Recieve', self)
        rb.setStatusTip('Recieve')
        rb.setShortcut('Ctrl+Shift+g')
        rb.triggered.connect(self.get_btn)


        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.newFile)
        self.toolbar.addAction(self.openFile)
        self.toolbar.addAction(self.saveFile)
        self.toolbar.addAction(self.cutText)
        self.toolbar.addAction(self.copyText)
        self.toolbar.addAction(self.pasteText)
        self.toolbar.addAction(self.undoFunc)
        self.toolbar.addAction(self.redoFunc)
        self.toolbar.addAction(findAction)
        self.toolbar.addAction(rb)

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

        fontCol = QtGui.QAction(QtGui.QIcon('res/fontCol'),'Font Color',self)
        fontCol.triggered.connect(self.textCol)

        hiCol = QtGui.QAction(QtGui.QIcon('res/hiCol'), 'Highlight text', self)
        hiCol.triggered.connect(self.highlight)

        boldAction = QtGui.QAction(QtGui.QIcon('res/bold'), "Bold text", self)
        boldAction.setStatusTip('Bold')
        boldAction.setShortcut('Ctrl+B')
        boldAction.triggered.connect(self.bold)

        italicAction = QtGui.QAction(QtGui.QIcon('res/Italic'), "Italic text", self)
        italicAction.setStatusTip('Italic')
        italicAction.setShortcut('Ctrl+I')
        italicAction.triggered.connect(self.italic)

        underlineAction = QtGui.QAction(QtGui.QIcon('res/underline'), "Underline text", self)
        underlineAction.setStatusTip('Underline Text')
        underlineAction.setShortcut('Ctrl+U')
        underlineAction.triggered.connect(self.underline)

        indentAction = QtGui.QAction(QtGui.QIcon('res/indent'),"Indent text",self)
        indentAction.setStatusTip('Indent')
        indentAction.setShortcut('Ctrl+Tab')
        indentAction.triggered.connect(self.Indent)

        alignRightAction = QtGui.QAction(QtGui.QIcon('res/rightAllign'),"Align text Right",self)
        alignRightAction.setStatusTip('Align Right')
        alignRightAction.triggered.connect(self.alignRight)

        alignLeftAction = QtGui.QAction(QtGui.QIcon('res/leftAllign'),"Align text Left",self)
        alignLeftAction.setStatusTip('Align Left')
        alignLeftAction.triggered.connect(self.alignLeft)

        alignCenterAction = QtGui.QAction(QtGui.QIcon('res/CenterAllign'), "Align text Center", self)
        alignCenterAction.setStatusTip('Align Center')
        alignCenterAction.triggered.connect(self.alignCenter)


        bulletList = QtGui.QAction(QtGui.QIcon('res/bullet'), 'Bulleted List', self)
        bulletList.setStatusTip('Bulleted List')
        bulletList.setShortcut('Ctrl+Shift+B')
        bulletList.triggered.connect(self.bullet_list)

        numList = QtGui.QAction(QtGui.QIcon('res/numbered'), 'Numbered List', self)
        numList.setStatusTip('Numbered List')
        numList.setShortcut('Ctrl+Shift+L')
        numList.triggered.connect(self.num_list)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(textStyle)
        self.formatbar.addWidget(textSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontCol)
        self.formatbar.addAction(hiCol)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(alignLeftAction)
        self.formatbar.addAction(alignRightAction)
        self.formatbar.addAction(alignCenterAction)
        self.formatbar.addAction(bulletList)
        self.formatbar.addAction(numList)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlineAction)


    def myMenubar(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        about = menubar.addMenu("About")
        help = menubar.addMenu("Help")

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
        self.setWindowIcon(QtGui.QIcon('res/logo1.png'))

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
        self.setWindowTitle(filename)
        file = open(filename,'r')

        with file:
            content = file.read()
            self.text.setText(content)

    def save_file(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,'Save')
        file = open(filename,'w')
        content = self.text.toPlainText()
        file.write(content)

        file.close()

    def bullet_list(self) :
        cur.insertList(QtGui.QTextListFormat.ListDisc)

    def num_list(self):
        cur.insertList(QtGui.QTextListFormat.ListDecimal)

    def Indent(self):
        tab = "\t"
        start = cur.selectionStart()
        end = cur.selectionEnd()
        cursor = cur

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()

        while cursor.position() < end :
            global var
            #print(cursor.position(),end)

            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)
            end += len(tab)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def bold(self):
        weight = self.text.fontWeight()
        if weight == 50:
            self.text.setFontWeight(QtGui.QFont.Bold)
        elif weight == 75:
            self.text.setFontWeight(QtGui.QFont.Normal)

    def italic(self):
        incline = self.text.fontItalic()

        if incline == False:
            self.text.setFontItalic(True)
        elif incline == True:
            self.text.setFontItalic(False)

    def underline(self):
        uline = self.text.fontUnderline()
        if uline == False:
            self.text.setFontUnderline(True)
        elif uline == True:
            self.text.setFontUnderline(False)


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

    def Find(self):
        global f

        find = Find(self)
        find.show()

        def handleFind():

            f = find.findTextBox.toPlainText()
            print(f)

            casesen = False
            wholeword = False

            if casesen == True and wholeword == False:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively

            elif casesen == False and wholeword == False:
                flag = QtGui.QTextDocument.FindBackward

            elif casesen == False and wholeword == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindWholeWords

            elif casesen == True and wholeword == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords

            self.text.find(f, flag)

        def handleReplace():
            f = find.findTextBox.toPlainText()
            r = find.replaceTextBox.toPlainText()

            text = self.text.toPlainText()

            newText = text.replace(f, r)

            self.text.clear()
            self.text.append(newText)

        find.src.clicked.connect(handleFind)
        find.replaceButton.clicked.connect(handleReplace)


    def curPosition(self):
        global data
        data = str(self.text.toPlainText())
        print data
        self.send_data(data)

        global cur
        cur = self.text.textCursor()
        line_no = cur.blockNumber() + 1
        col_no = cur.columnNumber()
        self.mystatusbar.showMessage("Line : {} | Column : {}".format(line_no, col_no))

    def send_data(self, data):
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


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


if __name__ =="__main__":
    main()