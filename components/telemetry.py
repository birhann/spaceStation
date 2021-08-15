import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time
import csv
import re
import websocket
import socket
from components.graphics import Graph
from components.gps import LiveMap
from config import appConfig


class Worker(QThread):
    receivedtel = pyqtSignal(list, object)
    connectionControl = pyqtSignal(object)
    setInfo = pyqtSignal(str)
    webSocketCon = False
    graphControl = True
    finishControl = False

    def run(self):
        UDP_IP_ADDRESS = appConfig["UDP_IP_ADDRESS"]
        ESP_IP_ADDRESS = appConfig["ESP_IP_ADDRESS"]
        UDP_PORT_NO = 44444
        try:
            serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
            self.webSocketCon = True
            Message = "#ESP_DONE#"
            Message2 = "@@@magnet0"
            serverSock.sendto(bytes(Message, encoding='utf8'),
                              (ESP_IP_ADDRESS, UDP_PORT_NO))
            while True:
                data, addr = serverSock.recvfrom(1024)
                if(data != ""):
                    self.telemetry = [i[1:-1].strip()
                                      for i in data.decode("utf-8").split(",")[0:-1]]
                    self.receivedtel.emit(self.telemetry, self.webSocketCon)

                    if self.graphControl:
                        self.graphControl = False
                        self.connectionControl.emit(self.webSocketCon)
                    if self.finishControl:
                        print("evet")
                        serverSock.sendto(bytes("FINISH", encoding='utf8'),
                                          (ESP_IP_ADDRESS, UDP_PORT_NO))
                        self.finishControl = False
                        self.setInfo.emit("Server connection closed!")
                else:
                    break

            self.webSocketCon = False
            self.connectionControl.emit(self.webSocketCon)

        except:
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
        self.finishControl = False

    def finishControlFunc(self):
        self.thread.finishControl = True

    def startTelemetry(self):
        try:
            self.thread = Worker()
            self.thread.daemon = True
            self.thread.receivedtel.connect(self.setTelemetry)
            self.thread.connectionControl.connect(
                self.webSocketConnectionControl)
            self.thread.setInfo.connect(self.setInfo)
            self.thread.finished.connect(self.setLastInfos)
            self.thread.start()
        except:
            self.setInfo(Exception)

    def stopTelemetry(self):
        self.thread.ws.close()

    def setLastInfos(self):
        self.webSocketCon = False
        self.setInfo("Telemetry Connection is Over!")

    def webSocketConnectionControl(self, is_connected):
        self.webSocketCon = is_connected
        if self.webSocketCon:
            self.setInfo("Telemetry Connection Successful!")
            self.interface.telemetryConButton.setEnabled(False)
            css = "QPushButton{background-color:rgb(17, 199, 14);border-radius:5px;color:#fff;"
            self.interface.telemetryConButton.setStyleSheet(css)
            self.interface.telemetryConButton.setText("Connected!")
            self.GraphObject = Graph(
                self.interface, self.interface.TelemetryObject)
            self.GpsObject = LiveMap(
                self.interface, self.interface.TelemetryObject)
        else:
            self.setInfo("Telemetry Connection Failed!")
            self.interface.telemetryConButton.setEnabled(True)
            css = "QPushButton{background-color: rgb(17, 199, 14)} QPushButton:hover{background-color: rgb(13, 159, 10)}"
            self.interface.telemetryConButton.setStyleSheet(css)
            self.interface.telemetryConButton.setText("Connect")

    def setInfo(self, msg):
        self.interface.infoScreen.insertPlainText(
            "Telemetry: {}\n".format(msg))
        self.interface.infoScreen.ensureCursorVisible()

    def setTelemetry(self, telemetrys, webSocketCon):
        self.webSocketCon = webSocketCon
        self.telemetryData = {
            'teamNumber': telemetrys[0][1:-1],
            'packageNo': telemetrys[1],
            'sendingTime': telemetrys[2],
            'hour': telemetrys[3],
            'pressure': telemetrys[4],
            'height': telemetrys[5],
            'descentRate': telemetrys[6],
            'temperature': telemetrys[7],
            'voltage': telemetrys[8],
            'latitude': telemetrys[9],
            'longitude': telemetrys[10],
            'altitude': telemetrys[11],
            'satelliteStatus': telemetrys[12],
            'pitch': telemetrys[13],
            'roll': telemetrys[14],
            'yaw': telemetrys[15],
            'rollingCount': telemetrys[16],
            'transferringStatus': telemetrys[17]
        }
        # print(self.telemetryData, "\n")

        self.interface.teamNumberLabel.setText(
            str(self.telemetryData['teamNumber']))

        self.interface.packageNoLabel.setText(
            str(self.telemetryData['packageNo']))

        self.interface.hourLabel.setText(
            str(self.telemetryData['sendingTime']))

        self.interface.satelliteStatusLabel.setText(
            str(self.telemetryData['satelliteStatus']))

        self.interface.descentRateLabel.setText(
            str(self.telemetryData['descentRate']))

        self.interface.latitudeLabel.setText(
            str(self.telemetryData['latitude']))

        self.interface.longitudeLabel.setText(
            str(self.telemetryData['longitude']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TelemetryObject()
    w.show()
    sys.exit(app.exec_())
