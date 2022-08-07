import time

import serial
import serial.tools.list_ports
import numpy as np

'''
    串口类的实现参考：https://www.cnblogs.com/-wenli/p/11261109.html
    数据解包实现参考：https://blog.csdn.net/yldmkx/article/details/115482351
    日志输出实现参考：https://blog.csdn.net/qq_33567641/article/details/82769523
    
'''

send_data = {
    'q_ankle_des': 0,
    'qd_ankle_des': 0,
    'torque_ankle_des': 0,
    'q_knee_des': 0,
    'qd_knee_des': 0,
    'torque_knee_des': 0,
    'terrain_mode': 0
}
read_data = {
    'q_ankle_real': 0,
    'qd_ankle_real': 0,
    'q_knee_real': 0,
    'qd_knee_real': 0,
    'F_x': 0,
    'F_z': 0,
    'M_y': 0,
    'motion_mode': 0
}


def set_send_vec(vec_send):
    global send_data
    count = 0
    for key, value in send_data.items():
        send_data[key] = vec_send[count]
        count += 1


def set_read_vec(vec_read):
    global read_data
    count = 0
    for key, value in read_data.items():
        read_data[key] = vec_read[count]
        count += 1


def set_send_item(key, value):
    global send_data
    if key in send_data:
        send_data[key] = value
    else:
        print("\033[31m [ERROR]Not in serial dict\033[0m")


def get_read_item(key):
    global read_data
    return read_data[key]


def get_sent_item(key):
    global send_data
    return send_data[key]


def get_read_vec():
    global read_data
    return np.array(list(read_data.values()))


def get_sent_vec():
    global read_data
    return np.array(list(send_data.values()))


def analysis_read_data(bytes_read, k_float_2_int=100.0, b_float_2_int=30000.0):
    global read_data
    correct_read = 0
    data = np.frombuffer(bytes_read, dtype=np.uint16)  # ndarray uint16
    # print('bytes_read', bytes_read)
    if len(data) == len(read_data):
        data = (data - b_float_2_int) / k_float_2_int
        set_read_vec(data)
        correct_read = 1
        # print('data_read', data)
        # print('-------------------------------')
    else:
        print("\033[33m [Warning]Data Length Incorrect = %d\033[0m" % len(data))
        correct_read = 0
    return correct_read


def package_send_data(k_float_2_int=100.0, b_float_2_int=30000.0):
    global send_data
    data = get_sent_vec()
    # print('------------------------------------')
    # print('data_send', data)
    data = data * k_float_2_int + b_float_2_int
    send_byte = bytearray(data.astype(np.uint16))
    # print('bytes_send', send_byte)
    return send_byte


class USART():
    def __init__(self, baud_rate=115200):
        self.ser = None
        self.port = None
        self.baud_rate = baud_rate
        self.is_open = False
        self.scan_com()

    def scan_com(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) == 0:
            print("\033[33m [Warning]No port can be used \033[0m")
            return 0
        for port in port_list:
            try:
                self.ser = serial.Serial(
                    port=port,
                    baudrate=self.baud_rate,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS, timeout=1e-2
                )
                if self.ser.is_open:
                    correct_count = 0
                    for i in range(5):
                        self.UART_Transmit_Data()
                        time.sleep(5e-3)
                        c = self.UART_Receive_Data()
                        correct_count += 5
                    if correct_count == 5:
                        self.port = port
                        self.is_open = True
                        print("\033[32m [LOG]Serial is open\033[0m")
                        print("-----[Information]-----")
                        print("| PortName = ", self.port)
                        print("| BaudRate = ", self.baud_rate)
                    else:
                        self.ser.close()
                        continue
            except Exception as e:
                print("\033[31m [ERROR]Serial not Open | {}\033[0m".format(e))


    def open_UART(self):
        self.ser.open()
        if self.ser.is_open:
            self.is_open = True
            print("\033[32m [LOG]Serial is open\033[0m")
            print("-----[Information]-----")
            print("| PortName = ", self.port)
            print("| BaduRate = ", self.baud_rate)

    def close_UART(self):
        self.ser.close()
        if not self.is_open:
            self.is_open = False
            print("\033[32m [LOG]Serial is close\033[0m")

    def UART_Receive_Data(self):
        global read_data
        num_read_bytes = len(read_data) * 2
        bytes_read = self.ser.read(num_read_bytes)
        c = analysis_read_data(bytes_read)
        return c

    def UART_Transmit_Data(self):
        global send_data
        num_send_bytes = len(send_data) * 2
        bytes_send = package_send_data()
        self.ser.write(bytes_send)
