#!python2

from __future__ import division, print_function

class UMI_parameters:
    def __init__(self):
        # Specifications of UMI
        # Zed
        self.hpedestal = 1.082
        self.pedestal_offset = 0.0675
        self.wpedestal = 0.1 # Undefined in real robot

        # Dimensions upper arm
        self.upper_length = 0.2535
        self.upper_height = 0.095

        # Dimensions lower arm
        self.lower_length = 0.2535
        self.lower_height = 0.08

        # Dimensions wrist
        self.wrist_height = 0.09

        # Height of the arm from the very top of the riser, to the tip of the gripper.
        self.total_arm_height = self.pedestal_offset + self.upper_height \
                                + self.lower_height + self.wrist_height

        # Joint-ranges in meters (where applicable e.g. Riser, Gripper) and in degrees for the rest.
        self.joint_ranges = {
            "Riser"     : [0, 0.925],
            "Shoulder"  : [-90, 90],
            "Elbow"     : [-180, 110],
            "Wrist"     : [-110, 110],
            "Gripper"   : [0, 0.05]
        }

    def correct_height(self, y):
        '''
            Function that corrects the y value of the umi-rtx, because the real arm runs from
            from -self.hpedestal/2 to self.hpedestal/2, while y runs from 0 to self.hpedestal.
        '''
        return y - 0.5*self.hpedestal
