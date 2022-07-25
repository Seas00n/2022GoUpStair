import json

import numpy as np

import pyqtgraph as pg

import time
import sys

from PyQt5.Qt import *
from dym_plot_graph import Ui_MainWindow
from PyQt5.QtChart import QChart, QValueAxis, QChartView, QSplineSeries


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super(QMainWindow, self).__init__()
        self.app = app
        self.setup_ui()  # 渲染画布
        self.update_data_thread = UpdateDataThread()  # 创建更新波形数据线程
        self.connect_signals()  # 绑定触发事件

    def setup_ui(self):
        self.setupUi(self)
        self.x_range = np.arange(128)
        # 加载波形
        self.set_graph_ui()  # 设置绘图窗口
        self.plot_show(Sin().get_data())

    def set_graph_ui(self):
        # pg.setConfigOption('background', 'w')
        pg.setConfigOptions(antialias=True, background='w')  # pyqtgraph全局变量设置函数，antialias=True开启曲线抗锯齿
        win1 = pg.GraphicsLayoutWidget()  # 创建pg layout，可实现数据界面布局自动管理
        win2 = pg.GraphicsLayoutWidget()
        # pg绘图窗口可以作为一个widget添加到GUI中的graph_layout，当然也可以添加到Qt其他所有的容器中
        self.plot_view.addWidget(win1)
        self.dym_plot_view = win1.addPlot()  # 添加第一个绘图窗口
        self.dym_plot_view.setLabel('top', text='强度', color='#000000')  # y轴设置函数
        self.dym_plot_view.showGrid(x=True, y=True)  # 栅格设置函数
        self.dym_plot_view.setLogMode(x=False, y=False)  # False代表线性坐标轴，True代表对数坐标轴
        self.dym_plot_view.setLabel('bottom', text='时间', units='s')  # x轴设置函数
        # p1.addLegend()  # 可选择是否添加legend
        self.dym_plot_view.setYRange(0, 20)
        self.dym_plot_view.setXRange(0,120)
        self.dym_plot_view.setLimits(xMin=0, xMax=100, yMin=-20, yMax=20)
        # ax = self.dym_plot_view.getAxis('bottom')  # 设置x轴间隔
        # dx = [(value, str(value)) for value in range(128)]
        # ax.setTicks([dx, []])
        self.plot_view.addWidget(win2)
        self.dym_plot_view2 = win2.addPlot()
        self.dym_plot_view2.setLimits(xMin=0, xMax=1024, yMin=-20, yMax=20)

    def plot_show(self, data):
        # 显示波形
        y_data = np.array(data)
        self.dym_plot_view.plot(self.x_range, y_data, pen='b', name='动态波形', clear=True)  # pen画笔颜色为蓝色
        self.dym_plot_view2.plot(self.x_range, -y_data, pen='r', name='动态波形2', clear=True)
    def connect_signals(self):
        # 绑定触发事件
        self.btn_start.clicked.connect(self.btn_start_clicked)
        self.update_data_thread._signal_update.connect(self.update_data_thread_slot)  # 绑定回调事件

    def btn_start_clicked(self):
        # 开启按钮
        self.update_data_thread.start()

    def update_data_thread_slot(self, data):
        # 线程回调函数
        data = json.loads(data)
        self.plot_show(data['sin_data'])


# 使用线程不断更新波形数据
class UpdateDataThread(QThread):
    _signal_update = pyqtSignal(str)  # 信号

    def __init__(self, parent=None):
        super(UpdateDataThread, self).__init__(parent)
        self.qmut = QMutex()
        self.is_exit = False
        self.x_range = 128
        self.sin = Sin()

    def run(self):
        while True:
            self.qmut.lock()
            if self.is_exit:
                break
            self.qmut.unlock()

            self._signal_update.emit(json.dumps({'sin_data': self.sin.get_data()}))  # 发送信号给槽函数
            time.sleep(0.1)

        self.qmut.unlock()


class Sin():
    # 创建一个正弦波数据
    def __init__(self, pha=0):
        self.pha = pha  # 初始相位
        self.x_data = np.arange(128)
        self.ts = time.time()

    def get_data(self):
        dt = time.time() - self.ts
        z_data = 10 * np.sin(self.x_data + dt * 100)  # 准备动态数据
        return z_data.tolist()


def main():
    app = QApplication(sys.argv)
    mywindow = Window(app)
    mywindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()