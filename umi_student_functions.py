from __future__ import division, print_function
from umi_parameters import UMI_parameters
import math
from visual import *
# Specifications of UMI
# Enter the correct details in the corresponding file (umi_parameters.py).
# <<<<<<<<<<-------------------------------------------------------------------- TODO FOR STUDENTS
UMI = UMI_parameters()

def apply_inverse_kinematics(x, y, z):
    # Real arm runs from -0.541 to 0.541 instead of 0 to 1.082
    riser_position = y + (-0.541 + UMI.total_arm_height)
    # Use the position on of the gripper to choose left/right handedness
    if z < 0:
        left_handed = True
    else:
        left_handed = False
    arm_1 = UMI.upper_length
    arm_2 = UMI.lower_length
    #print(x, z, x*x, z*z)
    c2 = float(x*x + z*z - 2.0*arm_1*arm_2) / float(2.0*arm_1*arm_2)
    # Rounding errors, which make c2 either 1 or slightly higher than 1. if the arm is fully stretched
    if c2 >= 1 and c2 < 1.000000000001:
        c2 = 0.99999999999999
    # Choose angle based on whether the arms bends left or right
    if left_handed:
        s2 = - math.sqrt(1 - c2*c2)
    else:
        s2 = math.sqrt(1 - c2*c2)
    elbow_angle = degrees(math.atan2(s2, c2))
    shoulder_angle = degrees(math.atan2(z,x) - math.atan2(arm_2*s2,arm_1 + arm_2*c2))
    wrist_angle = - elbow_angle - shoulder_angle
    return riser_position, shoulder_angle, elbow_angle, wrist_angle, left_handed