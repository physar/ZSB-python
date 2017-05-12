# Based on Bruce Sherwood's Double Pendulum
# Modified to look somewhat more like a robot arm
# By Andrew Lee
# Math 198 Fall 2009

from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *
import wx

scene.title = "UMI RTX"
scene.height = scene.width = 600

#**********************************************
# ROBOT PARAMETERS

# Specifications of UMI
# Zed
hpedestal = 1.082
pedestal_offset = 0.0675
wpedestal = 0.1 # Undefined

# Dimensions upper arm
upper_length = 0.2535
upper_height = 0.095

# Dimensions lower arm
lower_length = 0.2535
lower_height = 0.08

# Dimensions wrist
wrist_height = 0.09

#**********************************************
# Functions that are called on various events

def rotateShoulderPos(evt): # called on "Rotate left" button event
    shoulder_joint.rotate(axis = (0, 1, 0), angle = pi/180)

def rotateShoulderNeg(evt): # called on "Rotate right" button event
    shoulder_joint.rotate(axis = (0, 1, 0), angle = -pi/180)

def leave(evt): # called on "Exit under program control" button event
    exit()

def setRiserHeight(evt): # called on slider events (output in mm)
    value = s0.GetValue() / 1000.0
    print(s0.GetMin())
    s0_label.SetLabel('Set Riser Height: %d mm' % (value * 1000 + s0.GetMax()))
    riser.pos = (wpedestal/2.0, value, 0)

def setShoulderAngle(evt): # called on slider events (output in degrees)
    value = s1.GetValue() / 1000.0
    s1_label.SetLabel('Set Shoulder rotation: %.2f degrees' % degrees(value))
    shoulder_joint.axis = (cos(value),0,sin(value))

def setElbowAngle(evt): # called on slider events (output in degrees)
    value = s2.GetValue() / 1000.0
    s2_label.SetLabel('Set Elbow rotation: %.2f degrees' % degrees(value))
    elbow_joint.axis = (cos(value),0,sin(value))

def setWristAngle(evt): # called on slider events] (output in degrees)
    value = s3.GetValue() / 1000.0
    s3_label.SetLabel('Set Wrist rotation: %.2f degrees' % degrees(value))
    wrist_joint.axis = (cos(value),0,sin(value))

def setGripperWidth(evt): # called on slider events] (output in degrees)
    value = s4.GetValue() / 1000.0
    s4_label.SetLabel('Set Gripper opening: %d mm' % (value * 1000))
    gripper_pos.pos = (0, gripper_pos.pos.y, 0.5*gripper_pos.width+value/2)
    gripper_neg.pos = (0, gripper_pos.pos.y, -0.5*gripper_pos.width-value/2)

L = 600
# Create a window. Note that w.win is the wxPython "Frame" (the window).
# window.dwidth and window.dheight are the extra width and height of the window
# compared to the display region inside the window. If there is a menu bar,
# there is an additional height taken up, of amount window.menuheight.
# The default style is wx.DEFAULT_FRAME_STYLE; the style specified here
# does not enable resizing, minimizing, or full-sreening of the window.
w = window(width=2*(L+window.dwidth), height=L+window.dheight+window.menuheight,
           menus=True, title='UMI RTX',
           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

# Place a 3D display widget in the left half of the window.
d = 20
disp = display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=-vector(1,0.25,1), center=vector(0,0.5,0))

# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d,4), size=(L-2*d,d), label='3D representation.',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

max_height = 0.5*(hpedestal)*1000.0
min_height = (-0.5*(hpedestal)+pedestal_offset+upper_height+lower_height+wrist_height)*1000.0

s0 = wx.Slider(p, pos=(1.0*L,0.1*L), size=(0.9*L,20), minValue=min_height, maxValue=max_height)
s0.Bind(wx.EVT_SCROLL, setRiserHeight)
s0_label = wx.StaticText(p, pos=(1.0*L,0.05*L), label='Set Riser height: %d mm' % (max_height*2))

