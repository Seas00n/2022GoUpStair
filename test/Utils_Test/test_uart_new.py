import argparse
import queue
import time
from multiprocessing import Process, Manager, Pipe

from PyQt5 import Qt, QtWidgets
from PyQt5.Qt import *

from GUI.pros_app import ProsTestSerial
from utils.imu import *
from utils.key_bord_event import *
from utils.usart import *
from roypy import *
from roypy_sample_utils import CameraOpener
from sample_3d_cp import MyListener, pcd_to_binary_image
import glob
import cv2

camera_imu_id = ['038819D6']


def pros_ctrl_process_task():
    print("\033[32m [LOG]Create Process \033[0m \033[31m MAIN \033[0m :{}".format(os.getppid()))
    NumLoop = 20
    t_vec = np.arange(0, NumLoop * 2 * np.pi, 0.01 * np.pi)

    print("\033[32m [LOG]Loading Manager \033[0m")
    msg_server = Manager()
    print("\033[32m [LOG]Manager Created \033[0m")
    msg_dict = msg_server.dict()
    lock = msg_server.Lock()
    set_msg_server(msg_dict)

    pipe = Pipe(True)

    uart_process = Process(target=uart_process_task, args=('COM4', msg_dict, lock))
    gui_process = Process(target=gui_process_task, args=(msg_dict, lock, pipe))
    camera_imu_process = Process(target=camera_imu_process_task, args=(msg_dict, lock))
    camera_vision_process = Process(target=camera_vision_process_task, args=(msg_dict, lock, pipe))
    test_camera_vision_process = Process(target=test_camera_vision_process_task, args=(msg_dict, lock, pipe))

    # camera_imu_process.start()
    # print("\033[32m [LOG]Create Process \033[0m \033[31m CAMERA_IMU \033[0m :{}".format(camera_imu_process.pid))
    # wait_for_camera_imu(msg_dict)

    uart_process.start()
    print("\033[32m [LOG]Create Process \033[0m \033[31m UART \033[0m :{}".format(uart_process.pid))
    wait_for_uart(msg_dict)

    # camera_vision_process.start()
    # print("\033[32m [LOG]Create Process \033[0m \033[31m CAMERA \033[0m :{}".format(camera_vision_process.pid))

    test_camera_vision_process.start()
    print("\033[32m [LOG]Create Process \033[0m \033[31m Test_Pipe \033[0m :{}".format(test_camera_vision_process.pid))

    gui_process.start()
    print("\033[32m [LOG]Create Process \033[0m \033[31m GUI \033[0m :{}".format(gui_process.pid))

    for i in range(len(t_vec)):
        if not uart_process.is_alive():
            sys.exit(print("Program Over"))
        lock.acquire()
        msg_dict['t'] = t_vec[i]
        sin_signal = 20 * np.sin(t_vec[i])
        msg_dict['q_thigh'] = sin_signal * 0.5
        msg_dict['q_ankle_des'] = sin_signal
        msg_dict['q_knee_des'] = sin_signal
        lock.release()
        time.sleep(5e-3)
    uart_process.join()
    gui_process.join()


def uart_process_task(port, msg_dict, lock):
    usart6 = USART()
    if not usart6.is_open:
        return -1
    else:
        msg_dict['is_uart_ready'] = True
    with keyboard.Listener(on_press=on_press,
                           on_release=partial(on_release, )):
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


def camera_imu_process_task(msg_dict, lock):
    ref_device_id_vec = np.array(camera_imu_id)
    port_vec, _ = get_port_vec(ref_device_id_vec)
    device_vec, callback_vec, control_vec = open_device(port_vec)
    msg_dict['is_camera_imu_ready'] = True
    with keyboard.Listener(on_press=on_press,
                           on_release=partial(on_release, )):
        while True:
            captured_data_vec = capture_one_frame(callback_vec)
            if captured_data_vec is not None:
                lock.acquire()
                msg_dict['imu_angle'] = captured_data_vec[0]
                lock.release()


def gui_process_task(msg_dict, lock, pipe):
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    w = ProsTestSerial()
    close, input_pipe = pipe
    close.close()

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
        data_new[0] = d['imu_angle']
        l.release()
        w.fifo_plot_buffer(data_new)
        count = 0
        for key, c in w.curves.items():
            w.curves[key].setData(w.buf_plot[count, :])
            count += 1
        w.linkage.set_angle(data_new[w.plot_index.get('q_thigh')],
                            data_new[w.plot_index.get('q_knee_real')],
                            data_new[w.plot_index.get('q_ankle_real')])
        pcd_2d = input_pipe.recv()
        x_data = np.array([1, 3, 2, 1]) * 0.1
        y_data = np.array([-1, 2, 3, 1]) * 0.1
        w.scatter.setData(10 * x_data - 2, 10 * y_data - 2)

    w.timer.timeout.connect(lambda: update_data_with_msg_dict(msg_dict, lock))
    w.show()
    sys.exit(app.exec_())


def camera_vision_process_task(msg_dict, lock, pipe):
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("--code", default=None, help="access code")
    parser.add_argument("--rrf", default=None, help="play a recording instead of opening the camera")
    parser.add_argument("--cal", default=None, help="load an alternate calibration file (requires level 2 access)")
    parser.add_argument("--raw", default=False, action="store_true",
                        help="enables raw data output (requires level 2 access)")
    parser.add_argument("--seconds", type=int, default=300, help="duration to capture data")
    opener = CameraOpener(parser.parse_args())
    cam = opener.open_camera()
    q = queue.Queue()
    l = MyListener(q)
    cam.registerDataListener(l)
    use_cases = cam.getUseCases()
    cam.setUseCase(use_cases[3])
    output_pipe, _ = pipe
    # 相机开始采集
    cam.startCapture()
    with keyboard.Listener(on_press=on_press,
                           on_release=partial(on_release, )):
        while True:
            try:
                if len(q.queue) == 0:
                    item = q.get(True, 1)
                else:
                    for i in range(0, len(q.queue)):
                        item = q.get(True, 1)

                item = item[np.all(item != 0, axis=1)]
                lock.acquire()
                angle = msg_dict['imu_angle']
                lock.release()
                _, pcd_2d = pcd_to_binary_image(item, angle)
                pcd_2d_send = pcd_2d[::100, :]
                output_pipe.send(pcd_2d_send)
                time.sleep(0.1)
            except queue.Empty:
                break
    output_pipe.close()
    cam.stopCapture()


def test_camera_vision_process_task(msg_dict, lock, pipe):
    output_pipe, _ = pipe
    with keyboard.Listener(on_press=on_press,
                           on_release=partial(on_release, )):
        while True:
            pcd_2d_send = np.random.random([700, 2])
            output_pipe.send(pcd_2d_send)
            time.sleep(0.1)


def set_msg_server(msg_dict):
    msg_dict['t'] = 0
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
    msg_dict['imu_angle'] = 0
    msg_dict['is_uart_ready'] = False
    msg_dict['is_camera_imu_ready'] = False
    print('\033[32m [LOG]Manager Dict List \033[0m')
    for key, value in msg_dict.items():
        print('\033[4m  {}  \033[0m'.format(key))


def wait_for_camera_imu(msg_dict):
    while not msg_dict['is_camera_ready']:
        continue


def wait_for_uart(msg_dict):
    while not msg_dict['is_uart_ready']:
        continue


if __name__ == '__main__':
    pros_ctrl_process_task()
