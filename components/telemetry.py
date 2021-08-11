import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time
import csv
import re
import websocket
from config import appConfig


class Worker(QThread):
    receivedtel = pyqtSignal(list, object)
    connectionControl = pyqtSignal(object)
    webSocketCon = False
    counter = 0

    def run(self):
        ws = websocket.WebSocket()
        ws.connect("ws://{}".format(appConfig['ESP_IP']))
        self.webSocketCon = True
        self.connectionControl.emit(self.webSocketCon)

        while True:
            ws.send("Python")
            result = ws.recv()
            if(result != "" and result != "Python"):
                telemetrys = re.split(",", result)
                telemetrys[-1] = telemetrys[-1][0:-2]
                telemetrys = [i[1:-1]for i in telemetrys]
                self.receivedtel.emit(telemetrys, self.webSocketCon)

        ws.close()
        self.webSocketCon = False
        self.connectionControl.emit(self.webSocketCon)


class TelemetryObject():
    def __init__(self, GUI):
        super().__init__()
        self.interface = GUI
        self.telemetryData = {}
        self.counter = 0
        self.startTelemetry()
        self.webSocketCon = False

    def startTelemetry(self):
        try:
            self.thread = Worker()
            self.thread.daemon = True
            self.thread.receivedtel.connect(self.setTelemetry)
            self.thread.connectionControl.connect(
                self.webSocketConnectionControl)
            self.thread.finished.connect(self.setLastInfos)
            self.thread.start()
        except:
            print("TELEMETRY ERROR:", Exception)

    def setLastInfos(self, is_connected):
        self.webSocketCon = is_connected
        print("Telemetry Connection is Over...")

    def webSocketConnectionControl(self, is_connected):
        self.webSocketCon = is_connected
        if self.webSocketCon:
            print("Telemetry Connection Successful!")
        else:
            print("Telemetry Connection Failed!")

    def setTelemetry(self, telemetrys, webSocketCon):
        self.webSocketCon = webSocketCon
        self.telemetryData = {
            'teamNumber': telemetrys[0],
            'packageNo': telemetrys[1],
            'sendingTime': telemetrys[2],
            'pressure': telemetrys[3],
            'height': telemetrys[4],
            'descentRate': telemetrys[5],
            'temperature': telemetrys[6],
            'voltage': telemetrys[7],
            'latitude': telemetrys[8],
            'longitude': telemetrys[9],
            'altitude': telemetrys[10],
            'satelliteStatus': telemetrys[11],
            'pitch': telemetrys[12],
            'roll': telemetrys[13],
            'yaw': telemetrys[14],
            'rollingCount': telemetrys[15],
            'transferringStatus': telemetrys[16]
        }
        # print(self.telemetryData)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TelemetryObject()
    # w.show()
    sys.exit(app.exec_())
