import cv2
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
# from Ui_cameraViewer import Ui_Form
from config import appConfig

import cv2


class EspWorker(QThread):
    setView = pyqtSignal(QImage)
    workerStatus = True

    def run(self):
        cap = cv2.VideoCapture(
            "http://{}:81/stream".format(appConfig["ESP_IP_ADDRESS"]))
        try:
            while True:
                ret, frame = cap.read()
                # cv2.imshow('frame', frame)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.flip(rgbImage, 1)  # mirroring
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                image = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
                self.setView.emit(image)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        except:
            pass
        # cap.release()
        # cv2.destroyAllWindows()
        # self.capture.release()


class EspWorker2(QThread):
    setView = pyqtSignal(QImage)
    workerStatus = True

    def run(self):
        cap = cv2.VideoCapture("http://192.168.137.50:81/stream")
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(
            'Stream.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))
        while True:
            ret, frame = cap.read()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # rgbImage = cv2.flip(rgbImage, 1)  # mirroring
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            image = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
            self.setView.emit(image)
            writer.write(frame)
            # cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # cap.release()
        writer.release()
        # cv2.destroyAllWindows()


class PcCameraWorker(QThread):
    setView = pyqtSignal(QImage)
    workerStatus = True

    def run(self):
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while self.capture.isOpened():
            ret, frame = self.capture.read()
            if self.workerStatus:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage = cv2.flip(rgbImage, 1)  # mirroring
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
            from config import appConfig
            if appConfig["CAMERA_SIMULATION"]:
                self.thread = PcCameraWorker()
            else:
                self.thread = EspWorker()
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
