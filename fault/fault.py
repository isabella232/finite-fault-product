#!/usr/bin/env

# third party imports
import numpy as np

# local imports
from fault.io.timeseries import read_from_directory
from fault.io.fsp import read_from_file


class Fault(object):
    """Class for analyzing a fault and associated information."""
    def __init__(self):
        self._event = None
        self._segments = None
        self._timeseries_dict = None

    def autocorrelateSums(self, rows, columns):
        """Return slips summed along each axis and autocorrelated.

        Args:
            rows (nd.array): Array of slips summed along the rows.
            columns (nd.array): Array of slips summed along the columns.
        Returns:
            tuple: autocorrelated rows and columns
        """
        rows_copy = rows.copy()
        columns_copy = columns.copy()
        autocorrelated_rows = self._autocorrelate(rows_copy)
        autocorrelated_columns = self._autocorrelate(columns_copy)
        return (autocorrelated_rows, autocorrelated_columns)

    @property
    def event(self):
        """
        Helper to return event dictionary.

        Returns:
            dictionary: Event information.
        """
        return self._event

    @event.setter
    def event(self, event):
        """
        Helper to set event dictionary.

        event (dictionary): Event information.
        """
        self._event = event

    @classmethod
    def from_files(cls, fault_file, timeseries_directory):
        """Creates class instance with a fault model and time series.

        Args:
            fault_file (str): Path to finite fault (.fsp) file.
            input_directory (str): Path to directory of files.

        Returns:
            Fault: Fault object with all information set.
        """
        event, segments = read_from_file(fault_file)
        timeseries_dict = read_from_directory(timeseries_directory)
        fault = cls()
        fault.segments = segments
        fault.event = event
        fault.timeseries_dict = timeseries_dict
        return fault

    @classmethod
    def from_fsp(cls, fault_file):
        """Creates class instance with a fault model.

        Args:
            fault_file (str): Path to finite fault (.fsp) file.

        Returns:
            Fault: Fault object with fault model information set.
        """
        event, segments = read_from_file(fault_file)
        fault = cls()
        fault.segments = segments
        fault.event = event
        return fault

    @classmethod
    def from_timeseries(cls, timeseries_directory):
        """Creates class instance with time series data.

        Args:
            input_directory (str): Path to directory of files.

        Returns:
            Fault: Fault object with time series information set.
        """
        timeseries_dict = read_from_directory(timeseries_directory)
        fault = cls()
        fault.timeseries_dict = timeseries_dict
        return fault

    def getRuptureSize(self, rows, columns):
        """Return rupture length and width.

        Args:
            rows (nd.array): Array of slips, summed along the rows and autocorrelated.
            columns (nd.array): Array of slips, summed along the columns and autocorrelated.
        Returns:
            tuple: rupture length and width
        """
        dx = self.event['dx']
        dz = self.event['dz']
        rows_copy = rows.copy()
        columns_copy = columns.copy()

        # Integrate to get the area under the curve
        row_area = np.trapz(rows_copy, dx=dx)
        column_area = np.trapz(columns_copy, dx=dz)

        # Normalize by the t=0 (or maximum) value
        rupture_length = row_area / rows_copy.max()
        rupture_width = column_area / columns_copy.max()
        return (rupture_length, rupture_width)

    def getRuptureGrid(self, length, width, thresholded_slip, fault_length, fault_width):
        dx = self.event['dx']
        dz = self.event['dz']

        # Initialize values
        left_location = 0
        right_location = left_location + length
        top_location = 0
        bottom_location = top_location + width
        max_left = -1
        max_right = -1
        max_top = -1
        max_bottom = -1
        max_area = -1

        # Find maximum area within a grid
        while right_location < fault_length :
            top_location = 0
            bottom_location = top_location + width

            # Get indices of min an max length
            left_idx = int(np.floor(left_location / dx))
            right_idx = int(np.floor(right_location / dx))
            left_location += dx
            right_location += dx
            while bottom_location < fault_width:
                # Get indices of min an max width
                top_idx = int(np.floor(top_location / dz))
                bottom_idx = int(np.floor(bottom_location / dz))
                top_location += dz
                bottom_location += dz

                # Sum subarray of the thesholded slip
                subarray = thresholded_slip[top_idx : bottom_idx, left_idx : right_idx]
                area = np.sum(subarray)
                if area > max_area:
                    max_left = left_idx
                    max_right = right_idx
                    max_top = top_idx
                    max_bottom = bottom_idx
                    max_area = area

        # Set final min and max values in both directions
        left = max_left
        right = max_right
        top = max_top
        bottom = max_bottom
        return left, right, top, bottom

    def getRuptureCorners(self, window, dd, length, sum_rows, sum_columns):
        """Return rupture length and width.

        Args:
            window (float): Length/width across rupture.
            length (float): Length/width defined in the file.
            dd (float): Spacing between values.
            sum_rows (nd.array): Slip values summed along the rows.
            sum_collumns (nd.array): Slip values summed alon the collumns.
        Returns:
            Tuple: Indices of min and max locations in a given direction.
        """
        # Initialize values
        first_location = 0
        last_location = first_location + window
        max_first = -1
        max_last = -1
        max_area = -1

        # Find min and max values in two directions
        while last_location < length:
            first_idx = int(np.floor(first_location/dd))
            last_idx = int(np.floor(last_location/dd))
            first_location += dd
            last_location += dd
            subarray = sum_rows[first_idx:last_idx]
            area = np.trapz(subarray,dx=dd)
            if area > max_area:
                max_first = first_idx
                max_last = last_idx
                max_area = area
        return (max_first, max_last)

    def getCornerCoordinates(self, left, right, top, bottom, lon, lat):
        """Return rupture length and width.

        Args:
            left (int): Left index.
            right (int): Right index.
            top (int): Top index.
            bottom (int): Bottom index.
            lon (nd.array): Array of longitude values.
            lat (nd.array): Arrau of latitude values.
        Returns:
            Dict: Dictionary of corner coordinates.
        """
        gP1x = lon[top, left]
        gP1y = lat[top, left]

        gP2x = lon[top, right]
        gP2y = lat[top, right]

        gP3x = lon[bottom, right]
        gP3y = lat[bottom, right]

        gP4x = lon[bottom, left]
        gP4y = lat[bottom, left]
        corners = {}
        corners['P1'] = (gP1x, gP1y)
        corners['P2'] = (gP2x, gP2y)
        corners['P3'] = (gP3x, gP3y)
        corners['P4'] = (gP4x, gP4y)
        return corners

    def getNumSegments(self):
        """Return the number of rupture segments contained in the file.

        Returns:
            int: Number of rupture segments.
        """
        return len(self.segments)

    def getSegment(self,idx=0):
        """Return an individual segment dictionary.

        Args:
            idx (int): Desired segment number (0 offset).
        Returns:
            dict: Segment dictionary, containing fields:
                  - strike Along-strike axis direction.
                  - dip Dip angle.
                  - lat 2D numpy array of latitudes.
                  - lon 2D numpy array of longitudes.
                  - slip 2D numpy array of slip, in meters.
        """
        if idx > len(self.segments)-1 or idx < 0:
            fmt = 'Index %i exceeds number of segments %i'
            raise IndexError(fmt % (idx,len(self.segments)))
        return self.segments[idx]

    @property
    def segments(self):
        """
        Helper to return list of segments.

        Returns:
            list: List of segments (dict)
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Helper to set list of segments.

        segments (list): List of segments (dict)
        """
        self._segments = segments

    def sumSlip(self, slip):
        """Return slips summed along each axis.

        Args:
            slip (nd.array): Array of slips to sum.
        Returns:
            tuple: summed rows and summed columns
        """
        slip_copy = slip.copy()
        sum_rows = slip_copy.sum(axis=0)
        sum_columns = slip_copy.sum(axis=1)
        return (sum_rows, sum_columns)

    def thresholdSlip(self, slip):
        """Return slips filtered within the threshold.

        Args:
            slip (nd.array): Array of slips to filter.
        Returns:
            nd.array: Array of thresholded slips
        """
        thresholded_slip = slip.copy()
        slip_thresh = slip.max()*0.1
        if slip_thresh < 1:
            slip_thresh=1.0
        if thresholded_slip.max() <1:
            slip_thresh=0.2
        if thresholded_slip.max() < 3:
            slip_thresh=0.5
        thresholded_slip[thresholded_slip < slip_thresh] = 0
        return thresholded_slip

    @property
    def timeseries_dict(self):
        """
        Helper to return time series dictionary.

        Returns:
            dictionary: Dictionary of time series for each station.
        """
        return self._timeseries_dict

    @timeseries_dict.setter
    def timeseries_dict(self, timeseries_dict):
        """
        Helper to set time series dictionary.

        segmtimeseries_dictents (dictionary): Dictionary of time series for
                each station.
    """
        self._timeseries_dict = timeseries_dict

    def _autocorrelate(self, x):
        """Autocorrelate a 1D array.

        Args:
            x (nd.array): 1D array of data.

        Returns:
            nd.array: autocorrelated data
        """
        result = np.correlate(x,x,mode='full')[len(x)//2:]
        return result
