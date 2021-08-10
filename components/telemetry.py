import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time
import csv
import re
import websocket


class Worker(QThread):
    receivedtel = pyqtSignal(list, object)
    webSocketCon = False
    workerStatus = True
    counter = 0
    webSocketCon = None

    def run(self):
        ws = websocket.WebSocket()
        ws.connect("ws://192.168.242.250")
        print("Connected to WebSocket server")
        self.webSocketCon = True

        while True:
            if self.workerStatus:
                ws.send("Python")
                result = ws.recv()
                if(result != "" and result != "Python"):
                    telemetrys = re.split(",", result)
                    telemetrys[-1] = telemetrys[-1][0:-2]
                    telemetrys = [i[1:-1]for i in telemetrys]
                    self.receivedtel.emit(telemetrys, self.webSocketCon)
            else:
                break
        ws.close()


class TelemetryObject():
    def __init__(self):
        super().__init__()
        #self.interface = GUI
        self.telemetryData = {}
        self.telStatus = False
        self.counter = 0
        self.startTelemetry()
        self.webSocketCon = False

    def startTelemetry(self):
        if not self.telStatus:
            self.telStatus = True
            try:
                self.thread = Worker()
                self.thread.daemon = True
                self.thread.receivedtel.connect(self.setTelemetry)
                self.thread.finished.connect(self.setLastInfos)
                self.thread.start()
            except:
                print("TELEMETRY ERROR:", Exception)
        else:
            self.telStatus = False
            self.thread.workerStatus = False

    def setLastInfos(self):
        print("telemetry is over..")

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
