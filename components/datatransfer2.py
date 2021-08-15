# if self.file.isEmpty():
import ftplib
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from typing_extensions import ParamSpec
import sys


class DataTransferWorker(QThread):
    receivedtel = pyqtSignal(list, object)
    connectionControl = pyqtSignal(object)
    filePath = None
    fileName = None

    def run(self):
        session = ftplib.FTP(
            '192.168.137.178', 'esp32', 'esp32')
        self.file = open("{}".format(self.filePath), 'rb')
        session.storbinary('STOR {}'.format(self.fileName), self.file)
        self.file.close()
        session.quit()


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
            self.interface.infoScreen.insertPlainText("Data Transfer: '{}' {}".format(
                self.fileName, "File selected!\n"))

        elif self.file.isEmpty() and self.isFileSelected:
            self.interface.fileNameLineEdit.setText((self.fileName))
            self.isFileSelected = True
            self.interface.infoScreen.insertPlainText("Data Transfer: '{}' {}".format(
                self.fileName, "Old file selected!\n"))

        else:
            self.interface.fileNameLineEdit.setText((self.fileName))
            self.isFileSelected = False
            self.interface.infoScreen.insertPlainText(
                "Data Transfer: File not selected!\n")

    def sendVideo(self):
        if self.isFileSelected:

            self.thread = DataTransferWorker()
            self.thread.daemon = True
            self.thread.receivedtel.connect(self.setTelemetry)
            self.thread.finished.connect(self.setLastInfos)
            if self.file.isEmpty():
                self.thread.filePath = self.oldFilePath
            else:
                self.thread.filePath = self.filePath
            self.thread.fileName = self.fileName
            self.thread.start()
        else:
            self.interface.infoScreen.insertPlainText(
                "Data Transfer: Please select file first!\n")
