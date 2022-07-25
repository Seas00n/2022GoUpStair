# planningAlgo
路径规划算法

Class SwingPlanner:
	
    def _init_(self):
		self.human_inspired_via_points
		self.optimized_via_points
		self.desired_knee_ankle_joint_p_v = zeros([0,4])
	
	def cal_human_inspired_via_points: #输入LegState.next_foot_placement、LegState.intention、输出human inspired swing foot trajectory上的若干个via points

	def optimized_via_points: 输入human_inspired_via_points、LegState.state_foot、Environment.leg2obstacle_distance等，对via points实时优化

Class StancePlanner:
	
    def _init_(self):
		self.k_model_parameter
		self.b_model_parameter
		self.q0_model_parameter
		self.virtual_leg_length = 0
		self.desired_torque = zeros([0,2])

	def cal_virtual_leg_length: 输入PendulemState.p_CoM、Environment.height、width、theta，计算虚拟腿长

	def cal_desired_torque：输入虚拟腿长、k b q0曲线模型的参数、计算k b q0，计算关节输出扭矩

