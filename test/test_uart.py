import numpy as np
import time
import serial
from utils.usart import *

'''
    测试串口通信和波形图显示
'''


def main():
    NumLoop = 20
    t_vec = np.arange(0, 20 * 2 * np.pi, 0.01 * np.pi)
    sin_signal1 = np.sin(t_vec)
    sin_signal2 = 1.5 * np.sin(2 * np.pi / 5 * t_vec) + 2
    cos_signal1 = np.cos(t_vec)
    cos_signal2 = 2 * np.cos(2 * np.pi / 3 * t_vec) - 1
    usart6 = USART(port='COM8', baud_rate=115200)
    if not usart6.is_open:
        return -1
    for i in range(len(t_vec)):
        set_send_item('q_knee', sin_signal1[i])
        set_send_item('q_ankle', sin_signal1[i])
        set_send_item('qd_knee', cos_signal1[i])
        set_send_item('qd_ankle', cos_signal1[i])
        set_send_item('torque_knee', sin_signal2[i])
        set_send_item('torque_ankle', sin_signal2[i])
        set_send_item('terrain_mode', 0)
        usart6.UART_Transmit_Data()


if __name__ == '__main__':
    main()
