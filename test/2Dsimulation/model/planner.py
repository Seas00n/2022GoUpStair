import numpy as np
import scipy.interpolate as scip

DEGREE_TO_RAD = np.pi / 180
RAD_TO_DEGREE = 180 / np.pi
g = 9.8
class sinCurve(object):
    def __init__(self, A=0.75, w=0.0006):
        self.A_ = A
        self.w_ = w

    def update_desired_pos_and_velocity(self, t):
        q = self.A_ * np.sin(self.w_ * t)
        qd = self.A_ * self.w_ * np.cos(self.w_ * t)
        return q, qd

class LIPM2D_Steady(object):
    def __init__(self,zh,Tsup,s):
        self.w = np.sqrt(g/zh)
        self.Tc = 1/self.w
        self.C = np.cosh(Tsup/self.Tc)
        self.S = np.sinh(Tsup/self.Tc)
        self.s_normal = s
        # 稳定步态下的运动原语
        xi = -s/2
        vi = abs(xi)*(self.C+1)/self.Tc/self.S
        xf = s/2
        vf = abs(xf)*(self.C+1)/self.Tc/self.S


