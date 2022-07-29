import numpy as np


class Msg():
    def __init__(self):
        self.msg_dict = {}
        self.data_buf = []

    # 在子进程调用设置，后统一发送
    def set_msg_item(self, key, value):
        if key in self.msg_dict:
            self.msg_dict[key] = value
        else:
            print("\033[31m [ERROR]Not in msg dict\033[0m")

    def get_msg_item(self, key):
        return self.msg_dict[key]

    # 在主进程调用
    def write_msg(self):
        count =0
        for key, value in self.msg_dict.items():
            self.data_buf[count] = value
            count += 1
        self.data_buf.flush()

    def read_msg(self):
        count = 0
        for key, value in self.msg_dict.items():
            self.msg_dict[key] = self.data_buf[count]
            count += 1
        return np.array(list(self.msg_dict.values()))


class FSMMailBox(Msg):
    def __init__(self):
        super(FSMMailBox, self).__init__()
        # 根据需求编写，顺序尽量和画图程序保持一致
        self.msg_dict['q_thigh'] = 0
        self.msg_dict['q_knee_real'] = 0
        self.msg_dict['q_ankle_real'] = 0
        self.msg_dict['f'] = 0
        self.msg_dict['phase'] = 0
        self.msg_dict['state'] = 0
        self.msg_dict['terrain_mode'] = 0
        self.msg_dict['q_knee_des']=0
        self.msg_dict['q_ankle_des']=0

    def build_subscriber(self):
        self.data_buf = np.memmap('..\log\main_thread_data.npy', dtype='float32', mode='r', shape=(len(self.msg_dict),))

    def build_publisher(self):
        self.data_buf = np.memmap('..\log\main_thread_data.npy', dtype='float32', mode='r+',
                                  shape=(len(self.msg_dict),))


class ContinuousPhaseMailBox(Msg):
    def __init__(self):
        super(Msg, self).__init__()
        # 根据需求编写
        self.msg_dict['q_thigh'] = 0
        self.msg_dict['q_knee'] = 0
        self.msg_dict['q_ankle'] = 0
        self.msg_dict['f'] = 0
        self.msg_dict['phase'] = 0
        self.msg_dict['state'] = 0
        self.msg_dict['terrain_mode'] = 0

    def build_subscriber(self):
        self.data_buf = np.memmap('log\main_thread_data.npy', dtype='float32', mode='r', shape=(len(self.msg_dict),))

    def build_publisher(self):
        self.data_buf = np.memmap('log\main_thread_data.npy', dtype='float32', mode='r+', shape=(len(self.msg_dict),))


class HybridControlMailBox(Msg):
    def __init__(self):
        super(Msg, self).__init__()
        # 根据需求编写
        self.msg_dict['q_thigh'] = 0
        self.msg_dict['q_knee'] = 0
        self.msg_dict['q_ankle'] = 0
        self.msg_dict['f'] = 0
        self.msg_dict['phase'] = 0
        self.msg_dict['state'] = 0
        self.msg_dict['obs_height'] = 0
        self.msg_dict['obs_width'] = 0
        self.msg_dict['Kp'] = 0
        self.msg_dict['Ki'] = 0
        self.msg_dict['Kd'] = 0

    def build_subscriber(self):
        self.data_buf = np.memmap('log\main_thread_data.npy', dtype='float32', mode='r', shape=(len(self.msg_dict),))

    def build_publisher(self):
        self.data_buf = np.memmap('log\main_thread_data.npy', dtype='float32', mode='r+', shape=(len(self.msg_dict),))
