#!/usr/bin/env python

#stdlib imports
import os
import glob

# third party imports
import pandas as pd
import numpy as np


# local imports
from fault.io.fsp import FSPFILE


def test_fsp():
    homedir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(homedir, '..', '..', 'data', 'fsp')
    fsp_locations = []
    for file_path in glob.glob(input_directory + '/*.fsp'):
            fsp_locations += [file_path]
    for fspfile in fsp_locations:
        # Get filename and initialize plotting objects
        fsp = FSPFile(fspfile)
        fig = plt.figure(figsize=(20, 20))
        counter = 0;
        # Loop through segments
        for num in range(fsp.getNumSegments()):
            # Get segment
            segment = fsp.getSegment(num)
            # Threshold slip
            thresholded_slip = fsp.thresholdSlip(segment['slip'])
            # Sum rows and columns
            sum_rows, sum_columns = fsp.sumSlip(thresholded_slip)
            # Autocorrelate summed rows and columns
            autocorrelated_rows, autocorrelated_columns = fsp.autocorrelateSums(
                    sum_rows,sum_columns)
            # Get rupture dimensions
            rupture_length, rupture_width = fsp.getRuptureSize(
                    autocorrelated_rows, autocorrelated_columns)
            # Get min and max of rupture in two directions
            left, right, top, bottom = fsp.getRuptureGrid(rupture_length,
                            rupture_width, thresholded_slip,
                            segment['length'], segment['width'])
            # Get corners as coordinates for primary segment
            if num == 0:
                corners = fsp.getCornerCoordinates(left, right, top, bottom,
                        segment['lon'], segment['lat'])



if __name__ == '__main__':
    test_fsp()
