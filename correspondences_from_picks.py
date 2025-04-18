#!/usr/bin/env python

"""
This script prompts the user to pick known points on the calibration grid, associates them with known positions, and writes these correspondences to a comma-separated file where each row contains xi, yi, xr, yr:
    (xi, yi): Image coordinates
    (xr, yr): Coordinates of the corresponding point in the robot reference
              frame (i.e. the /base_link frame).

This is an alternative procedure to 'correspondences_from_tags' which operates on detected AprilTags through ROS (this is not a ROS script).

This is really the first step of the calibration process.  The second is achieved by 'interpolator.py' which reads 'known_correspondences.csv' and interpolates correspondences between them.

Andrew Vardy
"""
import sys
import csv
import common_picking
import common_calib
from input import *

def main():
    filename_out = 'known_correspondences.csv'

    robotCoords = []
    id = 0
    for j in range(common_calib.height_in_targets):
        for i in range(common_calib.width_in_targets):
            (xr, yr) = common_calib.get_corresponding_point(id)
            
            if (not common_calib.exclude_origin) or (xr != 0 or yr != 0):
                robotCoords.append((xr, yr))
            id += 1
    print(robotCoords)

    print('''
    Please click on the centre of the targets (left click performs a click,
    right click does an undo) ordered from left-to-right and top-to-bottom.
    ''')
    if common_calib.exclude_origin:
        print("\nDo not select the origin (middle).")
        
    pickList = common_picking.pick(common_calib.image_filename, robotCoords)

    # Write to the output file in CSV format where the first two columns
    # are the (x, y) coordinates in image space and the next two columns
    # are the corresponding (Xr, Yr) coordinates in robot space.
    with open(filename_out, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['xi', 'yi', 'xr', 'yr'], \
                                delimiter=',')
        csvfile.write('# ')
        writer.writeheader()
        for row in range(len(robotCoords)):
            xy = pickList[row]
            robotCoord = robotCoords[row]
            rowDict = {'xi':int(xy[0]), \
                       'yi':int(xy[1]), \
                       'xr':robotCoord[0], \
                       'yr':robotCoord[1] }
            writer.writerow(rowDict)

main()
