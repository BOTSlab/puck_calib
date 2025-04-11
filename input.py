#!/usr/bin/env python  

"""
Specification of the input image and the parameters of the calibration grid.
"""

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