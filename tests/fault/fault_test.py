#!/usr/bin/env python

#stdlib imports
import os
import glob

# local imports
from fault.fault import Fault


def test_from_files():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'timeseries')
    fspfile = os.path.join(homedir, '..', 'data', 'fsp', '1000dyad.fsp')
    fault = Fault.from_files(fspfile, ts_directory)
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
    fault = Fault.from_fsp(fspfile)
    fault = Fault.from_timeseries(ts_directory)


if __name__ == '__main__':
    test_from_files()
