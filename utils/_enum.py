from enum import Enum
import numpy as np
class MotionMode(Enum):
    static_standing = np.array([0,0]).astype('uint8')
    static_sitting = [0, 1]
    static_squating = [0, 1]
    dynamic_stancing= [1, 0]
    dynamic_push_off= [1, 1]
    dynamic_swing = [1, 2]
    dynamic_flexion = [1, 3]

class TerrainMode(Enum):
    level_ground = 0
    stair_ascent = 1
    stair_descent = 2
    ramp_ascent = 3
    ramp_descent = 4