import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from templates.Ui_MainGUI import Ui_MainGUI


class TurksatMuy(QMainWindow, Ui_MainGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TurksatMuy()
    win.show()
    sys.exit(app.exec())
