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
from utils.process_communication import *

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
        # self.setFixedSize(self.width(), self.height())
        self.btn_state_init()
        self.set_graph_ui()
        self.set_animation_ui()
        self.connect_signal()
        self.process1_mailbox = FSMMailBox()
        self.process1_mailbox.build_subscriber()


    def connect_signal(self):
        self.btn_check.clicked.connect(self.btn_check_clicked)
        self.btn_open.clicked.connect(self.btn_open_clicked)
        self.btn_close.clicked.connect(self.btn_close_clicked)

    def update_data(self):
        # 获取最新数据
        # data_new = self.simulation_data()
        msg_new = self.process1_mailbox.read_msg()
        # 从msg_new中设置需要绘制的部分
        data_new = np.zeros(self.NPlots)
        count = 0
        for key, c in self.curves.items():
            if key in self.process1_mailbox.msg_dict:
                data_new[count] = self.process1_mailbox.get_msg_item(key)
            else:
                data_new[count] = 0
            count += 1
        self.fifo_plot_buffer(data_new)
        print(data_new)

        count = 0
        for key, c in self.curves.items():
            self.curves[key].setData(self.buf_plot[count, :])
            count += 1
        self.linkage.set_angle(self.process1_mailbox.get_msg_item('q_thigh'),
                               self.process1_mailbox.get_msg_item('q_knee'),
                               self.process1_mailbox.get_msg_item('q_ankle'))

    def btn_state_init(self):
        self.btn_check.setEnabled(True)
        self.btn_open.setEnabled(False)
        self.btn_close.setEnabled(False)

    def btn_check_clicked(self):
        self.com_dict = {}
        port_list = list(serial.tools.list_ports.comports())

        self.combo_port.clear()
        for port in port_list:
            self.com_dict["%s" % port[0]] = "%s" % port[1]
            self.combo_port.addItem(port[0])
        if len(self.com_dict) == 0:
            self.combo_port.addItem("无串口")
        else:
            self.btn_open.setEnabled(True)

    def btn_open_clicked(self):
        self.port = self.combo_port.currentText()
        if len(self.com_dict) == 0:
            self.text_port.insertPlainText("串口异常无法打开\r\n")
        else:
            time.sleep(0.1)
            self.ser_open = True
            self.text_port.insertPlainText("{}开启,输出{}条曲线\r\n".format(self.port,self.NPlots))
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
        self.text_port.insertPlainText("{}关闭\r\n".format(self.port))

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
        self.curves = {}
        self.Nsamples = 110

        fig_q_thigh = self.figure_config(
            win=win,
            label='Thigh Angle/deg',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90]
        )
        curve_q_thigh = self.plot_curve(
            figure=fig_q_thigh,
            pen_color='r',
            curve_label='q_thigh'
        )

        win.nextRow()
        fig_q_knee = self.figure_config(
            win=win,
            label='Knee Angle/deg',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90]
        )

        curve_q_knee_desire = self.plot_curve(
            figure=fig_q_knee,
            pen_color='r',
            curve_label='q_knee_des',
            pen_symbol=QtCore.Qt.PenStyle.DotLine
        )

        curve_q_knee_real = self.plot_curve(
            figure=fig_q_knee,
            pen_color='b',
            curve_label='q_knee_real'
        )

        win.nextRow()
        fig_q_ankle = self.figure_config(
            win=win,
            label='Ankle Angle/deg',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90]
        )
        curve_q_ankle_desire = self.plot_curve(
            figure=fig_q_ankle,
            pen_color='r',
            curve_label='q_ankle_des',
            pen_symbol=QtCore.Qt.PenStyle.DotLine
        )
        curve_q_ankle_real = self.plot_curve(
            figure = fig_q_ankle,
            pen_color='b',
            curve_label='q_ankle_real'
        )

        win.nextRow()
        fig_phase = self.figure_config(
            win=win,
            label='Phase',
            xrange=[0, self.Nsamples + 5],
            yrange=[-90, 90],
            xlim=[0, self.Nsamples],
            ylim=[-90, 90],
        )
        curve_phase = self.plot_curve(
            figure=fig_phase,
            pen_color='g',
            curve_label='phase'
        )
        win.nextRow()
        fig_f = self.figure_config(
            win=win,
            label='Force/N',
            xrange=[0, self.Nsamples + 5],
            yrange=[-20, 110],
            xlim=[0, self.Nsamples],
            ylim=[-20, 120]
        )
        curve_f = self.plot_curve(
            figure=fig_f,
            pen_color='b',
            curve_label='f'
        )
        win.nextRow()
        fig_state = self.figure_config(
            win=win,
            label='Current State',
            xrange=[0, self.Nsamples + 5],
            yrange=[0, 5],
            xlim=[0, self.Nsamples],
            ylim=[0, 4]
        )
        curve_state = self.plot_curve(
            figure=fig_state,
            curve_label='state',
            pen_color='b'
        )
        self.NPlots = len(self.curves)
        self.buf_plot = numpy.zeros((self.NPlots, self.Nsamples))

    def figure_config(self, win, label, xrange, yrange, xlim, ylim, grid_show=True):
        figure = win.addPlot()
        xaxis = figure.getAxis('bottom')
        xaxis.setLabel(text=label, color='#000000')
        figure.showGrid(x=grid_show, y=grid_show)
        figure.setRange(xRange=xrange, yRange=yrange, padding=0)
        figure.setLimits(xMin=xlim[0], xMax=xlim[1], yMin=ylim[0], yMax=ylim[1])
        figure.enableAutoRange('xy', False)
        return figure

    def plot_curve(self, figure, curve_label, pen_color='black', pen_width=2, pen_symbol=QtCore.Qt.PenStyle.SolidLine):
        pen = pg.mkPen(pen_color, width=pen_width, style=pen_symbol)
        curve = pg.PlotCurveItem(pen=pen)
        figure.addItem(curve)
        figure.plot()
        self.curves[curve_label] = curve
        return curve

    def fifo_plot_buffer(self, data_new):
        self.buf_plot[:, 0:-1] = self.buf_plot[:, 1:]
        self.buf_plot[:, -1] = data_new

    def simulation_data(self):
        global test_count
        test_count += 1
        if test_count > 180:
            test_count = 0
        data_new = np.ones(self.NPlots) * np.sin(test_count * np.pi / 180)
        data_new[0] *= 40
        data_new[1] *= -20
        data_new[2] *= 40
        return data_new


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
        self.bounding_box = QRectF(QPointF(-self.max_d, -0.2 * self.max_d), QPointF(self.max_d, self.max_d))

    def boundingRect(self):
        return self.bounding_box

    def set_angle(self, q_thigh, q_knee, q_ankle):
        self.prepareGeometryChange()
        self.x_knee = self.x_hip + self.L_thigh * numpy.sin(numpy.deg2rad(q_thigh))
        self.y_knee = self.y_hip + self.L_thigh * numpy.cos(numpy.deg2rad(q_thigh))
        self.x_ankle = self.x_knee + self.L_shank * numpy.sin(numpy.deg2rad(q_thigh + q_knee))
        self.y_ankle = self.y_knee + self.L_shank * numpy.cos(numpy.deg2rad(q_thigh + q_knee))
        self.x_toe = self.x_ankle + self.L_foot * numpy.sin(numpy.deg2rad(q_thigh + q_knee + q_ankle+90.0))
        self.y_toe = self.y_ankle + self.L_foot * numpy.cos(numpy.deg2rad(q_thigh + q_knee + q_ankle+90.0))

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
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
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
