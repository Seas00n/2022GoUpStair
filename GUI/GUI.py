import sys
import json
import time

import numpy
import numpy as np
import pyqtgraph
from PyQt5.Qt import *
from design_gui import *
import pyqtgraph as pg
from design_gui import Ui_MainWindow
import serial
import serial.tools.list_ports

test_count = 0
L_thigh = 40
L_shank = 40
L_foot = 15


# 多重继承
class ProsTestSerial(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ProsTestSerial, self).__init__(parent=parent)
        # Ui_MainWindow初始化函数，加载在designer中创建的组件
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.set_graph_ui()
        self.set_animation_ui()
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
            self.com_dict["%s" % port[0]] = "%s" % port[1]
            self.combo_port.addItem(port[0])
        if len(self.com_dict) == 0:
            self.combo_port.addItem("无串口")

    def btn_open_clicked(self):
        self.port = self.combo_port.currentText()
        if len(self.com_dict) == 0:
            self.text_port.insertPlainText("串口异常无法打开")
        else:
            time.sleep(0.1)
            self.ser_open = True
            self.text_port.insertPlainText("串口开启")
            self.btn_check.setEnabled(False)
            self.btn_close.setEnabled(True)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5)

    def btn_close_clicked(self):
        self.ser_open = False
        self.timer.stop()
        self.btn_open.setEnabled(True)
        self.btn_close.setEnabled(False)

    def set_animation_ui(self):
        win = QGraphicsView()
        self.animation_view.addWidget(win)
        scene = QGraphicsScene()
        win.setScene(scene)
        self.linkage = Linkage()
        scene.addItem(self.linkage)

    def set_graph_ui(self):
        # 抗锯齿+背景色
        pg.setConfigOptions(antialias=True, background='w')
        # 创建pg绘图窗口widget
        win = pg.GraphicsLayoutWidget()
        self.plot_view.addWidget(win)
        self.curves = []
        self.Nsamples = 110
        curve_q_thigh = self.plot_view_config(
            win=win,
            label='Thigh Angle/deg',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90],
            pen_color='r'
        )
        self.curves.append(curve_q_thigh)
        win.nextRow()
        curve_q_knee = self.plot_view_config(
            win=win,
            label='Knee Angle/deg',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90],
            pen_color='g'
        )
        self.curves.append(curve_q_knee)
        win.nextRow()
        curve_q_ankle = self.plot_view_config(
            win=win,
            label='Ankle Angle/deg',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90],
            pen_color='b'
        )
        self.curves.append(curve_q_ankle)

        win.nextRow()
        curve_phase = self.plot_view_config(
            win=win,
            label='Phase',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90],
            pen_color='g'
        )
        self.curves.append(curve_phase)
        win.nextRow()
        curve_f = self.plot_view_config(
            win=win,
            label='Force/N',
            xrange=[0, self.Nsamples + 5],
            yrange=[-20, 110],
            xlim=[0, self.Nsamples],
            ylim=[-20, 120],
            pen_color='b'
        )
        self.curves.append(curve_f)
        win.nextRow()
        curve_state = self.plot_view_config(
            win=win,
            label='Current State',
            xrange=[0, self.Nsamples + 5],
            yrange=[0, 5],
            xlim=[0, self.Nsamples],
            ylim=[0, 4],
            pen_color='g'
        )
        self.curves.append(curve_state)
        self.NPlots = len(self.curves)
        self.buf_plot = numpy.zeros((self.NPlots, self.Nsamples))

    def plot_view_config(self, win, label, xrange, yrange, xlim, ylim, pen_color, grid_show=True):
        dym_plot_view = win.addPlot()
        xaxis = dym_plot_view.getAxis('bottom')
        xaxis.setLabel(text=label, color='#000000')
        dym_plot_view.showGrid(x=grid_show, y=grid_show)
        dym_plot_view.setRange(xRange=xrange, yRange=yrange, padding=0)
        dym_plot_view.setLimits(xMin=xlim[0], xMax=xlim[1], yMin=ylim[0], yMax=ylim[1])
        dym_plot_view.enableAutoRange('xy', False)
        curve = dym_plot_view.plot(pen=pen_color, width=1)
        return curve

    def update_data(self):
        # 获取最新数据
        global test_count
        test_count += 1
        if test_count > 180:
            test_count = 0
        data_new = np.ones(self.NPlots) * np.sin(test_count * np.pi / 180)
        data_new[0] *= 40
        data_new[1] *= -20
        data_new[2] *= 40
        self.fifo_plot_buffer(data_new)
        for idx in range(self.NPlots):
            self.curves[idx].setData(self.buf_plot[idx, :])
        self.linkage.set_angle(data_new[0], data_new[1], data_new[2])

    def fifo_plot_buffer(self, data_new):
        self.buf_plot[:, 0:-1] = self.buf_plot[:, 1:]
        self.buf_plot[:, -1] = data_new


class Linkage(QGraphicsItem):
    def __init__(self):
        super(Linkage, self).__init__()
        global L_thigh, L_shank, L_foot
        self.L_thigh = L_thigh
        self.L_shank = L_shank
        self.L_foot = L_foot
        self.x_hip = 0
        self.y_hip = 0
        self.x_knee = 0
        self.y_knee = self.L_thigh
        self.x_ankle = 0
        self.y_ankle = self.L_thigh + self.L_shank
        self.x_toe = 0
        self.y_toe = self.L_thigh + self.L_shank + self.L_foot
        self.max_d = self.L_thigh + self.L_shank + self.L_foot
        self.bounding_box = QRectF(QPointF(-self.max_d, -0.2*self.max_d), QPointF(self.max_d, self.max_d))

    def boundingRect(self):
        return self.bounding_box

    def set_angle(self, q_thigh, q_knee, q_ankle):
        self.prepareGeometryChange()
        self.x_knee = self.x_hip+self.L_thigh * numpy.sin(numpy.deg2rad(q_thigh))
        self.y_knee = self.y_hip+self.L_thigh * numpy.cos(numpy.deg2rad(q_thigh))
        self.x_ankle = self.x_knee + self.L_shank * numpy.sin(numpy.deg2rad(q_thigh + q_knee))
        self.y_ankle = self.y_knee + self.L_shank * numpy.cos(numpy.deg2rad(q_thigh + q_knee))
        self.x_toe = self.x_ankle + self.L_foot * numpy.sin(numpy.deg2rad(q_thigh + q_knee + q_ankle))
        self.y_toe = self.y_ankle + self.L_foot * numpy.cos(numpy.deg2rad(q_thigh + q_knee + q_ankle))

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QBrush(Qt.red), 3))
        painter.drawLine(QLineF(QPointF(self.x_hip, self.y_hip),
                                QPointF(self.x_knee, self.y_knee)))
        painter.setPen(QPen(QBrush(Qt.green), 3))
        painter.drawLine(QLineF(QPointF(self.x_knee, self.y_knee),
                                QPointF(self.x_ankle, self.y_ankle)))
        painter.setPen(QPen(QBrush(Qt.blue), 3))
        painter.drawLine(QLineF(QPointF(self.x_ankle, self.y_ankle),
                                QPointF(self.x_toe, self.y_toe)))
        painter.setPen(QPen(QBrush(Qt.black), 2))
        painter.drawEllipse(QPointF(self.x_hip, self.y_hip), 3, 3)
        painter.drawRect(self.bounding_box)
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
