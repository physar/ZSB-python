#!python2
from __future__ import division, print_function
import csv

def to_coordinate(notation):
    """ Given a notation in the form [a1-h8], return the corresponding notation
        (0-7, 0-7)
        :param str notation: Location of a field on the board

        :return: Tuple internal coordinates of the field.
    """
    x = ord(notation[0]) - ord('a')
    z = int(notation[1]) - 1
    return (x, z)

def to_notation(coordinates):
    """ Given a board coordinate in the form (0-7, 0-7), return the corresponding notation
        [a1-h8]
        :param tuple coordinates: Tuple containing the internal coordinates on the board.

        :return: String in the form 'a1'
    """
    (x,z) = coordinates
    letter = chr(ord('a') + x)
    number = z + 1
    return letter + str(number)

def write_parameters_to_file(parameter_lines, output_file):
    with open(output_file, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(['Riser', 'Shoulder', 'Elbow', 'Wrist', 'Gripper'])
        for line in parameter_lines:
            csv_writer.writerow(line)

def read_parameters_from_file(input_file):
    with open(input_file, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        parameter_lines = []
        for line in csv_reader:
            parameter_lines.append([float(x) for x in line])
    return (headers, parameter_lines)