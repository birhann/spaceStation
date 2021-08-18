from http.client import PRECONDITION_FAILED
from os import pardir
import sys
from typing import Text
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from random import randint, uniform
from multiprocessing import Process, Queue, Pipe
import pyqtgraph as pg
import numpy as np
import time

from pyqtgraph.Qt import PYQT4

from config import appConfig, graphAxisRanges, simulationConf
from pyqtgraph.metaarray.MetaArray import axis
pg.setConfigOption('background', None)


class SimulationWorker(QThread):
    updateTemperatureGraph = pyqtSignal(list, list, object)
    updateHeightGraph = pyqtSignal(list, list, object)
    updateVoltageGraph = pyqtSignal(list, list, object)
    updatePressureGraph = pyqtSignal(list, list, object)
    updateDescentRateGraph = pyqtSignal(list, list, object)
    updateRollingCountGraph = pyqtSignal(list, list, object)
    simulationWorkerStatus = True
    counter = 0

    def run(self):
        self.createAxises()
        while self.counter < simulationConf["PROC_TIME"]:
            self.counter += 1

            self.temperatureGraph()
            self.heightGraph()
            self.voltageGraph()
            self.pressureGraph()
            self.descentRateGraph()
            self.rollingCountGraph()

            time.sleep(simulationConf["INTERVAL"])

    def createAxises(self):
        temperatureGraphX = None
        temperatureGraphY = None

        heightGraphX = None
        heightGraphY = None

        voltageGraphX = None
        voltageGraphY = None

        pressureGraphX = None
        pressureGraphY = None

        descentRateGraphX = None
        descentRateGraphY = None

        rollingCountGraphX = None
        rollingCountGraphY = None

    def temperatureGraph(self):
        self.temperatureGraphlastX = self.temperatureGraphX[-1] + 1
        self.temperatureGraphX.append(self.temperatureGraphlastX)
        self.temperatureGraphY.append(
            randint(graphAxisRanges["TEMPERATURE"]["MIN"], graphAxisRanges["TEMPERATURE"]["MAX"]))
        self.updateTemperatureGraph.emit(
            self.temperatureGraphX, self.temperatureGraphY, self.temperatureGraphlastX)

    def heightGraph(self):
        self.heightGraphlastX = self.heightGraphX[-1] + 1
        self.heightGraphX.append(self.heightGraphlastX)
        self.heightGraphY.append(
            randint(graphAxisRanges["HEIGHT"]["MIN"], graphAxisRanges["HEIGHT"]["MAX"]))
        self.updateHeightGraph.emit(
            self.heightGraphX, self.heightGraphY, self.heightGraphlastX)

    def voltageGraph(self):
        self.voltageGraphlastX = self.voltageGraphX[-1] + 1
        self.voltageGraphX.append(self.voltageGraphlastX)
        self.voltageGraphY.append(round(uniform(
            graphAxisRanges["VOLTAGE"]["MIN"],
            graphAxisRanges["VOLTAGE"]["MAX"]), 5))
        self.updateVoltageGraph.emit(
            self.voltageGraphX, self.voltageGraphY, self.voltageGraphlastX)

    def pressureGraph(self):
        self.pressureGraphlastX = self.pressureGraphX[-1] + 1
        self.pressureGraphX.append(self.pressureGraphlastX)
        self.pressureGraphY.append(round(uniform(
            graphAxisRanges["PRESSURE"]["MIN"],
            graphAxisRanges["PRESSURE"]["MAX"]), 2))
        self.updatePressureGraph.emit(
            self.pressureGraphX, self.pressureGraphY, self.pressureGraphlastX)

    def descentRateGraph(self):
        self.descentRateGraphlastX = self.descentRateGraphX[-1] + 1
        self.descentRateGraphX.append(self.descentRateGraphlastX)
        self.descentRateGraphY.append(round(uniform(
            graphAxisRanges["DESCENT_RATE"]["MIN"],
            graphAxisRanges["DESCENT_RATE"]["MAX"]), 2))
        self.updateDescentRateGraph.emit(
            self.descentRateGraphX, self.descentRateGraphY, self.descentRateGraphlastX)

    def rollingCountGraph(self):
        self.rollingCountGraphlastX = self.rollingCountGraphX[-1] + 1
        self.rollingCountGraphX.append(self.rollingCountGraphlastX)
        self.rollingCountGraphY.append(round(uniform(
            graphAxisRanges["ROLLING_COUNT"]["MIN"],
            graphAxisRanges["ROLLING_COUNT"]["MAX"]), 2))
        self.updateRollingCountGraph.emit(
            self.rollingCountGraphX, self.rollingCountGraphY, self.rollingCountGraphlastX)


