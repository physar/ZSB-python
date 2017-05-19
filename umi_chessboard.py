from __future__ import division, print_function
from visual import *
from visual.graph import *
from visual.controls import *

class UMI_chessboard:
    def __init__(self, frameworld, board_size=0.3, position_x_z = (0.15, -0.15), angle_degrees=0):
        # Dimensions of the board
        self.chessboard_size = board_size
        self.field_size = (self.chessboard_size / 8.0)

        # Edges of the locations
        self.wallthck = self.field_size / 15.0
        self.wallhght = self.field_size / 15.0

        # Position of the center of the board
        self.mplhght = (self.chessboard_size / 15.0)
        self.mplcent = self.chessboard_size

        # Colors of the board
        self.board_color_light = (1.0, 1.0, 1.0)
        self.board_color_dark = (1.0, 0.5, 1.0)
        self.beam_color = (0.9, 0.9, 0.9)

        self.framemp = frame(frame=frameworld)
        self.framemp.pos =(0, self.mplhght,0)
        
        # Create the board on screen
        self.generate_board()
        
        # Set the angle and position of the board, where the rotational axis is H8
        self.set_pos_angle(position_x_z, angle_degrees)
    
    def get_board_height(self):
        return self.mplhght
    
    def set_angle_radians(self, radians):
        ## Rotate the board
        self.framemp.axis = (cos(radians),0,sin(radians))
        self.board_angle = radians
    
    def set_angle_degrees(self, degrees):
        ## Rotate the board
        self.set_angle_radians(radians(degrees))
    
    def get_angle_radians(self):
        return self.board_angle
    
    def get_angle_degrees(self):
        ## Rotate the board
        return degrees(self.get_angle_radians())
    
    def set_position(self, x, z):
        self.framemp.pos.x = x
        self.framemp.pos.z = z
    
    def get_position(self):
        return (self.framemp.pos.x, self.framemp.pos.y, self.framemp.pos.z)
    
    def set_pos_angle(self, position_x_z, angle_degrees):
        self.set_position(position_x_z[0], position_x_z[1])
        self.set_angle_degrees(angle_degrees)
    
    def generate_board(self):
        self.mchessboard = box(frame = self.framemp,
                       height = self.mplhght,
                       length = self.chessboard_size,
                       width = self.chessboard_size,
                       pos = (0.5*self.chessboard_size, -0.5*self.mplhght, 0.5*self.chessboard_size),
                       color = self.board_color_light)
        
        # Draw the beams to create 64 squares
        self.width_beams = []
        self.vert_beams = []
        for field in range(8):
            beam_offset = field * (self.chessboard_size / 8.0)
            self.width_beams.append(box(frame = self.framemp,
                       height = self.wallhght,
                       length = self.wallthck,
                       width = self.mchessboard.width,
                       pos = (beam_offset+(0.5*self.wallthck), 0.5*self.wallhght, 0.5*self.mchessboard.width),
                       color = self.beam_color)
            )
            self.vert_beams.append(box(frame = self.framemp,
                       height = self.wallhght,
                       length = self.mchessboard.length,
                       width = self.wallthck,
                       pos = (0.5*self.mchessboard.length, 0.5*self.wallhght, beam_offset+(0.5*self.wallthck)),
                       color = self.beam_color)
            )
        self.width_beams.append(box(frame = self.framemp,
                       height = self.wallhght,
                       length = self.wallthck,
                       width = self.mchessboard.width,
                       pos = (self.chessboard_size-(0.5*self.wallthck), 0.5*self.wallhght, 0.5*self.mchessboard.width),
                       color = self.beam_color)
        )
        self.vert_beams.append(box(frame = self.framemp,
                       height = self.wallhght,
                       length = self.mchessboard.length,
                       width = self.wallthck,
                       pos = (0.5*self.mchessboard.length, 0.5*self.wallhght, self.chessboard_size-(0.5*self.wallthck)),
                       color = self.beam_color)
        )
        
        self.fields = []
        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    self.fields.append( box(frame = self.framemp,
                           height = 0.001,
                           length = self.field_size,
                           width = self.field_size,
                           pos = (self.field_size*(x+1) - self.field_size/2.0, 0, (self.field_size*y) + self.field_size/2),
                           color = self.board_color_dark)
                    )