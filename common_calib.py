#!/usr/bin/env python  

"""
Constants and common functionality for the calibration process.  The term
'target' here is generic and could mean an AprilTag fiducial or any other
marker.
"""

from math import floor

image_filename = 'grid_640x480.jpg'
    
# The (xr, yr) position of the upper-left target in the calibration grid,
# measured in cm.
upper_left_x = 3 * 10.16
upper_left_y = 3 * 10.16

# The distance between targets (assuming that the same distance exists between
# rows as between columns).
inter_target_distance = 10.16

# Width in targets.  In other words, the number of targets in a row
width_in_targets = 7

# Height in targets---the number of targets in a column
height_in_targets = 4

# Whether to exclude the origin when picking.
exclude_origin = False

# Radius around origin to exclude when running 'interpolator.py'.  Set to None
# to disable exclusion.
exclude_radius = None

# Dimensions of output.
output_width = 80
output_height = 60

def get_corresponding_point(index):
    """
    Return the (xr, yr) tuple associated with the target with the given index.
    The index values are assumed to start at 0 for the upper-left target and
    increase from left-to-right and top-to-bottom.

    Its very important to note that the robot reference frame has its x-axis
    aligned with the robot's forward's direction and its y-axis oriented 90
    degrees counter-clockwise to this.  Thus, rows in the calibration grid
    all have the same xr coordinates, but vary in their yr coordinates.
    """

    row = floor(index / width_in_targets)
    col = index - row * width_in_targets

    return (upper_left_x - row * inter_target_distance, \
            upper_left_y - col * inter_target_distance)
