import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from numpy.core.fromnumeric import repeat

import pyqtgraph as pg
import numpy as np
import time
import threading
import random

pg.setConfigOption('background', None)
# pg.setConfigOption('foreground', 'k')


class Graph():
    def __init__(self, GUI):
        self.interface = GUI
        self.telemtryStatus = True
        self.drawGraph()

    def repeat(self, graph):
        while True:
            randnums = np.random.randint(0, 100, 100)
            graph.setData(np.arange(start=0, stop=100, step=1), randnums)
            time.sleep(1)

    def drawGraph(self):
        if self.telemtryStatus:
            g1 = Grafik(self.interface.temperatureGraph)

            thread1 = threading.Thread(target=g1.update_plot_data, daemon=True)
            thread1.start()
            # self.temperature = self.interface.temperatureGraph.addPlot()
            # g6 = self.temperature.plot(np.random.normal(
            #     size=100), symbol='o', symbolSize=10, pen=pg.mkPen('k', width=2))

            # self.temperature.setYRange(0, 100)
            # self.temperature.setXRange(0, 100)
            # thread = threading.Thread(
            #     target=self.repeat, args=(g6,), daemon=True)
            # thread.start()


class Grafik():
    def __init__(self, ui_widget):
        self.x = list(range(300))
        self.y = [random.randint(0, 10) for _ in range(300)]
        pen = pg.mkPen(color=(255, 255, 255), width=2)

        self.addplotDegiskeni = ui_widget.addPlot(title="Temperature")
        self.plotDegiskeni = self.addplotDegiskeni.plot(
            self.x, self.y, pen=pen)

    def update_plot_data(self):

        self.plotDegiskeni.clear()
        while True:
            self.x = self.x[1:]
            self.x.append(self.x[0] + 1)
            self.y = self.y[1:]
            self.y.append(random.randint(0, 10))
            # print(self.x, self.y)
            self.plotDegiskeni.setData(self.x, self.y)

            time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Graph()
    win.show()
    sys.exit(app.exec())
