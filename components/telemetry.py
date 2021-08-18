import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time
import csv
import re
import websocket
import socket
from components.graphics import Graph
from components.gps import LiveMap, TelemetryWorker
from components.gyro import GyroObject
from config import appConfig


class Worker(QThread):
    receivedtel = pyqtSignal(list, object)
    connectionControl = pyqtSignal(object)
    writeCsvFile = pyqtSignal(list)
    setInfo = pyqtSignal(str)
    webSocketCon = False
    graphControl = True
    finishControl = False
    engineOnControl = False
    engineOffControl = False
    leavePayloadControl = False
    telemetryCsv = []

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
            serverSock.sendto(bytes(Message, encoding='utf8'),
                              (ESP_IP_ADDRESS, UDP_PORT_NO))
            self.characterControl = True
            while True:
                data, addr = serverSock.recvfrom(1024)
                # print("DATA: ", data)
                if(data != ""):
                    self.telemetry = [i[1:-1].strip()
                                      for i in data.decode("utf-8").split(",")[0:-1]]
                    self.telemetryCsv.append(self.telemetry)
                    self.receivedtel.emit(self.telemetry, self.webSocketCon)

                    if self.graphControl:
                        self.graphControl = False
                        self.connectionControl.emit(self.webSocketCon)
                    if self.finishControl:
                        serverSock.sendto(bytes("FINISH", encoding='utf8'),
                                          (ESP_IP_ADDRESS, UDP_PORT_NO))
                        self.finishControl = False
                        self.setInfo.emit("Server connection closed!")
                        break

                    if self.engineOnControl:
                        serverSock.sendto(bytes("@@@engineM", encoding='utf8'),
                                          (ESP_IP_ADDRESS, UDP_PORT_NO))
                        self.setInfo.emit("Engine started!")
                        self.engineOnControl = False

                    if self.engineOffControl:
                        serverSock.sendto(bytes("@@@engine0", encoding='utf8'),
                                          (ESP_IP_ADDRESS, UDP_PORT_NO))
                        self.setInfo.emit("Engine done!")
                        self.engineOffControl = False

                    if self.leavePayloadControl:
                        serverSock.sendto(bytes("@@@magnet0", encoding='utf8'),
                                          (ESP_IP_ADDRESS, UDP_PORT_NO))
                        self.setInfo.emit("Magnet left!")
                        self.leavePayloadControl = False
                else:
                    break
            self.writeCsvFile.emit(self.telemetryCsv)
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
        self.GraphObject.thread.graphControl = False
        print("Telemetry done!")

    def engineControlFunc(self, engineStatus):
        if engineStatus:
            self.thread.engineOffControl = True
        else:
            self.thread.engineOnControl = True

    def leavePayloadControl(self):
        self.thread.leavePayloadControl = True

    def startTelemetry(self):
        try:
            self.thread = Worker()
            self.thread.daemon = True
            self.thread.receivedtel.connect(self.setTelemetry)
            self.thread.writeCsvFile.connect(self.saveCsvFile)
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

    def saveCsvFile(self, datas):
        self.csvFile = open('telemetry.csv', 'w')
        self.writer = csv.writer(self.csvFile)
        self.header = ['TeamNo', 'PackageNo', 'Time', 'Hour', 'Pressure', 'Height', 'DescentRate', 'Temperature', 'Voltage',
                       'Latitude', 'Longitude', 'Altitude', 'Satellitestatus', 'Pitch', 'Roll', 'Yaw', 'RollingCount', 'TransferringStatus']
        self.writer.writerow(self.header)
        for i in datas:
            self.writer.writerow(i)
        self.csvFile.close()

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

            self.gyroThread = GyroObject()
            self.gyroThread.daemon = True
            self.gyroThread.start()

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
        print(telemetrys[0])
        self.webSocketCon = webSocketCon
        self.telemetryData = {
            'teamNumber': 62319,
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

        self.interface.teamNumberLabel.setText(
            str(self.telemetryData['teamNumber']))

        self.interface.packageNoLabel.setText(
            str(self.telemetryData['packageNo']))

        self.interface.dateLabel.setText(
            str(self.telemetryData['sendingTime']))

        self.interface.hourLabel.setText(
            str(self.telemetryData['hour']))

        self.interface.satelliteStatusLabel.setText(
            str(self.telemetryData['satelliteStatus']))

        self.interface.descentRateLabel.setText(
            str(self.telemetryData['descentRate']))

        self.interface.latitudeLabel.setText(
            str(self.telemetryData['latitude']))

        self.interface.longitudeLabel.setText(
            str(self.telemetryData['longitude']))

        self.interface.altitudeLabel.setText(
            str(self.telemetryData['altitude']))

        self.interface.rollingCountLabel.setText(
            str(self.telemetryData['rollingCount']))

        self.interface.pitchLabel.setText(
            str(self.telemetryData['pitch']))

        self.interface.rollLabel.setText(
            str(self.telemetryData['roll']))

        self.interface.yawLabel.setText(
            str(self.telemetryData['yaw']))

        self.setGyroApsis(
            self.telemetryData["pitch"], self.telemetryData["roll"], self.telemetryData["yaw"])

    def setGyroApsis(self, ax, ay, az):
        self.gyroThread.ax = float(int(ax))
        self.gyroThread.ay = float(int(ay))
        self.gyroThread.az = float(int(az))

    def gyroClose(self):
        self.gyroThread.closeControl = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TelemetryObject()
    w.show()
    sys.exit(app.exec_())
