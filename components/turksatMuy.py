import sys
from time import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox
from PyQt5 import QtCore

from templates.Ui_MainGUI import Ui_MainGUI
from components.camera import Camera
from components.gps import LiveMap
from components.graphics import Graph
from components.telemetry import TelemetryObject
from components.dataTransfer import SendingVideo
from config import appConfig


class TurksatMuy(QMainWindow, Ui_MainGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.telemetryConnection = False
        #  hiding title bar and setting position for window
        self.oldPos = self.pos()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # signals
        self.button_max_min.clicked.connect(self.maximized_minimized)
        self.button_close.clicked.connect(self.closeWindow)
        self.button_minimize.clicked.connect(self.showMinimized)
        # self.startCameraButton.clicked.connect(self.startCamera)
        self.telemetryConButton.clicked.connect(self.startTelemetryConnection)
        self.finishButton.clicked.connect(self.finishEsp)

        # # common operations
        # self.cameraViewerLabel.hide()

        # objects
        self.videoTransferObject = SendingVideo(self)
        if not appConfig["GRAPHIC_SIMULATION"]:
            self.infoScreen.clear()

    def startTelemetryConnection(self):
        if self.esp_ip_lineEdit.text() != "" and not appConfig["GRAPHIC_SIMULATION"]:
            if self.telemetryConnection:
                self.TelemetryObject.stopTelemetry()
                self.telemetryConnection = self.TelemetryObject.webSocketCon
                self.telemetryConButton.setEnabled(True)
                css = "color:#fff;background-color:rgb(17, 199, 14);"
                self.telemetryConButton.setStyleSheet(css)
                self.telemetryConButton.setText("Connect")
            else:
                self.CameraObject = Camera(self)
                self.CameraObject.startVideo()
                self.TelemetryObject = TelemetryObject(self)
                self.telemetryConButton.setEnabled(False)
                css = "background-color:#0d9f0a;color:#f9f9f9"
                self.telemetryConButton.setStyleSheet(css)
                self.setInfo("Trying to connect to server..")
        else:
            self.setInfo("The simulations are active!")
            css = "background-color:#b9b921;color:#f9f9f9"
            self.telemetryConButton.setStyleSheet(css)
            self.telemetryConButton.setText("Connected!")
            self.telemetryConButton.setEnabled(False)

            self.GpsObject = LiveMap(self, None)
            self.GraphObject = Graph(self, None)

            self.CameraObject = Camera(self)
            self.CameraObject.startVideo()

    def maximized_minimized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def finishEsp(self):
        self.TelemetryObject.finishControlFunc()
        self.finishButton.setEnabled(False)
        self.setInfo("Trying to close connection..")

    def setInfo(self, msg):
        self.infoScreen.insertPlainText(
            "Telemetry: {}\n".format(msg))
        self.infoScreen.ensureCursorVisible()

    def closeWindow(self):
        if self.confirm(
                "Hoop", 'Programı sonlandırmak istediğinize emin misiniz'):
            sys.exit()
        else:
            pass

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def confirm(self, baslik="Hoop", soru="Bu işlemi yapmak istediğinizden emin misiniz?"):
        box = QMessageBox()
        # box.setWindowIcon(QtGui.QIcon('components/emin_misiniz.png'))
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle(baslik)
        box.setText(soru)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Evet')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('İptal')
        box.exec_()
        if box.clickedButton() == buttonY:
            return True
        elif box.clickedButton() == buttonN:
            return False

    def startCamera(self):
        self.CameraObject.startVideo()
        self.cameraViewerLabel.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TurksatMuy()
    win.show()
    sys.exit(app.exec())
