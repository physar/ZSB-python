#!python2

from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *
import wx
from copy import deepcopy
# Custom made imports
from umi_parameters import UMI_parameters
from umi_chessboard import UMI_chessboard
from umi_student_functions import *
import numpy as np
scene.title = "UMI RTX"
scene.height = scene.width = 600

#**********************************************
# ROBOT PARAMETERS

# Specifications of UMI ARE IMPORTED THROUGH umi_student_functions.

#**********************************************
# Functions that are called on various events

def setRiserHeight(evt): # called on slider events (output in mm)
    value = s0.GetValue() / 1000.0
    moveRiser(value)

def moveRiser(value):
    s0_label.SetLabel('Set Riser Height: %d mm' % (value * 1000.0))
    riser.pos.y = UMI.correct_height(value)
    UMI_angles[0] = value

def setShoulderAngle(evt): # called on slider events (output in degrees)
    value = s1.GetValue() / 1000.0
    moveShoulder(value)

def moveShoulder(value):
    s1_label.SetLabel('Set Shoulder rotation: %.2f degrees' % degrees(value))
    shoulder_joint.axis = (cos(value),0,sin(value))
    UMI_angles[1] = value

def setElbowAngle(evt): # called on slider events (output in degrees)
    value = s2.GetValue() / 1000.0
    moveElbow(value)

def moveElbow(value):
    s2_label.SetLabel('Set Elbow rotation: %.2f degrees' % degrees(value))
    elbow_joint.axis = (cos(value),0,sin(value))
    UMI_angles[2] = value

def setWristAngle(evt): # called on slider events] (output in degrees)
    value = s3.GetValue() / 1000.0
    moveWrist(value)

def moveWrist(value):
    s3_label.SetLabel('Set Wrist rotation: %.2f degrees' % degrees(value))
    wrist_joint.axis = (cos(value),0,sin(value))
    UMI_angles[3] = value

def setGripperWidth(evt): # called on slider events] (output in degrees)
    value = s4.GetValue() / 1000.0
    moveGripper(value)

def moveGripper(value):
    s4_label.SetLabel('Set Gripper opening: %d mm' % (value * 1000))
    gripper_pos.pos = (0, gripper_pos.pos.y, 0.5*gripper_pos.width+value/2)
    gripper_neg.pos = (0, gripper_pos.pos.y, -0.5*gripper_pos.width-value/2)
    UMI_angles[4] = value

L = 600
# Create a window. Note that w.win is the wxPython "Frame" (the window).
# window.dwidth and window.dheight are the extra width and height of the window
# compared to the display region inside the window. If there is a menu bar,
# there is an additional height taken up, of amount window.menuheight.
# The default style is wx.DEFAULT_FRAME_STYLE; the style specified here
# does not enable resizing, minimizing, or full-sreening of the window.
w = window(width=2*(L+window.dwidth), height=L+window.dheight,
           menus=False, title='UMI RTX',
           style= wx.CAPTION | wx.CLOSE_BOX)

# Place a 3D display widget in the left half of the window.
d = 20
disp = display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=-vector(1,0.25,1), center=vector(0,0.5,0))

# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d,4), size=(L-2*d,d), label='3D representation.',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

#max_height = 0.5*(UMI.hpedestal)*1000.0
#min_height = (-0.5*(UMI.hpedestal)+UMI.total_arm_height)*1000.0

s0 = wx.Slider(p, pos=(1.0*L,0.1*L), size=(0.9*L,20), minValue=UMI.joint_ranges["Riser"][0]*1000.0, maxValue=UMI.joint_ranges["Riser"][1]*1000.0)
s0.Bind(wx.EVT_SCROLL, setRiserHeight)
s0_label = wx.StaticText(p, pos=(1.0*L,0.05*L), label='Set Riser height: %d mm' % (UMI.joint_ranges["Riser"][1]*1000.0))

