import sys
import io
from PyQt5 import sip
from PyQt5.QtGui import qRgba
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QThread, pyqtSignal
import folium
import time
import random
from config import simulationConf, appConfig


class Worker(QThread):
    updateMap = pyqtSignal(object, object)
    workerStatus = True
    counter = 0

    def getCoordinates(self):
        # x = random.random()*50.0
        # y = random.random()*50.0 40.76358185278211, 29.90650776805874
        # koceli 40.76358185278211 29.90650776805874
        # 38.76226363276871, 33.661376158029405
        x, y = 38.76226363276871+random.random()*0.0015, 33.661376158029405 + \
            random.random()*0.0015
        return x, y

    def run(self):
        while self.counter < simulationConf["PROC_TIME"]:
            if self.workerStatus:
                x, y = self.getCoordinates()
                self.updateMap.emit(x, y)
                self.counter += 1
                time.sleep(1)
            else:
                break


class TelemetryWorker(QThread):
    updateMap = pyqtSignal(object, object, object)
    workerStatus = True
    telemetryObject = None
    counter = 0

    def getCoordinates(self):
        if bool(self.telemetryObject.telemetryData):
            x = self.telemetryObject.telemetryData["latitude"]
            y = self.telemetryObject.telemetryData[
                'longitude']
            z = self.telemetryObject.telemetryData['altitude']
        else:
            x, y, z = 0, 0, 0
        return x, y, z

    def run(self):
        while self.counter < simulationConf["PROC_TIME"]:
            if self.workerStatus:
                x, y, z = self.getCoordinates()
                self.updateMap.emit(x, y, z)
                self.counter += 1
                time.sleep(1)
            else:
                break


class LiveMap(QWidget):
    def __init__(self, GUI, TELEMETRY):
        super().__init__()
        self.interface = GUI
        self.telemetryObject = TELEMETRY
        self.mapStatus = False
        self.counter = 0
        self.defaultCoordinates = 40.76358185278211, 29.90650776805874

        self.createMap(self.defaultCoordinates)
        self.startLiveMap()

    def createMap(self, coordinates):
        if appConfig["GPS_SIMULATION"]:
            locationValue = (coordinates[0], coordinates[1])
        else:
            locationValue = (0, 0)
        mapObject = folium.Map(
            tiles='CartoDB dark_matter',
            zoom_start=14,
            max_bounds=True,
            location=locationValue
        )
        data = io.BytesIO()
        mapObject.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        self.interface.gpsLayout.addWidget(self.webView)

    def startLiveMap(self):
        if not self.mapStatus:
            self.mapStatus = True
            try:
                if appConfig["GPS_SIMULATION"]:
                    self.thread = Worker()
                    self.thread.daemon = True
                    self.thread.updateMap.connect(self.setCoordinate)
                    self.thread.finished.connect(self.setLastInfos)
                    self.thread.start()
                else:
                    self.thread = TelemetryWorker()
                    self.thread.daemon = True
                    self.thread.telemetryObject = self.telemetryObject
                    self.thread.updateMap.connect(self.setGpsCoordinate)
                    self.thread.finished.connect(self.setLastInfos)
                    self.thread.start()
            except:
                print("LIVE MAP ERROR:", Exception)

        else:
            self.mapStatus = False
            self.thread.workerStatus = False

    def deleteLayout(self, cur_lay):
        # QtGui.QLayout(cur_lay)

        if cur_lay is not None:
            while cur_lay.count():
                item = cur_lay.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(cur_lay)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def setLastInfos(self):
        print("map is over..")

    def setCoordinate(self, x, y):
        # self.webView.deleteLater()
        # self.deleteLayout(self.layout)
        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        mapObject = folium.Map(
            tiles='cartodbdark_matter',
            zoom_start=14,
            max_bounds=True,
            # zoom_control=False,
            scrollWheelZoom=False,
            # dragging=False,
            location=(x, y),
        )

        # folium.Marker(
        #     [38.76226363276871, 33.661376158029405], popup="<i>Ground Station</i>", icon=folium.Icon(color='red', icon='laptop', prefix='fa', icon_color='#FFFFFF')).add_to(mapObject)

        # folium.CircleMarker(
        #     location=[38.76226363276871, 33.661376158029405],
        #     radius=150,
        #     popup='Flight Area',
        #     color='#428bca',
        #     fill=True,
        #     fill_color='#428bca'
        # ).add_to(mapObject)

        self.interface.longitudeLabel.setText(str(x))
        self.interface.latitudeLabel.setText(str(y))
        folium.Marker(
            [x, y], popup="<i>Satellite</i>", icon=folium.Icon(icon='wifi', prefix='fa')).add_to(mapObject)

        data = io.BytesIO()
        mapObject.save(data, close_file=False)

        self.webView.setHtml(data.getvalue().decode())

    def setGpsCoordinate(self, x, y, z):
        mapObject = folium.Map(
            tiles='cartodbdark_matter',
            zoom_start=14,
            max_bounds=True,
            # zoom_control=False,
            scrollWheelZoom=False,
            # dragging=False,
            location=(x, y),
        )
        self.interface.longitudeLabel.setText(str(x))
        self.interface.latitudeLabel.setText(str(y))
        self.interface.altitudeLabel.setText(str(z))
        folium.Marker(
            [x, y], popup="<i>Satellite</i>", icon=folium.Icon(icon='wifi', prefix='fa')).add_to(mapObject)

        data = io.BytesIO()
        mapObject.save(data, close_file=False)

        self.webView.setHtml(data.getvalue().decode())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LiveMap()
    w.show()
    sys.exit(app.exec_())
