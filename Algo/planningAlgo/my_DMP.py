import numpy as np
from matplotlib import pyplot as plt

class DMP(object):
    def __init__(self,training_data,data_period,K=156.25,B=25):
        self.K = K
        self.B = B
        self.timesteps = training_data.shape[0]
        self.dt = data_period/self.timesteps
        self.weights = None
        self.T_orig = data_period
        self.training_data = training_data
    def find_basis_functions_weights(self, training_data, data_period,
                                     num_weights=10):
        dt = data_period/len(training_data)
        init_state = training_data[0]
        goal_state = training_data[-1]
        # 高斯函数的均值
        C = np.linspace(0,1,num_weights)
        # 高斯函数的方差
        H = (0.65 * (1. / (num_weights - 1)) ** 2)



def example_DMP():
    t = np.arange(0, 3 * np.pi / 2, 0.01)
    t1 = np.arange(0, np.pi/2, 0.01)[:-1]
    t2 = np.arange(np.pi/2, np.pi , 0.01)[:-1]
    t3 = np.arange(np.pi, 3 * np.pi / 2, 0.01)
    data_x = t + 0.02 * np.random.rand(t.shape[0])
    data_y = np.concatenate([np.sin(t1) + 0.1 * np.random.rand(t1.shape[0]),
                             np.sin(t2) + 0.1 * np.random.rand(t2.shape[0]),
                             np.sin(t3) + 0.1 * np.random.rand(t3.shape[0])])
    training_data = np.vstack([data_x, data_y]).T
    period = 3 * np.pi / 2

if __name__ =='__main__':
    example_DMP()