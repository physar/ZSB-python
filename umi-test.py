# Based on Bruce Sherwood's Double Pendulum
# Modified to look somewhat more like a robot arm
# By Andrew Lee
# Math 198 Fall 2009

#Choose a location to move to by pressing keys 0-9
#Press enter (return) to execute

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
lower_height = 0.080

# Dimensions wrist
wrist_height = 0.189

# UMI SCALER
umi_scale = 4.0

#**********************************************
# Functions that are called on various events

def rotateShoulderPos(evt): # called on "Rotate left" button event
    shoulder_joint.rotate(axis = (0, 1, 0), angle = pi/180)

def rotateShoulderNeg(evt): # called on "Rotate right" button event
    shoulder_joint.rotate(axis = (0, 1, 0), angle = -pi/180)

def leave(evt): # called on "Exit under program control" button event
    exit()

def setred(evt): # called by "Make red" menu item
    pass

def setcyan(evt): # called by "Make cyan" menu item
    pass

def cuberate(value):
    pass

def setRiserHeight(evt): # called on slider events
    value = s0.GetValue() / 1000.0
    s0_label = wx.StaticText(p, pos=(1.0*L,0.15*L), label='Set Riser Height: '+ str(value))
    riser.pos = ((wpedestal*umi_scale)/2.0, value, 0)

def setShoulderAngle(evt): # called on slider events
    value = s1.GetValue() / 1000.0
    s1_label = wx.StaticText(p, pos=(1.0*L,0.35*L), label='Set Shoulder rotation: '+ str(value))
    shoulder_joint.axis = (cos(value),0,sin(value))

def setElbowAngle(evt): # called on slider events
    value = s2.GetValue() / 1000.0
    s2_label = wx.StaticText(p, pos=(1.0*L,0.60*L), label='Set Elbow rotation: '+ str(value))
    elbow_joint.axis = (cos(value),0,sin(value))

def setWristAngle(evt): # called on slider events]
    value = s3.GetValue() / 1000.0
    s3_label = wx.StaticText(p, pos=(1.0*L,0.85*L), label='Set Wrist rotation: '+ str(value))
    wrist_joint.axis = (cos(value),0,sin(value))


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
disp = display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=-vector(0,1,2))

# Place buttons, radio buttons, a scrolling text object, and a slider
# in the right half of the window. Positions and sizes are given in
# terms of pixels, and pos(0,0) is the upper left corner of the window.
p = w.panel # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d,4), size=(L-2*d,d), label='3D representation.',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

toggle_grip = wx.Button(p, label='Toggle Grip', pos=(1.5*L+10,15))
toggle_grip.Bind(wx.EVT_BUTTON, rotateShoulderNeg)

max_height = 0.5*(hpedestal-pedestal_offset)*umi_scale*1000.0
min_height = 0

s0 = wx.Slider(p, pos=(1.0*L,0.2*L), size=(0.9*L,20), minValue=min_height, maxValue=max_height)
s0.Bind(wx.EVT_SCROLL, setRiserHeight)
s0_label = wx.StaticText(p, pos=(1.0*L,0.15*L), label='Set Riser height: '+str(0.9*0.5*hpedestal*umi_scale))

s1 = wx.Slider(p, pos=(1.0*L,0.4*L), size=(0.9*L,20), minValue=0.5*-pi*1000.0, maxValue=0.5*pi*1000.0)
s1.Bind(wx.EVT_SCROLL, setShoulderAngle)
s1_label = wx.StaticText(p, pos=(1.0*L,0.35*L), label='Set Shoulder rotation: 0')

s2 = wx.Slider(p, pos=(1.0*L,0.65*L), size=(0.9*L,20), minValue=0.5*-pi*1000.0, maxValue=0.5*pi*1000.0)
s2.Bind(wx.EVT_SCROLL, setElbowAngle)
s2_label = wx.StaticText(p, pos=(1.0*L,0.60*L), label='Set Elbow rotation: 0')

s3 = wx.Slider(p, pos=(1.0*L,0.9*L), size=(0.9*L,20), minValue=0.5*-pi*1000.0, maxValue=0.5*pi*1000.0, style=wx.SL_HORIZONTAL)
s3.Bind(wx.EVT_SCROLL, setWristAngle)
s3_label = wx.StaticText(p, pos=(1.0*L,0.85*L), label='Set Wrist rotation: 0')

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
frame0.pos = (-(wpedestal*umi_scale)/2.0, 0.5*hpedestal*umi_scale,0)

