import pybullet
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from model import Biped2D
from model import planner

def run(robot, pl):
    t_n = int(1e5)
    for i in range(t_n):
        robot.t += 1/robot.simu_f
        qd_vec, dq_d_vec = pl.update()


if __name__ == '__main__':
    robot = Biped2D.Biped_7link()
    pl = planner.sinCurve()