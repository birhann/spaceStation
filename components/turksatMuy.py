import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox
from PyQt5 import QtCore
from templates.Ui_MainGUI import Ui_MainGUI


class TurksatMuy(QMainWindow, Ui_MainGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # setting position for window and hiding title bar
        self.oldPos = self.pos()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # title bar operations
        self.button_max_min.clicked.connect(self.maximized_minimized)
        self.button_close.clicked.connect(self.closeWindow)
        self.button_minimize.clicked.connect(self.showMinimized)

    def maximized_minimized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def closeWindow(self):
        cevap = self.confirm(
            "Hoop", 'Programı sonlandırmak istediğinize emin misiniz')
        if cevap:
            sys.exit()
        else:
            pass

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def confirm(self, baslik="Hoop", soru="Bu işlemi yapmak istediğinizden emin misiniz?"):
        box = QMessageBox()
        # box.setWindowIcon(QtGui.QIcon('components/emin_misiniz.png'))
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle(baslik)
        box.setText(soru)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Evet')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('İptal')
        box.exec_()
        if box.clickedButton() == buttonY:
            return True
        elif box.clickedButton() == buttonN:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TurksatMuy()
    win.show()
    sys.exit(app.exec())
