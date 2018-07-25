#!/usr/bin/env python

# stdlib imports
import os
import glob

# third party imports
import numpy as np

# local imports
from fault.fault import Fault


def test_fromFiles():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
    fspfile = os.path.join(homedir, '..', 'data', 'products', '1000dyad',
            '1000dyad.fsp')
    fault = Fault.fromFiles(fspfile, ts_directory)
    # Loop through segments
    for num in range(fault.getNumSegments()):
        # Get segment
        segment = fault.getSegment(num)
        # Threshold slip
        thresholded_slip = fault.thresholdSlip(segment['slip'])
        # Sum rows and columns
        sum_rows, sum_columns = fault.sumSlip(thresholded_slip)
        # Autocorrelate summed rows and columns
        autocorrelated_rows, autocorrelated_columns = fault.autocorrelateSums(
                sum_rows,sum_columns)
        # Get rupture dimensions
        rupture_length, rupture_width = fault.getRuptureSize(
                autocorrelated_rows, autocorrelated_columns)
        # Get min and max of rupture in two directions
        left, right, top, bottom = fault.getRuptureGrid(rupture_length,
                        rupture_width, thresholded_slip,
                        segment['length'], segment['width'])
        # Get corners as coordinates for primary segment
        if num == 0:
            fault.getCornerCoordinates(left, right, top, bottom,
                    segment['lon'], segment['lat'])
        fault.getRuptureCorners(segment['width'],
                segment['length']/len(sum_rows),
                segment['length'], sum_rows, sum_columns)
    assert isinstance(fault.timeseries_dict, dict)
    fault.createGeoJSON()

    corner_file = ts_directory = os.path.join(homedir, '..', 'data',
            'ffm_data', '1000dyad_slip.out')
    target_lon, target_lat, target_depth = np.loadtxt(corner_file,
            unpack=True, usecols=(0,1,3), comments='>')

    calc_corners = fault.corners
    calc_lat = np.asarray([])
    calc_lon = np.asarray([])
    calc_depth = np.asarray([])

    for corner in calc_corners["features"]:
        for idx, coord in enumerate(corner['geometry']['coordinates'][0]):
            if idx != len(corner['geometry']['coordinates'][0]) - 1:
                calc_lon = np.append(calc_lon, [coord[0]])
                calc_lat = np.append(calc_lat, [coord[1]])
                calc_depth = np.append(calc_depth, [coord[2]/1000])
    np.testing.assert_allclose(calc_lat, target_lat, rtol=1e-04)
    np.testing.assert_allclose(calc_lon, target_lon, rtol=1e-04)
    np.testing.assert_allclose(calc_depth, target_depth)

    fault = Fault.fromFsp(fspfile)
    fault = Fault.fromTimeseries(ts_directory)




if __name__ == '__main__':
    test_fromFiles()
