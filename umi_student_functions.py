#!python2

from __future__ import division, print_function
from umi_parameters import UMI_parameters
from umi_common import *
import math
import numpy as np
from visual import *
# Specifications of UMI
# Enter the correct details in the corresponding file (umi_parameters.py).
# <<<<<<<<<<-------------------------------------------------------------------- TODO FOR STUDENTS
UMI = UMI_parameters()

def apply_inverse_kinematics(x, y, z, gripper):
    ''' Computes the angles, given some real world coordinates
        :param float x: cartesian x-coordinate
        :param float y: cartesian y-coordinate
        :param float z: cartesian z-coordinate

        :return: Returns the a tuple containing the position and angles of the robot-arm joints.
    '''
    # Implementation is based on the Robotics readers made by Leo.

    # Real arm runs from -0.541 to 0.541 instead of 0 to 1.082
    #riser_position = y + (-0.541 + UMI.total_arm_height)
    riser_position = y + UMI.total_arm_height
    # Use the position on of the gripper to choose left/right handedness
    if z < 0:
        left_handed = True
    else:
        left_handed = False
    arm_1 = UMI.upper_length
    arm_2 = UMI.lower_length

    c2 = float(x*x + z*z - 2.0*arm_1*arm_2) / float(2.0*arm_1*arm_2)

    # Rounding errors, which make c2 either 1 or slightly higher than 1. if the arm is fully stretched
    if c2 >= 1 and c2 < 1.000000000001:
        c2 = 0.99999999999999
    # Choose angle based on whether the arms bends left or right
    if left_handed:
        s2 = - math.sqrt(1 - c2*c2)
    else:
        s2 = math.sqrt(1 - c2*c2)

    # Compute the resulting angles for each joint.
    elbow_angle = degrees(math.atan2(s2, c2))
    shoulder_angle = degrees(math.atan2(z,x) - math.atan2(arm_2*s2,arm_1 + arm_2*c2))
    wrist_angle = - elbow_angle - shoulder_angle
    # TODO: Do we want to return if he is left/right handed?????
    return (riser_position, shoulder_angle, elbow_angle, wrist_angle, gripper)

def board_position_to_cartesian(chessboard, position):
    ''' Convert a position between [a1-h8] to its cartesian coordinates in frameworld coordinates.

        You are not allowed to use the functions such as: frame_to_world.
        You have to show actual calculations using positions/vectors and angles.

        :param obj chessboard: The instantiation of the chessboard that you wish to use.
        :param str position: A position in the range [a1-h8]

        :return: tuple Return a position in the format (x,y,z)
    '''
    # Get the local coordinates for the tiles on the board in the 0-7 range.
    (row, column) = to_coordinate(position)

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

def high_path(chessboard, from_pos, to_pos):
    sequence_list = []
    # We assume that 20 centimeter above the board is safe.
    safe_height = 0.2
    low_height = 0.1

    half_piece_height = 0.06 /2
    if from_pos in chessboard.pieces:
        half_piece_height = chessboard.pieces_height[chessboard.pieces[from_pos][1]]  / 2
        print("Piece found at from_pos.")
    (from_x, from_y, from_z) = board_position_to_cartesian(chessboard, from_pos)
    (to_x, to_y, to_z) = board_position_to_cartesian(chessboard, to_pos)
    # Check for the piece height:

    # Hover above the first field on SAFE height:
    sequence_list.append(apply_inverse_kinematics(from_x, from_y + safe_height, from_z, chessboard.field_size))
    # Hover above the first field on LOW height:
    sequence_list.append(apply_inverse_kinematics(from_x, from_y + low_height, from_z, chessboard.field_size))
    # Hover above the first field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(from_x, from_y + low_height, from_z, chessboard.field_size))
    # Hover above the first field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(from_x, from_y + half_piece_height, from_z, chessboard.field_size))
    # Grip the piece
    sequence_list.append(apply_inverse_kinematics(from_x, from_y + half_piece_height, from_z, UMI.joint_ranges["Gripper"][0]))
    # Hover above the first field on SAFE height:
    sequence_list.append(apply_inverse_kinematics(from_x, from_y + safe_height, from_z, UMI.joint_ranges["Gripper"][0]))

    # Move to new position on SAFE height
    sequence_list.append(apply_inverse_kinematics(to_x, to_y + safe_height, to_z, UMI.joint_ranges["Gripper"][0]))
    # Hover above the first field on LOW height:
    sequence_list.append(apply_inverse_kinematics(to_x, to_y + low_height, to_z, UMI.joint_ranges["Gripper"][0]))
    # Hover above the first field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(to_x, to_y + half_piece_height, to_z, UMI.joint_ranges["Gripper"][0]))
    # Hover above the first field on half of the piece height:
    sequence_list.append(apply_inverse_kinematics(to_x, to_y + half_piece_height, to_z, chessboard.field_size))
    # Move to new position on SAFE height
    sequence_list.append(apply_inverse_kinematics(to_x, to_y + safe_height, to_z, chessboard.field_size))
    return sequence_list

def move_to_garbage(chessboard, from_pos):
    pass

def move(chessboard, from_pos, to_pos):
    pass
