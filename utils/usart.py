import serial
import serial.tools.list_ports
import numpy as np
import time

'''
    串口类的实现参考：https://www.cnblogs.com/-wenli/p/11261109.html
    数据解包实现参考：https://blog.csdn.net/yldmkx/article/details/115482351
    日志输出实现参考：https://blog.csdn.net/qq_33567641/article/details/82769523
    
'''
send_data = {
    'q_knee_des': [],
    'qd_knee_des': [],
    'q_ankle_des': [],
    'qd_ankle_des': [],
    'torque_knee_des': [],
    'torque_ankle_des': [],
    'terrain_mode': []
}
read_data = {
    'q_knee_real': [],
    'qd_knee_real': [],
    'q_ankle_real': [],
    'qd_ankle_real': [],
    'F_x': [],
    'F_z': [],
    'M_y': [],
    'motion_phase': []
}


def set_send_vec(vec_send):
    global send_data
    count = 0
    for key, value in send_data.items():
        send_data[key] = vec_send[count]


def set_read_vec(vec_read):
    global read_data
    count = 0
    for key, value in read_data.items():
        read_data[key] = vec_read[count]


def set_send_item(key, value):
    global send_data
    send_data[key] = value


def get_read_item(key):
    global read_data
    return read_data[key]


def get_read_vec():
    global read_data
    return np.array(list(read_data.values()))


def get_sent_vec():
    global read_data
    return np.array(list(send_data.values()))


def analysis_read_data(bytes_read, k_float_2_int=100, b_float_2_int=30000):
    global read_data
    data = np.frombuffer(bytes_read, dtype=np.uint16)
    if len(data) == len(read_data):
        data = (data - b_float_2_int) / k_float_2_int
        set_read_vec(data)
    else:
        print("\033[33m [Warning]Data Length Incorrect = %d\033[0m" % len(data))


def package_send_data(k_float_2_int=100, b_float_2_int=30000):
    global send_data
    data = get_sent_vec()
    data = data * k_float_2_int + b_float_2_int
    data = data.astype(dtype='uint16')
    send_byte = bytearray(data.tolist())
    return send_byte


class USART():
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.is_open = False
        test_g = 1
        try:
            USART.print_Available_Com()
            self.ser = serial.Serial(
                port=port,
                baudrate=baud_rate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS, timeout=1e-2
            )
            if self.ser.is_open:
                self.is_open = True
                print("\033[32m [LOG]Serial is open\033[0m")
                print("-----[Information]-----")
                print("| PortName = ", self.port)
                print("| BaduRate = ", self.baud_rate)

        except Exception as e:
            print("\033[31m [ERROR]Serial not Open | {}\033[0m".format(e))

    @staticmethod
    def print_Available_Com():
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) == 0:
            print("\033[33m [Warning]No port can be used \033[0m")

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
        num_read_bytes = len(read_data) * 2
        bytes_read = self.ser.read(num_read_bytes)
        analysis_read_data(bytes_read)

    def UART_Transmit_Data(self):
        num_send_bytes = len(send_data) * 2
        bytes_send = package_send_data()
        self.ser.write(bytes_send)