s1 = wx.Slider(p, pos=(1.0*L,0.2*L), size=(0.9*L,20), minValue=radians(-90)*1000.0, maxValue=radians(90)*1000.0)
s1.Bind(wx.EVT_SCROLL, setShoulderAngle)
s1_label = wx.StaticText(p, pos=(1.0*L,0.15*L), label='Set Shoulder rotation: 0 degrees')

s2 = wx.Slider(p, pos=(1.0*L,0.3*L), size=(0.9*L,20), minValue=radians(-180)*1000.0, maxValue=radians(110)*1000.0)
s2.Bind(wx.EVT_SCROLL, setElbowAngle)
s2_label = wx.StaticText(p, pos=(1.0*L,0.25*L), label='Set Elbow rotation: 0 degrees')

s3 = wx.Slider(p, pos=(1.0*L,0.4*L), size=(0.9*L,20), minValue=radians(-110)*1000.0, maxValue=radians(110)*1000.0, style=wx.SL_HORIZONTAL)
s3.Bind(wx.EVT_SCROLL, setWristAngle)
s3_label = wx.StaticText(p, pos=(1.0*L,0.35*L), label='Set Wrist rotation: 0 degrees')

s4 = wx.Slider(p, pos=(1.0*L,0.5*L), size=(0.9*L,20), minValue=0, maxValue=50, style=wx.SL_HORIZONTAL)
s4.Bind(wx.EVT_SCROLL, setGripperWidth)
s4_label = wx.StaticText(p, pos=(1.0*L,0.45*L), label='Set Gripper opening: 50 mm')

# Create a menu of options (Rotate right, Rotate right, Make red, Make cyan).
# Currently, menus do not work on the Macintosh.
m = w.menubar # Refers to the menubar, which can have several menus

menu = wx.Menu()
item = menu.Append(-1, 'Toggle Grip', 'Shoulder negative rotate')
w.win.Bind(wx.EVT_MENU, rotateShoulderNeg, item)

# Add this menu to an Options menu next to the default File menu in the menubar
m.Append(menu, 'Options')

#***********************************************
# ROBOT JOINTS
frameworld = frame()
frame0 = frame(frame=frameworld)
frame0.pos = (-wpedestal/2.0, 0.5*hpedestal,0)

# The shoulder joint location is now on world position (x,z) = (0,0)
riser = frame(frame=frame0)
riser.pos = (wpedestal/2.0,frame0.pos.y, 0)

shoulder_joint = frame(frame=riser)
shoulder_joint.pos = (0,-pedestal_offset, 0)
#shoulder_joint.rotate(axis = (0, 1, 0), angle = pi/4)

elbow_joint = frame(frame=shoulder_joint)
elbow_joint.pos = (upper_length,-upper_height, 0)
#elbow_joint.rotate(axis = (0, 1, 0), angle = pi/4)

wrist_joint = frame(frame=elbow_joint)
wrist_joint.pos = (lower_length,-lower_height, 0)
#wrist_joint.rotate(axis = (0, 1, 0), angle = pi/4)
#************************************************
# ROBOT ARM
pedestal = box(frame = frame0,
               pos = (0,0,0),
               height = hpedestal,
               length = wpedestal,
               width = wpedestal,
               color = (0.4, 0.4, 0.4))
riser_part = cylinder(frame = riser,
               pos = (0, -pedestal_offset, 0),
               axis = (0, pedestal_offset, 0),
               radius = wpedestal/2.0,
               color = color.red)

upper_arm = box(frame = shoulder_joint,
               pos = (upper_length/2.0,-upper_height/2,0),
               height = upper_height,
               length = upper_length*1.25,
               width = 0.08,
               color = color.green)
lower_arm = box(frame = elbow_joint,
               pos = (lower_length/2.0,-lower_height/2,0),
               height = lower_height,
               length = lower_length*1.25,
               width = 0.08,
               color = color.green)

wrist = box(frame = wrist_joint,
               pos = (0,-wrist_height/8,0),
               height = wrist_height/4,
               length = 0.08,
               width = 0.08,
               color = color.green)

