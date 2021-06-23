from OpenGL.lazywrapper import lazy
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox
from PyQt5 import QtCore

from Ui_threeD import Ui_Form


class ThreeDGyro(QMainWindow, Ui_Form):
    def __init__(self, gyroWindow):
        super().__init__()
        self.setupUi(self)


video_flags = OPENGL | DOUBLEBUF
pygame.init()
screen = pygame.display.set_mode((640, 480), video_flags)


app = QApplication(sys.argv)
pencere = ThreeDGyro(screen)
pencere.show()
sys.exit(app.exec_())
