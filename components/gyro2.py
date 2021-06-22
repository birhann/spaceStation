from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time


class Worker(QThread):
    updateMap = pyqtSignal(object, object)
    workerStatus = True
    counter = 0

    def run(self):
        while self.counter < 55:
            if self.workerStatus:
                pass
                time.sleep(1)
            else:
                break


class GyroState(QWidget):
    def __init__(self, GUI):
        super().__init__()
        self.interface = GUI
