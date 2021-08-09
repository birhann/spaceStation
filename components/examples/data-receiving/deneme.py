# coding:utf-8
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(900, 600)
        self.myButton = QtWidgets.QPushButton(self)
        self.myButton.setObjectName("myButton")
        self.myButton.setText("click")
        self.myButton.clicked.connect(self.msg)

    def msg(self):
        # Directory1 = QFileDialog.getExistingDirectory (self, "select folder", "./") start path #
        # print(directory1)

        # set the file extension filter, note double semicolon
        fileName1, filetype = QFileDialog.getOpenFileName(
            self, "select file", "./", "All Files (*) ;; Excel Files (* .xls)")
        print(fileName1, filetype)

        # files, ok1 = QFileDialog.getOpenFileNames (self, "multi-file selection", "./", "All Files (*) ;; Text Files (* .txt)")
        # print(files,ok1)

        # FileName2, ok2 = QFileDialog.getSaveFileName (self, "File Save", "./","All Files (*) ;; Text Files (* .txt)")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.msg()
    myshow.show()
    sys.exit(app.exec_())