class TelemetryWorker(QThread):
    updateTemperatureGraph = pyqtSignal(list, list, object)
    updateHeightGraph = pyqtSignal(list, list, object)
    updateVoltageGraph = pyqtSignal(list, list, object)
    updatePressureGraph = pyqtSignal(list, list, object)
    updateDescentRateGraph = pyqtSignal(list, list, object)
    updateRollingCountGraph = pyqtSignal(list, list, object)
    simulationWorkerStatus = True
    telemetryObject = None
    counter = 0
    graphControl = True

    def run(self):
        self.createAxises()
        while self.graphControl:
            self.counter += 1
            self.temperatureGraph()
            self.pressureGraph()
            self.voltageGraph()
            self.heightGraph()
            self.descentRateGraph()
            self.rollingCountGraph()
            time.sleep(simulationConf["INTERVAL"])

    def createAxises(self):
        temperatureGraphX = None
        temperatureGraphY = None

        heightGraphX = None
        heightGraphY = None

        voltageGraphX = None
        voltageGraphY = None

        pressureGraphX = None
        pressureGraphY = None

        descentRateGraphX = None
        descentRateGraphY = None

        rollingCountGraphX = None
        rollingCountGraphY = None

    def temperatureGraph(self):
        self.temperatureGraphlastX = self.temperatureGraphX[-1] + 1
        self.temperatureGraphX.append(self.temperatureGraphlastX)
        # print(self.telemetryObject.telemetryData)
        if self.telemetryObject.webSocketCon:
            self.temperatureGraphY.append(float(
                self.telemetryObject.telemetryData["temperature"]))
        else:
            self.temperatureGraphY.append(0)
        self.updateTemperatureGraph.emit(
            self.temperatureGraphX, self.temperatureGraphY, self.temperatureGraphlastX)

    def pressureGraph(self):
        self.pressureGraphlastX = self.pressureGraphX[-1] + 1
        self.pressureGraphX.append(self.pressureGraphlastX)
        if self.telemetryObject.webSocketCon:
            self.pressureGraphY.append(float(
                self.telemetryObject.telemetryData["pressure"]))
        else:
            self.pressureGraphY.append(0)
        self.updatePressureGraph.emit(
            self.pressureGraphX, self.pressureGraphY, self.pressureGraphlastX)

    def voltageGraph(self):
        self.voltageGraphlastX = self.voltageGraphX[-1] + 1
        self.voltageGraphX.append(self.voltageGraphlastX)
        if self.telemetryObject.webSocketCon:
            self.voltageGraphY.append(float(
                self.telemetryObject.telemetryData["voltage"]))
        else:
            self.voltageGraphY.append(0)
        self.updateVoltageGraph.emit(
            self.voltageGraphX, self.voltageGraphY, self.voltageGraphlastX)

    def heightGraph(self):
        self.heightGraphlastX = self.heightGraphX[-1] + 1
        self.heightGraphX.append(self.heightGraphlastX)
        if self.telemetryObject.webSocketCon:
            self.heightGraphY.append(
                float(self.telemetryObject.telemetryData["height"]))
        else:
            self.heightGraphY.append(0)
        self.updateHeightGraph.emit(
            self.heightGraphX, self.heightGraphY, self.heightGraphlastX)

    def descentRateGraph(self):
        self.descentRateGraphlastX = self.descentRateGraphX[-1] + 1
        self.descentRateGraphX.append(self.descentRateGraphlastX)
        if self.telemetryObject.webSocketCon:
            self.descentRateGraphY.append(
                float(self.telemetryObject.telemetryData["descentRate"]))
        else:
            self.descentRateGraphY.append(0)
        self.updateDescentRateGraph.emit(
            self.descentRateGraphX, self.descentRateGraphY, self.descentRateGraphlastX)

    def rollingCountGraph(self):
        self.rollingCountGraphlastX = self.rollingCountGraphX[-1] + 1
        self.rollingCountGraphX.append(self.rollingCountGraphlastX)
        if self.telemetryObject.webSocketCon:
            # self.rollingCountGraphY.append(
            #     float(self.telemetryObject.telemetryData["rollingCount"]))
            self.rollingCountGraphY.append(0)
        else:
            self.rollingCountGraphY.append(0)
        self.updateRollingCountGraph.emit(
            self.rollingCountGraphX, self.rollingCountGraphY, self.rollingCountGraphlastX)


