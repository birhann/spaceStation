# if self.file.isEmpty():
import ftplib
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from typing_extensions import ParamSpec
import sys
from config import appConfig


class DataTransferWorker(QThread):
    throwError = pyqtSignal(str)
    startTelemetry = pyqtSignal()

    ESP_IP_ADDRESS = appConfig["ESP_IP_ADDRESS"]
    filePath = None
    fileName = None

    def run(self):
        try:

            self.throwError.emit("Trying to connect to server...")
            session = ftplib.FTP(self.ESP_IP_ADDRESS, 'esp32', 'esp32')
            self.file = open("{}".format(self.filePath), 'rb')
            self.throwError.emit("Connection to server successful!")
            self.throwError.emit("Sending file...")
            session.storbinary('STOR {}'.format(self.fileName), self.file)
            self.file.close()
            session.quit()
            self.throwError.emit(
                "'{}' file sent successfully!".format(self.fileName))
            self.startTelemetry.emit()
        except:
            self.throwError.emit("Server is not responding!")


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
            self.setInfo("'{}' {}".format(self.fileName, "file selected!"))

        elif self.file.isEmpty() and self.isFileSelected:
            self.interface.fileNameLineEdit.setText((self.fileName))
            self.isFileSelected = True
            self.setInfo("'{}' {}".format(self.fileName, "old file selected!"))

        else:
            self.interface.fileNameLineEdit.setText((self.fileName))
            self.isFileSelected = False
            self.setInfo("File not selected!")

    def sendVideo(self):
        if self.isFileSelected:
            self.interface.sentDataButton.setEnabled(False)
            css = "QPushButton{border-radius:3px;font-size:18px;border-radius:4px;padding:0px;}QPushButton:hover{background-color: #646464;}"
            self.interface.sentDataButton.setStyleSheet(css)
            self.interface.sentDataButton.setText("Sending...")
            self.thread = DataTransferWorker()
            self.thread.daemon = True
            self.thread.finished.connect(self.setLastInfos)
            self.thread.throwError.connect(self.setInfo)
            self.thread.startTelemetry.connect(self.startTelemetryConnection)
            if self.file.isEmpty():
                self.thread.filePath = self.oldFilePath
            else:
                self.thread.filePath = self.filePath
            self.thread.fileName = self.fileName
            self.thread.start()
        else:
            self.setInfo("Please select file first!")

    def setLastInfos(self):
        self.setInfo("Connection closed!")
        self.interface.sentDataButton.setEnabled(True)
        css = "QPushButton{border-radius:3px;font-size:18px;border-radius:4px;padding:0px;}QPushButton:hover{background-color: #4363d8;}"
        self.interface.sentDataButton.setStyleSheet(css)
        self.interface.sentDataButton.setText("Sent")

    def setInfo(self, msg):
        self.interface.infoScreen.insertPlainText(
            "Data Transfer: {}\n".format(msg))
        self.interface.infoScreen.ensureCursorVisible()

    def startTelemetryConnection(self):
        self.interface.esp_ip_lineEdit.setText(appConfig["ESP_IP_ADDRESS"])
        self.interface.startTelemetryConnection()
