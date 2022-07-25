import sys
import json
import time

import numpy
from PyQt5.Qt import *
from design_gui import *
import pyqtgraph as pg
from design_gui import Ui_MainWindow
import serial
import serial.tools.list_ports

# 多重继承
class ProsTestSerial(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ProsTestSerial, self).__init__(parent=parent)
        # Ui_MainWindow初始化函数，加载在designer中创建的组件
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.set_graph_ui()
        self.connect_signal()

    def connect_signal(self):
        self.btn_check.clicked.connect(self.btn_check_clicked)
        self.btn_open.clicked.connect(self.btn_open_clicked)
        self.btn_close.clicked.connect(self.btn_close_clicked)

    def btn_check_clicked(self):
        self.com_dict = {}
        port_list = list(serial.tools.list_ports.comports())

        self.combo_port.clear()
        for port in port_list:
            self.com_dict["%s"%port[0]] = "%s"%port[1]
            self.combo_port.addItem(port[0])
        if len(self.com_dict)==0:
            self.combo_port.addItem("无串口")

    def btn_open_clicked(self):
        self.port = self.combo_port.currentText()
        self.is_open = True

    def btn_close_clicked(self):
        self.is_open = False

    def set_graph_ui(self):
        # 抗锯齿+背景色
        pg.setConfigOptions(antialias=True, background='w')
        # 创建pg绘图窗口widget
        win = pg.GraphicsLayoutWidget()
        self.plot_view.addWidget(win)

        self.dym_plot_view_q_knee = self.plot_view_config(
            win=win,
            label='Knee Angle/deg',
            xrange=[0, 110],
            yrange=[-90, 90],
            xlim=[0, 100],
            ylim=[-90, 90]
        )
        win.nextRow()
        self.dym_plot_view_q_ankle = self.plot_view_config(
            win=win,
            label='Ankle Angle/deg',
            xrange=[0, 110],
            yrange=[-90, 90],
            xlim=[0, 100],
            ylim=[-90, 90]
        )

        win.nextRow()
        self.dym_plot_view_phase = self.plot_view_config(
            win=win,
            label='Phase',
            xrange=[0, 110],
            yrange=[-90, 90],
            xlim=[0, 100],
            ylim=[-90, 90]
        )

        win.nextRow()
        self.dym_plot_view_f = self.plot_view_config(
            win=win,
            label='Force/N',
            xrange=[0, 110],
            yrange=[-20, 110],
            xlim=[0, 100],
            ylim=[-20, 120]
        )

        win.nextRow()
        self.dym_plot_view_state = self.plot_view_config(
            win=win,
            label='Current State',
            xrange=[0, 110],
            yrange=[0, 5],
            xlim=[0, 100],
            ylim=[0, 4]
        )


    def plot_view_config(self, win, label, xrange, yrange, xlim, ylim, grid_show=True):
        dym_plot_view = win.addPlot()
        font = QtGui.QFont()
        font.setFamily("Times")
        font.setPointSize(4)
        xaxis=dym_plot_view.getAxis('bottom')
        xaxis.setLabel(text=label, color='#000000')
        xaxis.tickFont = font
        dym_plot_view.showGrid(x=grid_show, y=grid_show)
        dym_plot_view.setRange(xRange=xrange, yRange=yrange,padding=0)
        dym_plot_view.setLimits(xMin=xlim[0], xMax=xlim[1], yMin=ylim[0], yMax=ylim[1])
        return dym_plot_view




if __name__ == '__main__':
    # 创建应用对象
    app = QtWidgets.QApplication(sys.argv)
    # 自定义类继承自QWidgets,包含一系列创建桌面应用的UI元素
    w = ProsTestSerial()
    # 在桌面显示窗口
    w.show()
    # 事件处理器这个时候开始工作。主循环从窗口上接收事件，并把事件派发到应用控件里。
    # 当调用exit()方法或直接销毁主控件时，主循环就会结束。
    # sys.exit()方法能确保主循环安全退出。
    # 外部环境会收到主控件如何结束的信息。
    sys.exit(app.exec_())
