import sys
from typing_extensions import ParamSpec
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl

import ftplib


class SendingVideo():
    def __init__(self, GUI) -> None:
        self.interface = GUI
        self.isFileSelected = False
        self.fileName = None
        self.oldFilePath = None
        self.oldFile = None
        self.interface.chooseFileButton.clicked.connect(self.openFileDialog)
        self.interface.sentDataButton.clicked.connect(self.sendVideo)

    def openFileDialog(self):
        self.filePath, self.filetype = QFileDialog.getOpenFileName(
            self.interface, "select file", "./", "All Files (*) ;; Excel Files (* .xls)")
        self.file = QUrl.fromLocalFile(self.filePath)

        if not self.file.isEmpty():
            self.fileName = self.file.fileName()
            self.interface.fileNameLineEdit.setText(self.fileName)
            self.isFileSelected = True
            self.oldFilePath = self.filePath
            self.oldFile = self.file
            print(self.fileName, self.filePath, " file selected..")

        elif self.file.isEmpty() and self.isFileSelected:
            self.interface.fileNameLineEdit.setText((self.fileName))
            self.isFileSelected = True
            print(self.fileName, " old file still selected..")

        else:
            self.interface.fileNameLineEdit.setText((self.fileName))
            self.isFileSelected = False
            print("file not selected")

    def sendVideo(self):
        if self.isFileSelected:
            if self.file.isEmpty():
                session = ftplib.FTP(
                    '192.168.137.178', 'esp32', 'esp32')
                file = open("{}".format(self.oldFilePath), 'rb')
                session.storbinary('STOR {}'.format(self.fileName), file)
                file.close()
                session.quit()
            else:
                session = ftplib.FTP(
                    '192.168.137.178', 'esp32', 'esp32')
                file = open("{}".format(self.filePath), 'rb')
                session.storbinary('STOR {}'.format(self.fileName), file)
                file.close()
                session.quit()
        else:
            print("asd")
