#!/usr/bin/env python

"""
See comments in correspondences_from_tags.py.  Here we read the file 'known_correspondences.csv' then interpolate pixel-to-robot-coordinate mappings.

Note that this is NOT a ROS script.  It is just sitting here for convenience.

Andrew Vardy
"""
import sys
import csv
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np
import common_calib
import numpy.ma as ma
from math import isnan, sqrt

def main():
    interpolate('known_correspondences.csv', common_calib.output_width, common_calib.output_height)
    
def interpolate(filename_in, width, height):

    # Resolution string
    #resString = str(width) + 'x' + str(height)

    xmin = 0
    xmax = width-1
    ymin = 0
    ymax = height-1

    #filename = baseDir + robot + '/phase1_' + resString + '.csv'
    [x, y, Xr, Yr] = readPhase1File(filename_in)

    # Plot the seed values as obtained from phase 1
    plt.subplot(1, 2, 1)
    plt.title('Phase 1: Xr')
    plt.scatter(x, y, c=Xr)
    plt.axis([xmin, xmax, ymax, ymin])
    plt.colorbar()
    plt.subplot(1, 2, 2)
    plt.title('Phase 1: Yr')
    plt.scatter(x, y, c=Yr)
    plt.axis([xmin, xmax, ymax, ymin])
    plt.colorbar()
    plt.show()

    # Generate image coordinates for all pixels
    xi = np.linspace(xmin, xmax, width)
    yi = np.linspace(ymin, ymax, height)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate Xr and Yr
    x_array = np.array(x)
    y_array = np.array(y)
    Xr_array = np.array(Xr)
    Yr_array = np.array(Yr)
    Xr_interp = griddata((x_array, y_array), Xr_array, (xi, yi), method='cubic')
    Yr_interp = griddata((x_array, y_array), Yr_array, (xi, yi), method='cubic')

    # Cut out region around robot
    if common_calib.exclude_radius != None:
        n = Xr_interp.shape[0]
        assert n == Yr_interp.shape[0]
        rows_to_delete = []
        for i in range(height):
            for j in range(width):
                xr = Xr_interp[i, j]
                yr = Yr_interp[i, j]
                #if (not ma.is_masked(xr)
                #   and sqrt(xr*xr + yr*yr) < common_calib.exclude_radius):
                #    Xr_interp[i, j] = ma.masked
                #    Yr_interp[i, j] = ma.masked
                if (not isnan(xr)
                   and sqrt(xr*xr + yr*yr) < common_calib.exclude_radius):
                    Xr_interp[i, j] = float('nan')
                    Yr_interp[i, j] = float('nan')

    # Plot the interploated values as obtained from phase 2
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title('Phase 2: Xr')
    plt.pcolormesh(xi, yi, Xr_interp)
    plt.scatter(x, y, c=Xr, marker='.')
    plt.axis([xmin, xmax, ymax, ymin])
    plt.colorbar()
    plt.subplot(1, 2, 2)
    plt.title('Phase 2: Yr')
    plt.pcolormesh(xi, yi, Yr_interp)
    plt.scatter(x, y, c=Yr, marker='.')
    plt.axis([xmin, xmax, ymax, ymin])
    plt.colorbar()
    plt.show()

    # Write to the output file in CSV format where the first two columns
    # are the (x, y) coordinates in image space and the next two columns
    # are the corresponding interpolated (Xr, Yr) coordinates in robot space.
    filename_out = 'interpolated_correspondences.csv'
    with open(filename_out, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['xi', 'yi', 'Xr', 'Yr'], \
                                delimiter=',')
        csvfile.write('# ')
        writer.writeheader()
        for j in range(height):
            for i in range(width):
                #if not Xr_interp.mask[j][i] and not Yr_interp.mask[j][i]:
                if not isnan(Xr_interp[j][i]) and not isnan(Yr_interp[j][i]):
                    rowDict = {'xi':int(xi[j][i]), \
                               'yi':int(yi[j][i]), \
                               'Xr':float(Xr_interp[j][i]), \
                               'Yr':float(Yr_interp[j][i])}
                    writer.writerow(rowDict)

def readPhase1File(filename):
    f = open(filename, 'rt')
    x = []
    y = []
    Xr = []
    Yr = []
    try:
        reader = csv.reader(f, delimiter=',')
        # Skip the first (header) row
        next(reader)
        for row in reader:
            x.append(int(row[0]))
            y.append(int(row[1]))
            Xr.append(float(row[2]))
            Yr.append(float(row[3]))
        return [x, y, Xr, Yr]
    finally:
        f.close()

main()
