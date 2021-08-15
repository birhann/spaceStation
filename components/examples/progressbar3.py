import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ftplib import FTP
import unicodedata


class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.pyqtSignal(object)

    def run(self):
        self.data_downloaded.emit('Connecting...')

        ftp = FTP('example.com')
        ftp.login(user='user', passwd='password')

        ftp.cwd('/main_directory/')

        self.data_downloaded.emit('Downloading...')

        filename = 'testfile.bin'
        with open(filename, 'wb') as localfile:
            ftp.retrbinary('RETR ' + filename, localfile.write)

        ftp.quit()

        self.data_downloaded.emit('Done')


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.label = QtWidgets.QLabel
        self.button = QtWidgets.QPushButton("Start")
        self.button.clicked.connect(self.start_download)
        layout = QtWidgets.QVBoxLayout
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def start_download(self):
        self.thread = DownloadThread()
        self.thread.data_downloaded.connect(self.on_data_ready)
        self.thread.start()

    def on_data_ready(self, data):
        self.label.setText(unicodedata(data))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
