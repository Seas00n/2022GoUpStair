# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1171, 915)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pros.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(430, 10, 281, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 351, 231))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 30, 261, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_port = QtWidgets.QLabel(self.layoutWidget)
        self.label_port.setObjectName("label_port")
        self.horizontalLayout.addWidget(self.label_port)
        self.combo_port = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_port.sizePolicy().hasHeightForWidth())
        self.combo_port.setSizePolicy(sizePolicy)
        self.combo_port.setObjectName("combo_port")
        self.horizontalLayout.addWidget(self.combo_port)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_check = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_check.setObjectName("btn_check")
        self.horizontalLayout_2.addWidget(self.btn_check)
        self.btn_open = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout_2.addWidget(self.btn_open)
        self.btn_close = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_2.addWidget(self.btn_close)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.text_port = QtWidgets.QTextEdit(self.layoutWidget)
        self.text_port.setObjectName("text_port")
        self.verticalLayout_2.addWidget(self.text_port)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 270, 351, 221))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(79, 19, 201, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.animation_view = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.animation_view.setContentsMargins(0, 0, 0, 0)
        self.animation_view.setObjectName("animation_view")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 510, 351, 221))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(19, 29, 311, 181))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.camera_view = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.camera_view.setContentsMargins(0, 0, 0, 0)
        self.camera_view.setObjectName("camera_view")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(380, 30, 411, 831))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_4)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(19, 29, 381, 791))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.plot_view = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.plot_view.setContentsMargins(0, 0, 0, 0)
        self.plot_view.setObjectName("plot_view")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(820, 30, 331, 831))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_5)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 30, 291, 791))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.others_view = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.others_view.setContentsMargins(0, 0, 0, 0)
        self.others_view.setObjectName("others_view")
        self.textInformation = QtWidgets.QTextEdit(self.centralwidget)
        self.textInformation.setGeometry(QtCore.QRect(40, 760, 301, 91))
        self.textInformation.setObjectName("textInformation")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1171, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prosthesis GUI"))
        self.label_title.setText(_translate("MainWindow", "                   Pros GUI"))
        self.groupBox.setTitle(_translate("MainWindow", "串口属性"))
        self.label_port.setText(_translate("MainWindow", "Port"))
        self.btn_check.setText(_translate("MainWindow", "检测串口"))
        self.btn_open.setText(_translate("MainWindow", "打开串口"))
        self.btn_close.setText(_translate("MainWindow", "关闭串口"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Animation"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Camera"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Plot_view"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Others"))
