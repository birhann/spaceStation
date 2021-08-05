import sys
from PyQt5.QtWidgets import QApplication
from components import turksatMuy

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = turksatMuy.TurksatMuy()
    window.show()
    sys.exit(app.exec_())