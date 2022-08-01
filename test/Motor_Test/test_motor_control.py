import numpy as np
import serial
from utils.usart import *
from enum import Enum
import scipy.interpolate as scpip
'''
选择测试模式
'''

class Contorl_Method(Enum):
    Position_Control = 1
    Current_Control = 2
    FSM_Control = 3
    CPhase_Control = 4
def main():
    control_method = Contorl_Method.Position_Control
    # if control_method==Contorl_Method.Position_Control:

    # elif control_method==Contorl_Method.Current_Control:

    # elif control_method==Contorl_Method.FSM_Control:

    # elif control_method==Contorl_Method.CPhase_Control:



'''
基于定时器的事件触发器
'''
class Gait_Simulation_Data_Generator():
    def __init__(self,NumGaits,TGait,dt):
        self.NumGaits = NumGaits
        self.TGait = TGait
        self.dt = dt
        self.count = 0
        self.init_Timer()
        self.signal_dict={
            't':0,
            'phase': 1
        }

    def init_Timer(self):
        t_vec = np.arange(0,self.TGait,self.dt)
        s_vec = np.linspace(0,100,np.size(t_vec))
        self.t = t_vec
        self.s = s_vec
        if self.NumGaits>1:
            for i in range(self.NumGaits-1):
                self.t = np.append(self.t,t_vec+self.t[-1]-self.dt)
                self.s = np.append(self.s,s_vec)

    def Gait_Seed_Spanner(self,gait_seed_path):
        self.gait_seed = np.load(gait_seed_path,allow_pickle=True).item()
        self.simulation_data = np.zeros(len(self.signal_dict),np.size(self.t))
        t_vec = np.arange(0,self.TGait,self.dt)
        for key, value in range(len(self.signal_dict)):
            if key in self.gait_seed:
                x = np.arange(1,np.size(self.gait_seed[key]))
                x = x-1
                y = self.gait_seed[key]
                f = scpip.interp1d(x,y,'cubic')
                x_new = np.linspace(0,np.size(self.gait_seed[key]),np.size(t_vec))
                y_new = f(x_new)
                self.simulation_data[value,:] = np.tile(y_new,self.NumGaits)


class Position_Control_Data_Generater(Gait_Simulation_Data_Generator):
    def __init__(self,NumGaits,TGait,dt):
        super(Position_Control_Data_Generater, self).__init__()
        self.signal_dict['q_ankle_des'] = 2
        self.signal_dict['q_knee_des'] = 3
        self.signal_dict['qd_ankle_des'] = 4
        self.signal_dict['qd_knee_des'] = 5
        self.Gait_Seed_Spanner("data/test/pos_contorl_gait_seed.npy")

class Current_Control_Data_Generater(Gait_Simulation_Data_Generator):
    def __init__(self):
        pass

class FSM_Control_Data_Generator(Gait_Simulation_Data_Generator):
    def __init__(self):
        pass

# if __name__=='__main__':