s1 = wx.Slider(p, pos=(1.0*L,0.2*L), size=(0.9*L,20), minValue=radians(UMI.joint_ranges["Shoulder"][0])*1000.0, maxValue=radians(UMI.joint_ranges["Shoulder"][1])*1000.0)
s1.Bind(wx.EVT_SCROLL, setShoulderAngle)
s1_label = wx.StaticText(p, pos=(1.0*L,0.15*L), label='Set Shoulder rotation: 0 degrees')

s2 = wx.Slider(p, pos=(1.0*L,0.3*L), size=(0.9*L,20), minValue=radians(UMI.joint_ranges["Elbow"][0])*1000.0, maxValue=radians(UMI.joint_ranges["Elbow"][1])*1000.0)
s2.Bind(wx.EVT_SCROLL, setElbowAngle)
s2_label = wx.StaticText(p, pos=(1.0*L,0.25*L), label='Set Elbow rotation: 0 degrees')

s3 = wx.Slider(p, pos=(1.0*L,0.4*L), size=(0.9*L,20), minValue=radians(UMI.joint_ranges["Wrist"][0])*1000.0, maxValue=radians(UMI.joint_ranges["Wrist"][1])*1000.0, style=wx.SL_HORIZONTAL)
s3.Bind(wx.EVT_SCROLL, setWristAngle)
s3_label = wx.StaticText(p, pos=(1.0*L,0.35*L), label='Set Wrist rotation: 0 degrees')

s4 = wx.Slider(p, pos=(1.0*L,0.5*L), size=(0.9*L,20), minValue=UMI.joint_ranges["Gripper"][0]*1000.0, maxValue=UMI.joint_ranges["Gripper"][1]*1000.0, style=wx.SL_HORIZONTAL)
s4.Bind(wx.EVT_SCROLL, setGripperWidth)
s4_label = wx.StaticText(p, pos=(1.0*L,0.45*L), label='Set Gripper opening: 50 mm')

#***********************************************
# ROBOT JOINTS
frameworld = frame()

frame0 = frame(frame=frameworld)
frame0.pos = (-UMI.wpedestal/2.0, 0.5*UMI.hpedestal,0)

# The shoulder joint location is now on world position (x,z) = (0,0)
riser = frame(frame=frame0)
riser.pos = (UMI.wpedestal/2.0,frame0.pos.y, 0)

shoulder_joint = frame(frame=riser)
shoulder_joint.pos = (0,-UMI.pedestal_offset, 0)
#shoulder_joint.rotate(axis = (0, 1, 0), angle = pi/4)

elbow_joint = frame(frame=shoulder_joint)
elbow_joint.pos = (UMI.upper_length,-UMI.upper_height, 0)
#elbow_joint.rotate(axis = (0, 1, 0), angle = pi/4)

wrist_joint = frame(frame=elbow_joint)
wrist_joint.pos = (UMI.lower_length,-UMI.lower_height, 0)
#wrist_joint.rotate(axis = (0, 1, 0), angle = pi/4)
#************************************************
# ROBOT ARM
pedestal = box(frame = frame0,
               pos = (0,0,0),
               height = UMI.hpedestal,
               length = UMI.wpedestal,
               width = UMI.wpedestal,
               color = (0.4, 0.4, 0.4))
riser_part = cylinder(frame = riser,
               pos = (0, -UMI.pedestal_offset, 0),
               axis = (0, UMI.pedestal_offset, 0),
               radius = UMI.wpedestal/2.0,
               color = color.red)

upper_arm = box(frame = shoulder_joint,
               pos = (UMI.upper_length/2.0,-UMI.upper_height/2,0),
               height = UMI.upper_height,
               length = UMI.upper_length*1.25,
               width = 0.08,
               color = color.green)
lower_arm = box(frame = elbow_joint,
               pos = (UMI.lower_length/2.0,-UMI.lower_height/2,0),
               height = UMI.lower_height,
               length = UMI.lower_length*1.25,
               width = 0.08,
               color = color.green)

