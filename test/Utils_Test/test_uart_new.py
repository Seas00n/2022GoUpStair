import time
from multiprocessing import Process, Manager
import numpy as np
import os,signal
import sys

from PyQt5 import Qt, QtWidgets
from PyQt5.Qt import *
from utils.usart import *
from utils.key_bord_event import *
from GUI.pros_app import ProsTestSerial


def main():
    print("\033[32m [LOG]Create Process 0:{}\033[0m".format(os.getppid()))
    NumLoop = 20
    t_vec = np.arange(0, NumLoop * 2 * np.pi, 0.01 * np.pi)
    sin_signal1 = -50 * np.sin(t_vec)
    sin_signal2 = 1.5 * np.sin(2 * np.pi / 5 * t_vec) + 2
    cos_signal1 = -50 * np.cos(t_vec)
    cos_signal2 = 2 * np.cos(2 * np.pi / 3 * t_vec) - 1

    msg_server = Manager()
    msg_dict = msg_server.dict()
    lock = msg_server.Lock()
    set_msg_server(msg_dict)
    uart_process = Process(target=uart_process_task, args=('COM5', msg_dict, lock))
    gui_process = Process(target=gui_process_task, args=(msg_dict, lock))
    uart_process.start()
    gui_process.start()
    for i in range(len(t_vec)):
        if not uart_process.is_alive():
            sys.exit(print('False'))
            gui_process.terminate()
        lock.acquire()
        msg_dict['q_thigh'] = sin_signal1[i] * 0.5
        msg_dict['q_ankle_des'] = sin_signal1[i]
        msg_dict['q_knee_des'] = sin_signal1[i]
        lock.release()
        time.sleep(5e-3)
    uart_process.join()
    gui_process.join()


def uart_process_task(port, msg_dict, lock):
    usart6 = USART(port=port, baud_rate=115200)
    if not usart6.is_open:
        return -1
    with keyboard.Listener(on_press=on_press,
                           on_release=partial(on_release, )) as listener:
        while True:
            usart6.UART_Transmit_Data()
            usart6.UART_Receive_Data()
            lock.acquire()
            for key, value in send_data.items():
                if key in msg_dict:
                    set_send_item(key, msg_dict[key])
            for key, value in read_data.items():
                if key in msg_dict:
                    msg_dict[key] = get_read_item(key)
            lock.release()
            time.sleep(5e-3)

def visual_process_task():
    time.sleep(40)


def gui_process_task(msg_dict, lock):
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    w = ProsTestSerial()

    def update_data_with_msg_dict(d, l):
        data_new = np.zeros(w.NPlots)
        count = 0
        l.acquire()
        for key, c in w.curves.items():
            if key in d:
                data_new[count] = d[key]
            else:
                data_new[count] = 0
            count += 1
        l.release()
        w.fifo_plot_buffer(data_new)
        count = 0
        for key, c in w.curves.items():
            w.curves[key].setData(w.buf_plot[count, :])
            count += 1
        w.linkage.set_angle(data_new[w.plot_index.get('q_thigh')],
                            data_new[w.plot_index.get('q_knee_real')],
                            data_new[w.plot_index.get('q_ankle_real')])

    w.timer.timeout.connect(lambda: update_data_with_msg_dict(msg_dict, lock))
    w.show()
    sys.exit(app.exec_())


def set_msg_server(msg_dict):
    msg_dict['q_thigh'] = 0
    msg_dict['phase'] = 0
    msg_dict['q_ankle_real'] = 0
    msg_dict['qd_ankle_real'] = 0
    msg_dict['q_knee_real'] = 0
    msg_dict['qd_knee_real'] = 0
    msg_dict['q_ankle_des'] = 0
    msg_dict['qd_ankle_des'] = 0
    msg_dict['q_knee_des'] = 0
    msg_dict['qd_knee_des'] = 0
    msg_dict['torque_ankle_des'] = 0
    msg_dict['torque_knee_des'] = 0
    msg_dict['motion_mode'] = 0
    msg_dict['terrain_mode'] = 0
    msg_dict['F_x'] = 0
    msg_dict['F_z'] = 0
    msg_dict['M_y'] = 0
    msg_dict['obstacle_w'] = 0
    msg_dict['obstacle_h'] = 0
    msg_dict['obstacle_d'] = 0


if __name__ == '__main__':
    main()
