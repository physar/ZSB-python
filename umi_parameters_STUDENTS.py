#!python2

from __future__ import division, print_function

class UMI_parameters:
    def __init__(self):
        # Specifications of UMI
        # Zed
        self.hpedestal = ???? #in meters
        self.pedestal_offset = ???? #in meters
        self.wpedestal = 0.1 # Undefined in real robot

        # Dimensions upper arm
        self.upper_length = ???? #in meters
        self.upper_height = ???? #in meters

        # Dimensions lower arm
        self.lower_length = ???? #in meters
        self.lower_height = ???? #in meters

        # Dimensions wrist
        self.wrist_height = ???? #in meters

        # Height of the arm from the very top of the riser, to the tip of the gripper.
        self.total_arm_height = self.pedestal_offset + self.upper_height \
                                + self.lower_height + self.wrist_height

        # Joint-ranges in meters (where applicable e.g. Riser, Gripper) and in degrees for the rest.
        self.joint_ranges = {
            "Riser"     : [self.total_arm_height, self.hpedestal],
            "Shoulder"  : [???? mimimum degrees, ???? maximum degrees],
            "Elbow"     : [???? mimimum degrees, ???? maximum degrees],
            "Wrist"     : [???? mimimum degrees, ???? maximum degrees],
            "Gripper"   : [0, 0.05]
        }

    def correct_height(self, y):
        '''
            Function that corrects the y value of the umi-rtx, because the real arm runs from
            from -self.hpedestal/2 to self.hpedestal/2, while y runs from 0 to self.hpedestal.
        '''
        return y - 0.5*self.hpedestal
