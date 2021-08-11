import cv2
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
# from Ui_cameraViewer import Ui_Form
import os
import numpy as np
import cv2
import zipfile


class EspWorker(QThread):
    setView = pyqtSignal(QImage)
    workerStatus = True

    def run(self):
        cap = cv2.VideoCapture("http://192.168.242.251:81/stream")

        while True:
            ret, frame = cap.read()
            # cv2.imshow('frame', frame)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # rgbImage = cv2.flip(rgbImage, 1)  # mirroring
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            image = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
            self.setView.emit(image)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # cap.release()
        # cv2.destroyAllWindows()
        # self.capture.release()


class PcCameraWorker(QThread):
    setView = pyqtSignal(QImage)
    workerStatus = True

    def run(self):
        self.capture = cv2.VideoCapture(
            "http://192.168.43.80:81/stream")

        while self.capture.isOpened():
            ret, frame = self.capture.read()
            if self.workerStatus:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # rgbImage = cv2.flip(rgbImage, 1)  # mirroring
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                image = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
                self.setView.emit(image)
            else:
                break

        self.capture.release()


class Camera():
    def __init__(self, GUI):
        self.interface = GUI
        self.cameraStatus = 0

    def startVideo(self):
        if not self.cameraStatus:
            self.cameraStatus = 1
            self.thread = PcCameraWorker()
            self.thread.daemon = True
            self.thread.setView.connect(self.setImage)
            self.thread.finished.connect(self.finishVideo)
            self.thread.start()
        else:
            self.cameraStatus = 0
            self.thread.workerStatus = False

    def finishVideo(self):
        self.interface.cameraViewerLabel.clear()
        self.interface.cameraViewerLabel.setText("Camera")
        self.interface.cameraViewerLabel.show()

    # @pyqtSlot(QImage)
    def setImage(self, image):
        self.interface.cameraViewerLabel.setPixmap(
            QPixmap.fromImage(image).scaled(self.interface.cameraViewerLabel.frameGeometry().width(),
                                            self.interface.cameraViewerLabel.frameGeometry().height(),
                                            QtCore.Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Camera()
    win.show()
    sys.exit(app.exec())