class Graph():
    def __init__(self, GUI, TELEMETRY):
        self.interface = GUI
        self.telemetryObject = TELEMETRY
        self.SEC_AXIS_RANGE = graphAxisRanges["SEC_AXIS_RANGE"]
        self.createGraphics()
        self.startGraphicWithThreads()

    def createGraphics(self):
        self.createAxisLabels()
        self.createPlotWidgets()

    def createAxisLabels(self):
        self.interface.temperatureGraph.setLabel(
            axis='left', text='Temperature (°C)')
        self.interface.temperatureGraph.setLabel(
            axis='bottom', text='Time (sec)')

        self.interface.heightGraph.setLabel(
            axis="left", text="Height (m)")
        self.interface.heightGraph.setLabel(
            axis="bottom", text="Time (sec)")

        self.interface.voltageGraph.setLabel(
            axis="left", text="Voltage (V)")
        self.interface.voltageGraph.setLabel(
            axis="bottom", text="Time (sec)")

        self.interface.pressureGraph.setLabel(
            axis="left", text="Pressure (Pa)")
        self.interface.pressureGraph.setLabel(
            axis="bottom", text="Time (sec)")

        self.interface.descentRateGraph.setLabel(
            axis="left", text="Descent Rate (m/s)")
        self.interface.descentRateGraph.setLabel(
            axis="bottom", text="Time (sec)")

        self.interface.rollingCountGraph.setLabel(
            axis="left", text="Rolling Count")
        self.interface.rollingCountGraph.setLabel(
            axis="bottom", text="Time (sec)")

    def createPlotWidgets(self):
        self.pen = pg.mkPen(color=(255, 255, 244))

        # TEMPERATURE
        self.temperatureGW = self.interface.temperatureGraph
        self.temperatureX = list(range(2))
        self.temperatureY = [
            randint(graphAxisRanges["TEMPERATURE"]["MIN"],
                    graphAxisRanges["TEMPERATURE"]["MAX"]) for _ in range(2)]
        # self.temperatureY = [0, 0]
        self.temperatureDataLine = self.temperatureGW.plot(
            self.temperatureX, self.temperatureY, pen=self.pen)
        self.temperatureGW.setXRange(0, self.SEC_AXIS_RANGE)

        # HEIGHT
        self.heightGW = self.interface.heightGraph
        self.heightX = list(range(2))
        self.heightY = [
            randint(graphAxisRanges["HEIGHT"]["MIN"],
                    graphAxisRanges["HEIGHT"]["MAX"]) for _ in range(2)]
        # self.heightY = [0, 0]
        self.heightDataLine = self.heightGW.plot(
            self.heightX, self.heightY, pen=self.pen)
        self.heightGW.setXRange(0, self.SEC_AXIS_RANGE)

        # VOLTAGE
        self.voltageGW = self.interface.voltageGraph
        self.voltageX = list(range(2))
        self.voltageY = [round(uniform(
            graphAxisRanges["VOLTAGE"]["MIN"],
            graphAxisRanges["VOLTAGE"]["MAX"]), 5) for _ in range(2)]
        # self.voltageY = [0, 0]
        self.voltageDataLine = self.voltageGW.plot(
            self.voltageX, self.voltageY, pen=self.pen)
        self.voltageGW.setXRange(0, self.SEC_AXIS_RANGE)

        # PRESSURE
        self.pressureGW = self.interface.pressureGraph
        self.pressureX = list(range(2))
        self.pressureY = [round(uniform(
            graphAxisRanges["PRESSURE"]["MIN"],
            graphAxisRanges["PRESSURE"]["MAX"]), 2) for _ in range(2)]
        # self.pressureY = [0, 0]
        self.pressureDataLine = self.pressureGW.plot(
            self.pressureX, self.pressureY, pen=self.pen)
        self.pressureGW.setXRange(0, self.SEC_AXIS_RANGE)

        # DESCENT_RATE
        self.descentRateGW = self.interface.descentRateGraph
        self.descentRateX = list(range(2))
        self.descentRateY = [round(uniform(
            graphAxisRanges["DESCENT_RATE"]["MIN"],
            graphAxisRanges["DESCENT_RATE"]["MAX"]), 2) for _ in range(2)]
        # self.descentRateY = [0, 0]
        self.descentRateDataLine = self.descentRateGW.plot(
            self.descentRateX, self.descentRateY, pen=self.pen)
        self.descentRateGW.setXRange(0, self.SEC_AXIS_RANGE)

        # ROLLING_COUNT
        self.rollingCountGW = self.interface.rollingCountGraph
        self.rollingCountX = list(range(2))
        self.rollingCountY = [round(uniform(
            graphAxisRanges["ROLLING_COUNT"]["MIN"],
            graphAxisRanges["ROLLING_COUNT"]["MAX"]), 2) for _ in range(2)]
        # self.rollingCountY = [0, 0]
        self.rollingCountDataLine = self.rollingCountGW.plot(
            self.rollingCountX, self.rollingCountY, pen=self.pen)
        self.rollingCountGW.setXRange(0, self.SEC_AXIS_RANGE)

    def startGraphicWithThreads(self):
        if appConfig["GRAPHIC_SIMULATION"]:
            self.mapStatus = True
            print("Graph Simulation active!")

            self.thread = SimulationWorker()
            self.thread.daemon = True

            # temperature
            self.thread.temperatureGraphX, self.thread.temperatureGraphY = self.temperatureX, self.temperatureY
            self.thread.updateTemperatureGraph.connect(
                self.updateTemperature)

            # height
            self.thread.heightGraphX, self.thread.heightGraphY = self.heightX, self.heightY
            self.thread.updateHeightGraph.connect(
                self.updateHeight)

            # voltage
            self.thread.voltageGraphX, self.thread.voltageGraphY = self.voltageX, self.voltageY
            self.thread.updateVoltageGraph.connect(
                self.updateVoltage)

            # pressure
            self.thread.pressureGraphX, self.thread.pressureGraphY = self.pressureX, self.pressureY
            self.thread.updatePressureGraph.connect(
                self.updatePressure)

            # descent_rate
            self.thread.descentRateGraphX, self.thread.descentRateGraphY = self.descentRateX, self.descentRateY
            self.thread.updateDescentRateGraph.connect(
                self.updateDescentRate)

            # rolling_count
            self.thread.rollingCountGraphX, self.thread.rollingCountGraphY = self.rollingCountX, self.rollingCountY
            self.thread.updateRollingCountGraph.connect(
                self.updateRollingCount)

            self.thread.start()
        else:
            print("Telemetry Graph active!")
            self.thread = TelemetryWorker()
            self.thread.daemon = True
            self.thread.telemetryObject = self.telemetryObject
            # temperature
            self.thread.temperatureGraphX, self.thread.temperatureGraphY = self.temperatureX, self.temperatureY
            self.thread.updateTemperatureGraph.connect(
                self.updateTemperature)
            # voltage
            self.thread.voltageGraphX, self.thread.voltageGraphY = self.voltageX, self.voltageY
            self.thread.updateVoltageGraph.connect(
                self.updateVoltage)
            # pressure
            self.thread.pressureGraphX, self.thread.pressureGraphY = self.pressureX, self.pressureY
            self.thread.updatePressureGraph.connect(
                self.updatePressure)
            # height
            self.thread.heightGraphX, self.thread.heightGraphY = self.heightX, self.heightY
            self.thread.updateHeightGraph.connect(
                self.updateHeight)
            # descent_rate
            self.thread.descentRateGraphX, self.thread.descentRateGraphY = self.descentRateX, self.descentRateY
            self.thread.updateDescentRateGraph.connect(
                self.updateDescentRate)
            # rolling_count
            self.thread.rollingCountGraphX, self.thread.rollingCountGraphY = self.rollingCountX, self.rollingCountY
            self.thread.updateRollingCountGraph.connect(
                self.updateRollingCount)

            self.thread.start()

    def updateTemperature(self, x, y, lastX):
        self.temperatureDataLine.setData(x, y)
        self.temperatureGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.temperatureLabel.setText(str(y[-1]) + " °C")

    def updateHeight(self, x, y, lastX):
        self.heightDataLine.setData(x, y)
        self.heightGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.heightLabel.setText(str(y[-1]) + " m")

    def updateVoltage(self, x, y, lastX):
        self.voltageDataLine.setData(x, y)
        self.voltageGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.voltageLabel.setText(str(y[-1]) + " V")

    def updatePressure(self, x, y, lastX):
        self.pressureDataLine.setData(x, y)
        self.pressureGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.pressureLabel.setText(str(y[-1]) + " bar")

    def updateDescentRate(self, x, y, lastX):
        self.descentRateDataLine.setData(x, y)
        self.descentRateGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.descentRateLabel.setText(str(y[-1]) + " m/s")

    def updateRollingCount(self, x, y, lastX):
        self.rollingCountDataLine.setData(x, y)
        self.rollingCountGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.rollingCountLabel.setText(str(y[-1]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Graph()
    win.show()
    sys.exit(app.exec())
