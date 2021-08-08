import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time
import csv
import re
import websocket


class Worker(QThread):
    receivedtel = pyqtSignal(object)
    workerStatus = True
    counter = 0

    def run(self):
        ws = websocket.WebSocket()
        ws.connect("ws://192.168.196.106")
        print("Connected to WebSocket server")
        while True:
            if self.workerStatus:
                ws.send("Python")
                result = ws.recv()
                if(result != "" and result != "Python"):
                    telemetrys = re.split(",", result)

                    with open('telemetry.csv', mode='w') as file:
                        writer = csv.writer(file, delimiter=',',
                                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(telemetrys)
                    telemetrys = [i[1:-1] for i in telemetrys]
                    self.receivedtel.emit(telemetrys)
                # time.sleep(1)
            else:
                break
        ws.close()


class Telemetry():
    def __init__(self):
        super().__init__()
        #self.interface = GUI
        self.telStatus = False
        self.counter = 0

        self.startTelemetry()

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

    def setTelemetry(self, tele):
        #global TelemetryData
        TelemetryData = tele
        print(TelemetryData)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Telemetry()
    # w.show()
    sys.exit(app.exec_())
