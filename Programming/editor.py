#   ProPoint documentation master file, created by
#  sphinx-quickstart on Mon Nov 20 00:55:55 2017.
#   You can adapt this file completely to your liking, but it should at least
#   contain the root `toctree` directive.

#   Welcome to ProPoint's documentation!
#   ====================================
#   This is my introduction to the project 'PROPOINT'.

#   The ProPoint is a collaborative text editor specifically built for
#   Coding community in order to collaborate and build interesting Software.
#   It has some interesting functionality which is very rare in the any other
#   collaborative editors, one of those is to have an offline interface for
#   collaboration. Since it is offline, users can edit the view of their documents
#   in the same way a non-coding editor edits its text field. In spite of being a
#   collaborative editor it supports all features of a normal text editor like,
#   saving the document or opening an existing document from the PC
#   directly. Our aim is to ease the collaboration between coders.

#   Requirements :
#
#	- RethinkdB (2.3.6) must be installed.
#	- Depends on package PyQt



import sys
import time as time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qt
import rethinkdb as r
from PyQt4.QtGui import QPushButton
from memory_profiler import profile

from Find_Object import *
from share import *


filename = "Untitled"
caseSensitive = False
wholeWord = False

class Main(QtGui.QMainWindow):
    """
        This class represents the main window of the editor.

        Function involved :
            - myToolBar()
            - myFormatBar()
            - myMenuBar()
            - winFeatures()...

    """
    @profile
    def __init__(self, parent=None):
        """
        -----------Constructor-----------
                self,parent :parameter
                parent: None
        """
        QtGui.QMainWindow.__init__(self, parent)
        # self.filename = " ProPoint - Share your Projects "

        self.senderThread = SenderThread()
        self.win_features()

    def myToolbar(self):
        """
            self :parameter
            :return:  None

            This function sets the structure of the Toolbar in the editor. Also connects the designed buttons to their respective
            functions defined in Main Class.
        """
        self.newFile = QtGui.QAction(QtGui.QIcon("res/new_logo"), 'New', self)
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

        findAction = QtGui.QAction(QtGui.QIcon('res/find'), 'Redo', self)
        findAction.setStatusTip("Find")
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self.Find)

        shareAction = QtGui.QAction(QtGui.QIcon('res/share'), "Find", self)
        shareAction.setStatusTip("Share")
        shareAction.setShortcut("Alt+S")
        shareAction.triggered.connect(self.Share)

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

        self.toolbar.addSeparator()

        self.toolbar.addAction(findAction)
        self.toolbar.addAction(shareAction)
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

        textSizes = ['6', '7', '8', '9', '10', '11', '12', '14', '16', '18', '20',
                     '22', '24', '26', '28', '32', '36', '48', '72']

        for i in textSizes:
            textSize.addItem(i)

        fontCol = QtGui.QAction(QtGui.QIcon('res/fontCol'), 'Font Color', self)
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

        indentAction = QtGui.QAction(QtGui.QIcon('res/indent'), "Indent text", self)
        indentAction.setStatusTip('Indent')
        indentAction.setShortcut('Ctrl+Tab')
        indentAction.triggered.connect(self.Indent)

        alignRightAction = QtGui.QAction(QtGui.QIcon('res/rightAllign'), "Align text Right", self)
        alignRightAction.setStatusTip('Align Right')
        alignRightAction.triggered.connect(self.alignRight)

        alignLeftAction = QtGui.QAction(QtGui.QIcon('res/leftAllign'), "Align text Left", self)
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
        """
            self :parameter
            :return: None

            Designs menu items in Menu such as File and Edit.
        """
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
        """
            :parameter: self
            :return: None

            This function provides features such as toolbar, menubar etc..... by calling the functions defined above.
        """
        super(Main, self).__init__()
        self.setGeometry(100, 100, 1030, 800)
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
        """
            :parameter: self
            :return: None

            This function creates a new file.
        """
        temp1 = Main(self)
        temp1.show()

    def open_file(self):
        """
                    :parameter: self
                    :return: None

                    This function opens an existing file.
        """

        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open')
        self.setWindowTitle(filename)
        file = open(filename, 'r')

        with file:
            content = file.read()
            self.text.setText(content)

    def save_file(self):
        """
                    :parameter: self
                    :return: None

                    This function saves a file.
        """
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save')
        file = open(filename, 'w')
        content = self.text.toPlainText()
        file.write(content)

        file.close()

    def bullet_list(self):
        """
                    :parameter: self
                    :return: None

                    This function creates a bulleted list.
        """

        cur.insertList(QtGui.QTextListFormat.ListDisc)

    def num_list(self):
        """
                    :parameter: self
                    :return: None

                    This function creates a Numbered list.
        """
        cur.insertList(QtGui.QTextListFormat.ListDecimal)

    def Indent(self):
        """
                :parameter: self
                :return: None

                This function indents the document.
        """
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

        while cursor.position() < end:
            global var
            # print(cursor.position(),end)

            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)
            end += len(tab)

    def alignLeft(self):
        """
                :parameter: self
                :return: None

                This function aligns the document left.
        """
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        """
                :parameter: self
                :return: None

                This function aligns the document Right.
        """
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        """
            :parameter: self
            :return: None

            This function aligns the document to center.
        """
        self.text.setAlignment(Qt.AlignCenter)

    def bold(self):
        """
            :parameter: self
            :return: None

            This function makes the selected text Bold.
        """
        weight = self.text.fontWeight()
        if weight == 50:
            self.text.setFontWeight(QtGui.QFont.Bold)
        elif weight == 75:
            self.text.setFontWeight(QtGui.QFont.Normal)

    def italic(self):
        """
                :parameter: self
                :return: None

                This function makes the selected text italic.
        """
        incline = self.text.fontItalic()

        if incline == False:
            self.text.setFontItalic(True)
        elif incline == True:
            self.text.setFontItalic(False)

    def underline(self):
        """
                    :parameter: self
                    :return: None

                    This function underlines the selected text.
        """
        uline = self.text.fontUnderline()
        if uline == False:
            self.text.setFontUnderline(True)
        elif uline == True:
            self.text.setFontUnderline(False)

    def textStyle(self, font):
        """
                    :parameter: self
                    :return: None

                    This function changes the font style.
         """
        self.text.setCurrentFont(font)

    def textSize(self, fontsize):
        """
                    :parameter: self
                    :return: None

                    This function changes the text size.
        """
        self.text.setFontPointSize(int(fontsize))

    def textCol(self):
        """
                    :parameter: self
                    :return: None

                    This function sets the font colour.
        """
        col = QtGui.QColorDialog.getColor()
        self.text.setTextColor(col)

    def highlight(self):
        """
                    :parameter: self
                    :return: None

                    This function sets the background of the font.
        """
        col = QtGui.QColorDialog.getColor()
        self.text.setTextBackgroundColor(col)

    def Share(self):
        """
                    :parameter: self
                    :return: None

                    Builds a dialog box to input the data in order to share the document.
        """
        share1 = Share(self)
        share1.show()

        def shareHandler():
            uName = share1.userTextBox.toPlainText()
            for i in uName:
                if ((i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z')):
                     flag =1
                else:
                    flag = 0
            if flag == 1:
                print(uName)
            else:
                QMessageBox.warning(QWidget(), "Message","Enter valid User Name \n Username must consist of only alphabets")
            #flag = 0

            dName = share1.docTextBox.toPlainText()
            for i in dName:
                if ((i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z')):
                    flag = 1
                else:
                    flag = 0
            if flag == 1:
                print(dName)
            else:
                QMessageBox.warning(QWidget(), "Message","Enter valid Document Name \n Document Name must consist of atleast 1 alphabet")


            k = share1.kTextBox.toPlainText()
            print (k)

        share1.share.clicked.connect(shareHandler)


    def Find(self):
        """
                    :parameter: self
                    :return: None

                    This function has the code to implement the cases to find a string in the editor window.
        """
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
        """
                :parameter: self
                :return: None

                This function provides the position of the cursor.
        """
        self.senderThread.start()
        global data
        data = str(self.text.toPlainText())
        self.text.blockSignals(True)
        global r_data
        r_data = data
        # r_data = str(self.text.setText(r_data))
        # self.text.moveCursor(QtGui.QTextCursor.End)
        self.text.blockSignals(False)
        print data
        # self.send_data(data)


        global cur
        cur = self.text.textCursor()
        line_no = cur.blockNumber() + 1
        col_no = cur.columnNumber()
        self.mystatusbar.showMessage("Line : {} | Column : {}".format(line_no, col_no))

    def get_btn(self, r_data):
        """
                    :parameter: self
                    :return: None

                    This function is used to recieve the document from database.
        """
        r.connect("localhost", 28015).repl()
        list = r.db('test').table_list().run()
        if "proPoints" in list:  # its proPoints not proPoint
            var = r.db('test').table('proPoints').get(2).run()
            print(var)
            var1 = QString(var['value'])
            var2 = QString(var['user'])
            if var2 == "pujam":
                self.text.setText(var1)
        #else:
            #self.send_btn(" ")





class SenderThread(QThread):
    """
        :parameter: self

        This class implemets  methods to create new thread for updating the database.
    """
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        time.sleep(1)
        print "Send call"
        self.send_data(data)
        print "Sent"
        print "Thread done"

    def send_data(self, data):
        r.connect("localhost", 28015).repl()
        list = r.db('test').table_list().run()
        if "proPoints" in list:  # its proPoints not proPoint
            print("table exists")
            r.table("proPoints").get(2).update({
                "user": "pujam",
                "value": data
            }).run()
            print("updated")
        else:
            r.db("test").table_create("proPoints").run()
            r.table("proPoints").insert({
                "id": 2,
                "user": "pujam",
                "value": "robin"
            }).run()
            print("inserted")
        print("finished")


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
