# Import PyQtGraph Module
# Import PyQtGraph Module

import pyqtgraph as pg

# Import QtGui from the PyQtGraph Module

from pyqtgraph.Qt import QtGui


# Generate x-axis values

x = range(0, 10)

# Generate y-axis values

y = [3, 7, 5, 11, 8, 13, 9, 16, 15, 12]


# Initialize the plot

plt = pg.plot()

# Set the label for x axis

plt.setLabel('bottom', 'X-axis Values')

# Set the label for y-axis

plt.setLabel('left', 'Y-axis Values')

# Set horizontal range

plt.setXRange(0, 10)

# Set vertical range

plt.setYRange(0, 20)

# Set the title of the graph

plt.setTitle("Line Graph with styling and marker")


# Set the background color

plt.setBackground(None)

# Set the plot values with pen color and width

line = plt.plot(x, y, pen=pg.mkPen('r', width=6), symbol='o', symbolPen='b', symbolSize=20)

# Add legend

plt.addLegend()

# Show grids

plt.showGrid(x=True, y=True)


# Main method

if __name__ == '__main__':


    # Import sys module

    import sys


    # Start Qt event loop unless running in interactive mode

    if sys.flags.interactive != 1:

        QtGui.QApplication.instance().exec_()



# Main method

if __name__ == '__main__':


    # Import sys module

    import sys


    # Start Qt event loop unless running in interactive mode

    if sys.flags.interactive != 1:

        QtGui.QApplication.instance().exec_()