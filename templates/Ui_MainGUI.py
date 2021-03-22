# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Lenovo\Desktop\KOU\TM MARM-99 2021\turksat-muy-ground-station-2021\templates\MainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainGUI(object):
    def setupUi(self, MainGUI):
        MainGUI.setObjectName("MainGUI")
        MainGUI.resize(788, 680)
        self.centralwidget = QtWidgets.QWidget(MainGUI)
        self.centralwidget.setStyleSheet("margin:0px;\n"
"padding:0px;\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_bar_layout = QtWidgets.QHBoxLayout()
        self.title_bar_layout.setSpacing(0)
        self.title_bar_layout.setObjectName("title_bar_layout")
        self.left_bar = QtWidgets.QFrame(self.centralwidget)
        self.left_bar.setEnabled(True)
        self.left_bar.setMinimumSize(QtCore.QSize(100, 38))
        self.left_bar.setMaximumSize(QtCore.QSize(16777215, 38))
        self.left_bar.setStyleSheet("QFrame{\n"
"background:rgba(0,0,0,0.38);\n"
"}\n"
"QFrame{\n"
"border-radius:none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"background:rgba(0,0,0,0.40);\n"
"}")
        self.left_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_bar.setObjectName("left_bar")
        self.title_bar_layout.addWidget(self.left_bar)
        self.right_bar = QtWidgets.QFrame(self.centralwidget)
        self.right_bar.setEnabled(True)
        self.right_bar.setMinimumSize(QtCore.QSize(180, 38))
        self.right_bar.setMaximumSize(QtCore.QSize(180, 38))
        self.right_bar.setStyleSheet("QFrame{\n"
"background:rgba(0,0,0,0.38);\n"
"}\n"
"QFrame{\n"
"border-radius:none;\n"
"}\n"
"\n"
"QFrame:hover{\n"
"background:rgba(0,0,0,0.40);\n"
"}")
        self.right_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_bar.setObjectName("right_bar")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.right_bar)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_minimize = QtWidgets.QPushButton(self.right_bar)
        self.button_minimize.setMinimumSize(QtCore.QSize(60, 38))
        self.button_minimize.setMaximumSize(QtCore.QSize(60, 38))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.button_minimize.setFont(font)
        self.button_minimize.setStyleSheet("QPushButton{\n"
"background:rgba(0, 0, 0,0.15);\n"
"color:#fff;\n"
"\n"
"border-radius:none;\n"
"\n"
"padding-top:-7px\n"
"}\n"
"\n"
"\n"
"QPushButton:hover{\n"
"background:#e81123;\n"
"color:white\n"
"}")
        self.button_minimize.setObjectName("button_minimize")
        self.horizontalLayout_3.addWidget(self.button_minimize)
        self.button_max_min = QtWidgets.QPushButton(self.right_bar)
        self.button_max_min.setMinimumSize(QtCore.QSize(60, 38))
        self.button_max_min.setMaximumSize(QtCore.QSize(60, 38))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_max_min.setFont(font)
        self.button_max_min.setStyleSheet("QPushButton{\n"
"background:rgba(0, 0, 0,0.15);\n"
"color:#fff;\n"
"\n"
"border-radius:none;\n"
"padding-top:-3px\n"
"}\n"
"\n"
"\n"
"QPushButton:hover{\n"
"background:#e81123;\n"
"color:white\n"
"}")
        self.button_max_min.setObjectName("button_max_min")
        self.horizontalLayout_3.addWidget(self.button_max_min)
        self.button_close = QtWidgets.QPushButton(self.right_bar)
        self.button_close.setMinimumSize(QtCore.QSize(60, 38))
        self.button_close.setMaximumSize(QtCore.QSize(60, 38))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.button_close.setFont(font)
        self.button_close.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.button_close.setStyleSheet("QPushButton{\n"
"background:rgba(0, 0, 0,0.15);\n"
"color:#fff;\n"
"\n"
"border-radius:none;\n"
"}\n"
"\n"
"\n"
"QPushButton:hover{\n"
"background:#e81123;\n"
"color:white\n"
"}")
        self.button_close.setObjectName("button_close")
        self.horizontalLayout_3.addWidget(self.button_close, 0, QtCore.Qt.AlignLeft)
        self.title_bar_layout.addWidget(self.right_bar)
        self.verticalLayout_2.addLayout(self.title_bar_layout)
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setObjectName("main_layout")
        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_layout.setObjectName("top_layout")
        self.port = QtWidgets.QVBoxLayout()
        self.port.setObjectName("port")
        self.top_layout.addLayout(self.port)
        self.data = QtWidgets.QVBoxLayout()
        self.data.setObjectName("data")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.data.addWidget(self.pushButton)
        self.top_layout.addLayout(self.data)
        self.data_transfer = QtWidgets.QVBoxLayout()
        self.data_transfer.setObjectName("data_transfer")
        self.top_layout.addLayout(self.data_transfer)
        self.main_layout.addLayout(self.top_layout, 0, 0, 1, 1)
        self.mid_layout = QtWidgets.QHBoxLayout()
        self.mid_layout.setObjectName("mid_layout")
        self.main_layout.addLayout(self.mid_layout, 1, 0, 1, 1)
        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout.setObjectName("bottom_layout")
        self.main_layout.addLayout(self.bottom_layout, 2, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.main_layout)
        MainGUI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainGUI)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainGUI.setStatusBar(self.statusbar)

        self.retranslateUi(MainGUI)
        QtCore.QMetaObject.connectSlotsByName(MainGUI)

    def retranslateUi(self, MainGUI):
        _translate = QtCore.QCoreApplication.translate
        MainGUI.setWindowTitle(_translate("MainGUI", "TM MARM-99 YER ISTASYONU"))
        self.button_minimize.setText(_translate("MainGUI", "_"))
        self.button_max_min.setText(_translate("MainGUI", "🗖"))
        self.button_close.setText(_translate("MainGUI", "✕"))
        self.pushButton.setText(_translate("MainGUI", "PushButton"))
