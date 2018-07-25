#!/usr/bin/env

# stdlib imports
import copy
from matplotlib import colors
import matplotlib.cm as cm
import matplotlib.colors as colors
import os

# third party imports
from impactutils.colors.cpalette import ColorPalette
import numpy as np
from openquake.hazardlib.geo.geodetic import point_at
from openquake.hazardlib.geo.utils import OrthographicProjection

# local imports
from fault.io.timeseries import read_from_directory
from fault.io.fsp import read_from_file


homedir = os.path.dirname(os.path.abspath(__file__))
COLORS = ColorPalette.fromFile(os.path.join(homedir, 'fault2.cpt'))


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

    def createGeoJSON(self):
        """
        Create the GeoJSON for the segment grid cells and earthquake point.

        Returns:
            dictionary: GeoJSON formatted dictionary.
        """
        segment_cells = []

        slips = np.asarray([])
        for segment in self.segments:
            slips = np.append(slips, segment['slip'].flatten())
        max_slip = np.ceil(np.max(slips))
        COLORS.vmax = max_slip

        for segment in self.segments:
            arr_size = len(segment['lat'].flatten())
            dx = [self.event['dx']/2] * arr_size
            dy = [self.event['dz']/2] * arr_size
            length = [self.event['dx']] * arr_size
            width = [self.event['dz']] * arr_size
            strike = [segment['strike']] * arr_size
            dip = [segment['dip']] * arr_size
            optional_properties = copy.deepcopy(segment)
            for key in ['dip', 'strike', 'lon', 'depth',
                    'slip', 'lat', 'length', 'width']:
                del optional_properties[key]
            for key in optional_properties:
                optional_properties[key] = optional_properties[key].flatten()

            px = segment['lon'].flatten()
            py = segment['lat'].flatten()
            pz = segment['depth'].flatten()
            slips = segment['slip'].flatten()

            # Verify that all are numpy arrays
            px = np.array(px, dtype='d')
            py = np.array(py, dtype='d')
            # depth should be in meters not in km
            pz = np.array(pz, dtype='d') * 1000
            dx = np.array(dx, dtype='d')
            dy = np.array(dy, dtype='d')
            length = np.array(length, dtype='d')
            width = np.array(width, dtype='d')
            strike = np.array(strike, dtype='d')
            dip = np.array(dip, dtype='d')

            # Get P1 and P2 (top horizontal points)
            theta = np.rad2deg(np.arctan((dy * np.cos(np.deg2rad(dip))) / dx))
            P1_direction = strike + 180 + theta
            P1_distance = np.sqrt( dx**2 + (dy * np.cos(np.deg2rad(dip)))**2)
            P2_direction = strike
            P2_distance = length
            P1_lon = np.asarray([])
            P1_lat = np.asarray([])
            P2_lon = np.asarray([])
            P2_lat = np.asarray([])
            for idx, value in enumerate(px):
                P1_points = point_at(px[idx], py[idx],
                        P1_direction[idx], P1_distance[idx])
                P1_lon = np.append(P1_lon, P1_points[0])
                P1_lat = np.append(P1_lat, P1_points[1])
                P2_points = point_at(P1_points[0], P1_points[1],
                        P2_direction[idx], P2_distance[idx])
                P2_lon = np.append(P2_lon, P2_points[0])
                P2_lat = np.append(P2_lat, P2_points[1])

            # Get top depth
            top_horizontal_depth = pz - 1000 * np.abs(dy * np.sin(np.deg2rad(dip)))

            group_index = np.array(range(len(P1_lon)))

            # Convert dip to radians
            dip = np.radians(dip)


            # Get a projection object
            west = np.min((P1_lon.min(), P2_lon.min()))
            east = np.max((P1_lon.max(), P2_lon.max()))
            south = np.min((P1_lat.min(), P2_lat.min()))
            north = np.max((P1_lat.max(), P2_lat.max()))

            # Projected coordinates are in km
            proj = OrthographicProjection(west, east, north, south)
            xp2 = np.zeros_like(P1_lon)
            xp3 = np.zeros_like(P1_lon)
            yp2 = np.zeros_like(P1_lon)
            yp3 = np.zeros_like(P1_lon)
            zpdown = np.zeros_like(top_horizontal_depth)
            for i, p1lon in enumerate(P1_lon):
                # Project the top edge coordinates
                p0x, p0y = proj(p1lon, P1_lat[i])
                p1x, p1y = proj(P2_lon[i], P2_lat[i])

                # Get the rotation angle defined by these two points
                if strike is None:
                    dx = p1x - p0x
                    dy = p1y - p0y
                    theta = np.arctan2(dx, dy)  # theta is angle from north
                elif len(strike) == 1:
                    theta = np.radians(strike[0])
                else:
                    theta = np.radians(strike[i])

                R = np.array([[np.cos(theta), -np.sin(theta)],
                              [np.sin(theta), np.cos(theta)]])

                # Rotate the top edge points into a new coordinate system (vertical
                # line)
                p0 = np.array([p0x, p0y])
                p1 = np.array([p1x, p1y])
                p0p = np.dot(R, p0)
                p1p = np.dot(R, p1)

                # Get right side coordinates in project, rotated system
                dz = np.sin(dip[i]) * width[i] * 1000
                dx = np.cos(dip[i]) * width[i]
                p3xp = p0p[0] + dx
                p3yp = p0p[1]
                p2xp = p1p[0] + dx
                p2yp = p1p[1]

                # Get right side coordinates in un-rotated projected system
                p3p = np.array([p3xp, p3yp])
                p2p = np.array([p2xp, p2yp])
                Rback = np.array([[np.cos(-theta), -np.sin(-theta)],
                                  [np.sin(-theta), np.cos(-theta)]])
                p3 = np.dot(Rback, p3p)
                p2 = np.dot(Rback, p2p)
                p3x = np.array([p3[0]])
                p3y = np.array([p3[1]])
                p2x = np.array([p2[0]])
                p2y = np.array([p2[1]])

                # project lower edge points back to lat/lon coordinates
                lon3, lat3 = proj(p3x, p3y, reverse=True)
                lon2, lat2 = proj(p2x, p2y, reverse=True)

                xp2[i] = lon2
                xp3[i] = lon3
                yp2[i] = lat2
                yp3[i] = lat3
                zpdown[i] = top_horizontal_depth[i] + dz

            # ---------------------------------------------------------------------
            # Create GeoJSON object
            # ---------------------------------------------------------------------

            u_groups = np.unique(group_index)
            n_groups = len(u_groups)
            polygons = []

            for i in range(n_groups):
                ind = np.where(u_groups[i] == group_index)[0]
                lons = np.concatenate(
                    [P1_lon[ind[0]].reshape((1,)),
                     P2_lon[ind], xp2[ind][::-1],
                     xp3[ind][::-1][-1].reshape((1,)),
                     P1_lon[ind[0]].reshape((1,))
                     ])
                lats = np.concatenate(
                    [P1_lat[ind[0]].reshape((1,)),
                     P2_lat[ind],
                     yp2[ind][::-1],
                     yp3[ind][::-1][-1].reshape((1,)),
                     P1_lat[ind[0]].reshape((1,))
                     ])
                deps = np.concatenate(
                    [top_horizontal_depth[ind[0]].reshape((1,)),
                     top_horizontal_depth[ind],
                     zpdown[ind][::-1],
                     zpdown[ind][::-1][-1].reshape((1,)),
                     top_horizontal_depth[ind[0]].reshape((1,))])

                poly = []
                for lon, lat, dep in zip(lons, lats, deps):
                    lon = np.around(lon, decimals=4)
                    lat = np.around(lat, decimals=4)
                    deps = np.around(deps, decimals=4)
                    coordinates = np.around(np.asarray([lon, lat, dep]),
                            decimals=5)
                    poly.append(coordinates.tolist())

                properties = {}
                for property in optional_properties:
                    properties[property] = optional_properties[property][i]
                h = COLORS.getDataColor(slips[i], color_format='hex')
                properties["slip"] = slips[i]
                properties["fill"] = h
                properties["stroke-width"] = 1.5
                properties["fill-opacity"] = 1
                d = {
                         "type": "Feature",
                         "properties": properties,
                         "geometry": {
                             "type": "Polygon",
                             "coordinates": [poly]
                         }
                     }
                polygons += [d]
            segment_cells += polygons
        features = {"type": "FeatureCollection",
             "metadata": {
                'epicenter': {
                 'location': self.event['location'],
                 'date': self.event['date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                 'depth': self.event['depth'],
                 'moment': self.event['moment'],
                 'mag': self.event['mag'],
                 'lon': self.event['lon'],
                 'lat': self.event['lat']
                 }
             },
             "features": segment_cells
             }
        self.corners = features


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
    def fromFiles(cls, fault_file, timeseries_directory):
        """Creates class instance with a fault model and time series.

        Args:
            fault_file (str): Path to finite fault (.fsp) file.
            input_directory (str): Path to directory of files.

        Returns:
            Fault: Fault object with all information set.
        """
        fault = cls()
        event, segments = read_from_file(fault_file)
        try:
            timeseries_dict = read_from_directory(timeseries_directory)
            fault.timeseries_dict = timeseries_dict
        except:
            warnings.warn('Time series files unavailable.')
        fault.segments = segments
        fault.event = event
        return fault

    @classmethod
    def fromFsp(cls, fault_file):
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
    def fromTimeseries(cls, timeseries_directory):
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