gripper_pos = box(frame = wrist_joint,
               pos = (0,-wrist_height/2,0.025),
               height = wrist_height,
               length = 0.03,
               width = 0.005,
               color = color.blue)

gripper_neg = box(frame = wrist_joint,
               pos = (0,-wrist_height/2,-0.025),
               height = wrist_height,
               length = 0.03,
               width = 0.005,
               color = color.blue)
gripper_open = 1

floor = box(frame=frameworld,
               pos = (0,0,0),
               height = 0.001,
               length = wpedestal + 0.6,
               width = 0.6*2,
               color = (0.5, 0.5, 0.5))
floor.pos = (floor.length/2 - wpedestal, 0, 0)
#**************************************************************************
# CHESSBOARD

# Dimensions of the board
chessboard_size = 0.3
field_size = (chessboard_size / 8.0)
chessboard_dist = chessboard_size/2 - field_size

# Edges of the locations
wallthck = field_size / 15.0
wallhght = field_size / 15.0

# Position of the center of the board
mplhght = 0.02
mplcent = chessboard_size

# Colors of the board
board_color_light = (1.0, 1.0, 1.0)
board_color_dark = (1.0, 0.5, 1.0)
beam_color = (0.9, 0.9, 0.9)

framemp = frame(frame=frameworld)
framemp.pos =(mplcent, mplhght,0)
# Rotate the board
framemp.rotate(axis = (0, 1, 0), angle = 0)

mchessboard = box(frame = framemp,
               height = mplhght,
               length = chessboard_size,
               width = chessboard_size,
               pos = (chessboard_dist, -0.5*mplhght, 0),
               color = board_color_light)

# Draw the beams to create 64 squares
width_beams = []
vert_beams = []
for field in range(8):
    beam_offset = field * (chessboard_size / 8.0)
    width_beams.append(box(frame = framemp,
               height = wallhght,
               length = wallthck,
               width = mchessboard.width,
               pos = (chessboard_dist-mchessboard.length/2+beam_offset+(0.5*wallthck), 0.5*wallhght, 0),
               color = beam_color)
    )
    vert_beams.append(box(frame = framemp,
               height = wallhght,
               length = mchessboard.length,
               width = wallthck,
               pos = (chessboard_dist, 0.5*wallhght, beam_offset+(0.5*wallthck)-mchessboard.width/2),
               color = beam_color)
    )
width_beams.append(box(frame = framemp,
               height = wallhght,
               length = wallthck,
               width = mchessboard.width,
               pos = (chessboard_dist-mchessboard.length/2+chessboard_size-(0.5*wallthck), 0.5*wallhght, 0),
               color = beam_color)
)
vert_beams.append(box(frame = framemp,
               height = wallhght,
               length = mchessboard.length,
               width = wallthck,
               pos = (chessboard_dist, 0.5*wallhght, chessboard_size-(0.5*wallthck)-mchessboard.width/2),
               color = beam_color)
)
fields = []
for x in range(8):
    for y in range(8):
        if (x + y) % 2 == 0:
            fields.append( box(frame = framemp,
                   height = 0.001,
                   length = field_size,
                   width = field_size,
                   pos = (field_size*x - field_size/2.0, 0, (chessboard_dist - field_size*y) + field_size/2),
                   color = board_color_dark)
            )
#***************************************************************************
# INIT CONTROLS
s0.SetValue(frame0.pos.y*1000.0)
s1.SetValue(0) # update the slider
s2.SetValue(0) # update the slider
s3.SetValue(0) # update the slider
s4.SetValue(50) # update the slider
#**************************************************************************
# CREATE CONTROLS
while(True):
    rate(100)
    disp.center=frame0.frame_to_world(
        riser.frame_to_world(
            shoulder_joint.frame_to_world(
                elbow_joint.frame_to_world(
                    wrist_joint.pos - vector(0,wrist.height/2.0, 0)
                )
            )
        )
    )
#End Program

0
