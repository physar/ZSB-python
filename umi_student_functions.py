from __future__ import division, print_function
from umi_parameters import UMI_parameters
import math
import numpy as np
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

def board_position_to_cartesian(chessboard, position, real_world):
    ''' Convert a position between [a1-h8] to its cartesian coordinates in frameworld coordinates.
    
        You are not allowed to use the functions such as: frame_to_world.
        You have to show actual calculations using positions/vectors and angles.
        
        :param obj chessboard: The instantiation of the chessboard that you wish to use.
        :param str position: A position in the range [a1-h8]
        
        :return: tuple Return a position in the format (x,y,z)
    '''
    # Get the local coordinates for the tiles on the board in the 0-7 range.
    row = ord(position[0]) - ord('a')
    column = int(position[1]) - 1
    
    # Retrieve the translation and the rotation of the board
    board_position = chessboard.get_position()
    board_angle = chessboard.get_angle_radians()

    # Initialize the first tile of the board, closes to the robot (h8)
    cartesian_row = chessboard.field_size * (7.0 - row) + chessboard.field_size/2.0
    cartesian_col = chessboard.field_size * (7.0 - column) + chessboard.field_size/2.0
    
    # Compute the length of the vector
    length_vector = math.sqrt(cartesian_row * cartesian_row + cartesian_col * cartesian_col);
    # Compute the angle between the rotation center and the vector.
    position_angle = atan2(cartesian_row,cartesian_col) 
    # Add the rotation of the board to this angle
    total_angle = -board_angle+position_angle
    
    # compute the new row/column values
    rotated_cartesian_row = length_vector * sin(total_angle)
    rotated_cartesian_col = length_vector * cos(total_angle)    
    
    # Output the results.
    result = (rotated_cartesian_row+board_position[0], board_position[1], rotated_cartesian_col+board_position[2])
    return result
    
    #TODO: Remove markers.
    box(frame = real_world,
               pos = board_position,
               height = 0.3,
               length = 0.005,
               width = 0.005,
               color = color.red)
    
    box(frame = real_world,
               pos = result,
               height = 0.3,
               length = 0.005,
               width = 0.005,
               color = color.blue)
    
    
    