# The shoulder joint location is now on world position (x,z) = (0,0)
riser = frame(frame=frame0)
riser.pos = ((wpedestal*umi_scale)/2.0,0.9*frame0.pos.y, 0)

shoulder_joint = frame(frame=riser)
shoulder_joint.pos = (0,-(pedestal_offset*umi_scale), 0)
#shoulder_joint.rotate(axis = (0, 1, 0), angle = pi/4)

elbow_joint = frame(frame=shoulder_joint)
elbow_joint.pos = ((upper_length*umi_scale),-(upper_height*umi_scale), 0)
#elbow_joint.rotate(axis = (0, 1, 0), angle = pi/4)

wrist_joint = frame(frame=elbow_joint)
wrist_joint.pos = ((lower_length*umi_scale),-(lower_height*umi_scale), 0)
#wrist_joint.rotate(axis = (0, 1, 0), angle = pi/4)
#************************************************
# ROBOT ARM
pedestal = box(frame = frame0, 
               pos = (0,0,0),
               height = hpedestal*umi_scale,
               length = wpedestal*umi_scale,
               width = wpedestal*umi_scale,
               color = (0.4, 0.4, 0.4))
pointer_riser = box(frame = riser,
               pos = (0,0,0),
               height = 1,
               length = 0.1,
               width = 0.1,
               color = color.blue)
riser_part = cylinder(frame = riser,
               pos = (0, -pedestal_offset*umi_scale/2, 0),
               axis = (0, pedestal_offset*umi_scale, 0),
               radius = wpedestal*umi_scale/2,
               color = color.red)
                
pointer_shoulder = box(frame = shoulder_joint,
               pos = (0,0,0),
               height = 1,
               length = 0.1,
               width = 0.1,
               color = color.blue)
upper_arm = box(frame = shoulder_joint,
               pos = ((upper_length*umi_scale)/2.0,0,0),
               height = (upper_height*umi_scale),
               length = (upper_length*umi_scale)*1.2,
               width = 0.08*umi_scale,
               color = color.green)
pointer_elbow = box(frame = elbow_joint,
               pos = (0,0,0),
               height = 1,
               length = 0.1,
               width = 0.1,
               color = color.blue)
lower_arm = box(frame = elbow_joint,
               pos = ((lower_length*umi_scale)/2.0,0,0),
               height = (lower_height*umi_scale),
               length = (lower_length*umi_scale)*1.2,
               width = 0.08*umi_scale,
               color = color.green)
pointer_wrist = box(frame = wrist_joint,
               pos = (0,-(hpedestal*umi_scale)/2.0,0),
               height = hpedestal*umi_scale,
               length = 0.1,
               width = 0.1,
               color = color.blue)
wrist = box(frame = wrist_joint,
               pos = (0,0,0),
               height = wrist_height*umi_scale,
               length = 0.08*umi_scale,
               width = 0.08*umi_scale,
               color = color.green)

floor = box(frame=frameworld,
               pos = (0,0,0),
               height = 0.001,
               length = wpedestal*umi_scale + 0.6*umi_scale,
               width = 0.6*umi_scale*2,
               color = (0.5, 0.5, 0.5))
floor.pos = (floor.length/2 - (wpedestal*umi_scale), 0, 0)
#**************************************************************************
# CHESSBOARD

# Dimensions of the board
chessboard_size = umi_scale / 4.0
field_size = (chessboard_size / 8.0)
chessboard_dist = chessboard_size/2 - field_size

# Edges of the locations
wallthck = field_size / 15.0
wallhght = field_size / 15.0

# Position of the center of the board
mplhght = 0.2
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
                   height = 0.01,
                   length = field_size,
                   width = field_size,
                   pos = (field_size*x - field_size/2.0, 0, (chessboard_dist - field_size*y) + field_size/2),
                   color = board_color_dark)
            )
#***************************************************************************
# INIT CONTROLS
s0.SetValue(0.9*frame0.pos.y*1000.0)
s1.SetValue(0) # update the slider
s2.SetValue(0) # update the slider
s3.SetValue(0) # update the slider

#**************************************************************************
# CREATE CONTROLS
while(True):
    rate(100)

#End Program

0

