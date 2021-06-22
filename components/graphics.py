import sys
from typing import Text
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from random import randint

import pyqtgraph as pg
import numpy as np
import time

from config import appConfig, graphAxisRanges
from pyqtgraph.metaarray.MetaArray import axis
pg.setConfigOption('background', None)


class SimulationWorker(QThread):
    updateTemperatureGraph = pyqtSignal(list, list, object)
    simulationWorkerStatus = True
    counter = 0
    temperatureGraphX = None
    temperatureGraphY = None

    def run(self):
        while self.counter < 10:
            self.counter += 1
            # self.x = self.x[1:]  # Remove the first y element.
            self.temperatureGraphlastX = self.temperatureGraphX[-1] + 1
            self.temperatureGraphX.append(self.temperatureGraphlastX)
            # self.x = self.x[1:]  # Remove the first
            self.temperatureGraphY.append(
                randint(0, graphAxisRanges["TEMPERATURE"]["MAX"]))
            self.updateTemperatureGraph.emit(
                self.temperatureGraphX, self.temperatureGraphY, self.temperatureGraphlastX)
            time.sleep(1)


class Graph():
    def __init__(self, GUI):
        self.interface = GUI
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
        self.pen = pg.mkPen(color=(255, 255, 255))

        # TEMPERATURE
        self.temperatureGW = self.interface.temperatureGraph
        self.temperatureX = list(range(2))
        self.temperatureY = [
            randint(0, graphAxisRanges["TEMPERATURE"]["MAX"]) for _ in range(2)]
        self.temperatureDataLine = self.temperatureGW.plot(
            self.temperatureX, self.temperatureY, pen=self.pen)
        self.temperatureGW.setXRange(0, self.SEC_AXIS_RANGE)

    def startGraphicWithThreads(self):
        if appConfig["GRAPHIC_SIMULATION"]:
            print("hel")
            self.mapStatus = True
            try:
                self.thread = SimulationWorker()
                self.thread.daemon = True

                self.thread.temperatureGraphX, self.thread.temperatureGraphY = self.temperatureX, self.temperatureY
                self.thread.updateTemperatureGraph.connect(
                    self.updateTemperature)

                self.thread.start()
            except:
                print("GRAPH ERRORS:", Exception)
        else:
            print("graphics simulation is deactive")

    def updateTemperature(self, x, y, lastX):
        self.temperatureDataLine.setData(x, y)
        self.temperatureGW.setXRange(
            lastX - self.SEC_AXIS_RANGE, lastX)
        self.interface.temperatureLabel.setText(str(y[-1]) + " °C")
        # self.temperatureGW.setYRange(self.y[-5], self.y[-1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Graph()
    win.show()
    sys.exit(app.exec())
