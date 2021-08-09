import sys
from pyqtgraph.Qt import QtGui
import pyqtgraph

app = QtGui.QApplication(sys.argv)

mw = QtGui.QMainWindow()
mw.resize(800, 800)
mw.setWindowTitle('my qt window')

view = pyqtgraph.GraphicsLayoutWidget()
mw.setCentralWidget(view)
mw.show()

w1 = view.addPlot(title="my plot area")

w1.addLegend(offset=(0, 0))
w1.plot([0, 1, 2, 3, 4], [3, 6, 5, 8, 7],
        pen=pyqtgraph.mkPen(1, width=1), name="foo")
w1.plot([0, 1, 2, 3, 4], [5, 7, 6, 2, 9],
        pen=pyqtgraph.mkPen(2, width=1), name="bar")

axX = w1.getAxis('bottom')
print('x axis range: {}'.format(axX.range))
axY = w1.getAxis('left')
print('x axis range: {}'.format(axY.range))

sys.exit(app.exec_())
