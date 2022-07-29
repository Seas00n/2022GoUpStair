import numpy as np
import time
import serial
from utils.usart import *
from utils.process_communication import *
'''
    串口收发和波形图显示
'''


def main():
    NumLoop = 20
    t_vec = np.arange(0, NumLoop * 2 * np.pi, 0.01 * np.pi)
    sin_signal1 = -50*np.sin(t_vec)
    sin_signal2 = 1.5 * np.sin(2 * np.pi / 5 * t_vec) + 2
    cos_signal1 = -50*np.cos(t_vec)
    cos_signal2 = 2 * np.cos(2 * np.pi / 3 * t_vec) - 1
    usart6 = USART(port='COM8', baud_rate=115200)
    if not usart6.is_open:
        return -1

    # 创建发送端MailBox
    process0_mailbox = FSMMailBox()
    process0_mailbox.build_publisher()

    for i in range(len(t_vec)):
        # 设置要向串口发送的数据
        set_send_item('q_knee_des', sin_signal1[i])
        set_send_item('q_ankle_des', sin_signal1[i])
        set_send_item('qd_knee_des', cos_signal1[i])
        set_send_item('qd_ankle_des', cos_signal1[i])
        set_send_item('torque_knee_des', sin_signal2[i])
        set_send_item('torque_ankle_des', sin_signal2[i])
        set_send_item('terrain_mode', 0)
        # 发送串口数据
        usart6.UART_Transmit_Data()

        # 串口接收数据
        usart6.UART_Receive_Data()
        # 将接收到的数据写入邮箱
        process0_mailbox.set_msg_item('q_thigh',sin_signal1[i]*0.5)
        process0_mailbox.set_msg_item('q_knee_real', get_read_item('q_knee_real'))
        process0_mailbox.set_msg_item('q_ankle_real', get_read_item('q_ankle_real'))
        process0_mailbox.set_msg_item('f', get_read_item('F_z'))
        process0_mailbox.set_msg_item('state', get_read_item('motion_phase'))
        process0_mailbox.set_msg_item('q_knee_des',get_sent_item('q_knee_des'))
        process0_mailbox.set_msg_item('q_ankle_des',get_sent_item('q_ankle_des'))
        # 发送邮箱中的数据
        process0_mailbox.write_msg()
        time.sleep(5e-3)

if __name__ == '__main__':
    main()
