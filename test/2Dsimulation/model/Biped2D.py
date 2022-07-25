import pybullet as p
import pybullet_data
import numpy as np


class Biped_7link(object):
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.resetDebugVisualizerCamera(cameraDistance=6, cameraYaw=0,
                                     cameraPitch=0, cameraTargetPosition=[0, 2, 2.5])
        p.setGravity(0, 0, -9.8)
        self.ground = p.loadURDF('plane.urdf')
        self.robot = p.loadMJCF('/model/sustech_biped2d.xml', flags=p.MJCF_COLORS_FROM_FILE)[0]
        self.base_dof = 3  # degree of freedom for the base
        self.simu_f = 500  # simulation frequency Hz
        self.motion_f = 2  # controlled motion frequency Hz
        self.joints = self.get_joints()
        self.n_j = len(self.joints)
        self.zh = 0.9 # COM Height
        self.q_vec = np.zeros(self.n_j)
        self.dq_vec = np.zeros(self.n_j)
        self.q_mat = np.zeros((self.simu_f * 3, self.n_j))
        self.q_d_mat = np.zeros((self.simu_f * 3, self.n_j-self.base_dof))
        self.t = 0
        self.init_pos_and_vel_of_robot()
        print('Model Initialization')

    def get_joints(self):
        all_joints = []
        for j in range(p.getNumJoints(self.robot)):
            info = p.getJointInfo(self.robot, j)
            print(info)
            joint_type = info[2]
            if joint_type == p.JOINT_PRISMATIC or joint_type == p.JOINT_REVOLUTE:
                all_joints.append(j)
                p.setJointMotorControl2(self.robot, j, controlMode=p.VELOCITY_CONTROL, force=0)
        joints = all_joints
        return joints

    def init_pos_and_vel_of_robot(self):
        q_d_vec = np.zeros(self.n_j)
        d_q_d_vec = np.zeros(self.n_j)
        q_d_vec[1] = self.zh
        for j in range(self.n_j):
            p.resetJointState(self.robot, self.joints[j], targetValue=q_d_vec[j], targetVelocity=d_q_d_vec[j])
        p.stepSimulation()

