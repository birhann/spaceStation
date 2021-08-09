import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtGui

img = plt.imread("uzay.jpeg")
fig, ax = plt.subplots()
ax.imshow(img, extent=[-5, 80, -5, 30])
plt.show() 



if __name__ == '__main__':


    import sys

    if sys.flags.interactive != 1:

        QtGui.QApplication.instance().exec_()



if __name__ == '__main__':

    import sys

    if sys.flags.interactive != 1:

        QtGui.QApplication.instance().exec_()