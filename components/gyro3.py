from OpenGL.lazywrapper import lazy
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial


class Pencere(QWidget):
    def __init__(self):
        super().__init__()

        video_flags = OPENGL | DOUBLEBUF
        pygame.init()
        screen = pygame.display.set_mode((640, 480), video_flags)
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(screen)
        # self.setLayout(self.layout)


app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())
