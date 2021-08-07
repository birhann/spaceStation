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
        ws.connect("ws://192.168.27.106")
        print("Connected to WebSocket server")
        while True:
            if self.workerStatus:

                ws.send("Python")
                #time.sleep(20);

                result = ws.recv()
                #print(result)
                #if(result.find(">") == 0):
                #    print("Received: " + result)
                if(result != "" and result != "Python"):
                    #print("Received: " + results)
                    #result = "<62319>,<2>,<00:00:00>,<0.00>,<0.0>,<0.000000>,<0>,<0.91>,<0.000000>,<0.000000>,<0.0>,<BEKLEMEDE>,<0>,<0>,<0>,<DONUS>,<VIDEO>,<0>"
                    telemetrys = re.split(",", result)

                    with open('yeni.csv', mode='w') as yeni_dosya:
                        yeni_yazici = csv.writer(yeni_dosya, delimiter=',',
                                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)

                        yeni_yazici.writerow(telemetrys)

                    for i in range(18):
                        birinci = re.split("<", telemetrys[i])
                        telemetrys.remove(telemetrys[i])
                        telemetrys.insert(i, birinci[1])

                        ikinci = re.split(">", telemetrys[i])
                        telemetrys.remove(telemetrys[i])
                        telemetrys.insert(i, ikinci[0])

                    #print(telemetrys)

                    self.receivedtel.emit(telemetrys)
                self.counter += 1
                time.sleep(1)
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
    #w.show()
    sys.exit(app.exec_())
    