wrist = box(frame = wrist_joint,
               pos = (0,-UMI.wrist_height/8,0),
               height = UMI.wrist_height/4,
               length = 0.08,
               width = 0.08,
               color = color.green)

gripper_pos = box(frame = wrist_joint,
               pos = (0,-UMI.wrist_height/2,0.025),
               height = UMI.wrist_height,
               length = 0.03,
               width = 0.005,
               color = color.blue)

gripper_neg = box(frame = wrist_joint,
               pos = (0,-UMI.wrist_height/2,-0.025),
               height = UMI.wrist_height,
               length = 0.03,
               width = 0.005,
               color = color.blue)
gripper_open = 1

floor = box(frame=frameworld,
               pos = (0,0,0),
               height = 0.001,
               length = UMI.wpedestal + 0.6,
               width = 0.6*2,
               color = (0.5, 0.5, 0.5))
floor.pos = (floor.length/2 - UMI.wpedestal, 0, 0)
#**************************************************************************
# CHESSBOARD
# frame, board_size=0.3, position_x_z = (0.15, -0.15), angle_degrees=0)
# <<<<<<<<<<-------------------------------------------------------------------- CHANGE BOARD POSITION/ANGLE HERE
CHESSBOARD = UMI_chessboard(frameworld, 0.3, (0.15, -0.15), 0)

#***************************************************************************
# INIT CONTROLS
s0.SetValue(s0.GetMax())
s1.SetValue(0) # update the slider
s2.SetValue(0) # update the slider
s3.SetValue(0) # update the slider
s4.SetValue(50) # update the slider

# Storage only used to make the movements of the arm appear smoothed.
UMI_angles = [UMI.joint_ranges["Riser"][1], 0, 0, 0, 0.05]
#**************************************************************************
# CONTROLLER Functions
def get_gripper_bottom_position():
    return frame0.frame_to_world(
        riser.frame_to_world(
            shoulder_joint.frame_to_world(
                elbow_joint.frame_to_world(
                    wrist_joint.pos + vector(0,-UMI.wrist_height, 0)
                )
            )
        )
    )

def execute_sequence(sequence_list):
    # First move up so you do not knock over anything.
    safe_angles = deepcopy(UMI_angles)
    safe_angles[0] = CHESSBOARD.get_board_height() + 0.2 + UMI.total_arm_height
    # Set to a safe location and get in default position
    loop_angles = deepcopy(UMI_angles)
    # Then continue with the original plans.
    total_list = [safe_angles] + sequence_list
    for new_angles in total_list:
        # Degrees to Radians.
        new_angles = [new_angles[0]] + [radians(x) for x in new_angles[1:-1]] + [new_angles[-1]]
        # Correct the height
        move_arm_from_to(loop_angles, new_angles)
        loop_angles = deepcopy(UMI_angles)
        sleep(0.5)

def move_arm_from_to(from_angles, to_angles):
    # Compute the differences for all joints
    old_a = np.array(from_angles)
    new_a = np.array(to_angles)
    delta_a = ( new_a - old_a )
    # Move through these differences in 100 steps
    for i in np.arange(0.0, 1.01, 0.01):
        rate(100)
        moveRiser(old_a[0] + delta_a[0]*i)
        moveShoulder(old_a[1] + delta_a[1]*i)
        moveElbow(old_a[2] + delta_a[2]*i)
        moveWrist(old_a[3] + delta_a[3]*i)
        moveGripper(old_a[4] + delta_a[4]*i)
        disp.center=get_gripper_bottom_position()


#**************************************************************************
# CREATE CONTROLS
board_position_to_cartesian(CHESSBOARD, 'a1')
board_position_to_cartesian(CHESSBOARD, 'c5')
board_position_to_cartesian(CHESSBOARD, 'h8')
XX = True
sequence_list = high_path(CHESSBOARD, 'b2', 'd5')
while(True):
    rate(100)
    disp.center=get_gripper_bottom_position()
    if XX:
        execute_sequence(sequence_list)
        XX = False
    #break
#End Program
0
