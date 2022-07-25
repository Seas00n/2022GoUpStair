# legKinematics
腿部运动学

Class PendulemState:

    def _init_(self):
		self.v_CoM = zeros([0,3])
		self.p_CoM = zeros([0,3])
		self.orbital_energy = 0
		self.desired_orbital_energy = 0
		self.p_capture = zeros([0,3])

	def CoM_state_estimation: #输入LegState.thigh_angle和LegState.v_thigh，输出v_CoM和p_CoM

	def cal_orbital_energy: #计算轨道能量

	def cal_capture_point: #计算capture point位置，TO BE DEFINE: 平地转楼梯等特殊情况应用什么公式计算？需查阅文献

Class LegState:
	
    def _init_(self):
		self.thigh_angle = 0
		self.v_thigh = zeros([0,3])
		self.heel_strike_acc_threshold = 20 判断脚落地的imu加速度阈值
		self.v_knee = zeros([0,3]) #在以heel strike点为原点的世界坐标系下膝盖（也就是相机）的速度
		self.p_knee = zeros([0,3])
		self.state_foot = zeros([0,12]) #脚踝、跟、尖的位置、速度
		self.knee_ankle_joint_p_v = zeros([0,4]) #膝踝关节角度和角速度，从stm32读
		self.intention = 0 #匀速行走、停下、上楼、下楼、上下斜坡等 用0~n表示
		self.next_foot_placement = zeros([0,3])

	def predict_foot_placement: #输入Pendulum.p_capture，Environment.type_pred_from_hmm，Environment.height、width、theta，输出下一步可落足点的坐标和intention
	
	def cal_knee_state: #通过IMU积分+视觉里程计（待定）滤波得到v_knee和p_knee	

	def cal_foot_state: #输入v_knee,p_knee,knee_ankle_joint_p_v，输出state_foot

	def get_knee_ankle_joint_p_v: #从stm32读膝踝关节角度和角速度

	def inverse_kinematics: 输入SwingPlanner.optimized_via_points、LegState.state_foot，LegState.v_knee, LegStete.p_knee, 输出Swing.planner.desired_knee_ankle_joint_p_v