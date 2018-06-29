 #!/usr/bin/env

# Standard library imports
import re
from datetime import datetime

# Third party imports
import numpy as np



class FSPFile(object):
    def __init__(self,fspfile):
        """Read all relevant data from Finite Fault FSP file.

        Args:
            fspfile (str or file-like object): Input FSP file.
        """
        if isinstance(fspfile,str):
            self._fspfile = open(fspfile,'r')
        else:
            self._fspfile = fspfile

        # create an event dictionary with:
        # location
        # date (no time)
        # lat
        # lon
        # depth
        # magnitude
        # moment
        self._event = {}
        is_multi = False
        lc = 0

        # Read event information
        for line in self._fspfile.readlines():
            lc += 1
            if not line.startswith('%'):
                break
            if line.startswith('% Event :'):
                # remove stuff in between []
                try:
                    newline = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", line)
                    newline = re.sub('[^a-zA-Z0-9\s\:]*','',newline)
                    # get date string
                    datestring = re.search('[0-9]{8}',newline).group()
                    newline = newline.replace(datestring,'')
                    self._event['date'] = datetime.strptime(datestring,'%Y%m%d')
                except:
                    self._event['date'] = 'UNK'
                self._event['location'] = newline.split(':')[1].strip()
            if 'Loc ' in line:
                parts = line.split(':')[1].strip().split()
                self._event['lat'] = float(parts[2])
                self._event['lon'] = float(parts[5])
                self._event['depth'] = float(parts[8])
            if 'Size' in line:
                parts = line.split(':')[1].strip().split()
                length = float(parts[2])
                width = float(parts[6])
                self._event['mag'] = float(parts[10])
                self._event['moment'] = float(parts[13])
            if 'Dx' in line:
                parts = line.split(':')[1].strip().split()
                dx = float(parts[2])
                dz = float(parts[6])
                self._event['dx'] = dx
                self._event['dz'] = dz

            if 'MULTISEGMENT' in line:
                is_multi = True
            if 'Mech' in line:
                parts = line.split(':')[1].strip().split()
                strike = float(parts[2])
                dip = float(parts[5])

        # Get segment dimensions
        self._fspfile.close()
        nx = int(np.round_(length/dx, 2))
        nz = int(np.round_(width/dz, 2))
        # in some versions of numpy, you can't read open text files.
        data = np.genfromtxt(fspfile,max_rows=nx*nz,skip_header=lc-1).T
        lc += (nx*nz)-1
        self._fspfile = open(fspfile,'r')
        for _ in range(lc):
            line = next(self._fspfile)

        # Reshape data to proper dimensions
        lat = data[0].reshape(nz,nx)
        lon = data[1].reshape(nz,nx)
        slip = data[5].reshape(nz,nx)
        depth = data[4].reshape(nz,nx)

        # Store segment
        segment = {'strike':strike,
                   'dip':dip,
                   'lat':lat.copy(),
                   'lon':lon.copy(),
                   'depth':depth.copy(),
                   'slip':slip.copy(),
                   'length': length,
                   'width': width}
        self._segments = [segment]

        # Get multiple segments
        if is_multi:
            while True:
                for line in self._fspfile.readlines():
                    lc += 1
                    if not line.startswith('%'):
                        break
                    if 'SEGMENT' in line:
                        parts = line.split(':')[1].strip().split()
                        strike = float(parts[2])
                        dip = float(parts[6])
                    if 'LEN' in line:
                        parts = line.split()
                        length = float(parts[3])
                        width = float(parts[7])
                else:
                    break
                self._fspfile.close()
                nx = int(np.round_(length/dx, 2))
                nz = int(np.round_(width/dz, 2))

                # Import data
                data = np.genfromtxt(fspfile,max_rows=nx*nz,skip_header=lc-1).T
                lc += (nx*nz)-1

                # Reshape data into the proper dimensions
                self._fspfile = open(fspfile,'r')
                for _ in range(lc):
                    next(self._fspfile)
                lat = data[0].reshape(nz,nx)
                lon = data[1].reshape(nz,nx)
                slip = data[5].reshape(nz,nx)
                depth = data[4].reshape(nz,nx)

                # Store segment
                segment = {'strike':strike,
                   'dip':dip,
                   'lat':lat.copy(),
                   'lon':lon.copy(),
                   'depth':depth.copy(),
                   'slip':slip.copy(),
                   'length': length,
                   'width': width}
                self._segments.append(segment)

        # close fspfile object when done
        self._fspfile.close()

    def _autocorrelate(self, x):
        """Autocorrelate a 1D array.

        Args:
            x (nd.array): 1D array of data.

        Returns:
            nd.array: autocorrelated data
        """
        result = np.correlate(x,x,mode='full')[len(x)//2:]
        return result

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

    def getRuptureSize(self, rows, columns):
        """Return rupture length and width.

        Args:
            rows (nd.array): Array of slips, summed along the rows and autocorrelated.
            columns (nd.array): Array of slips, summed along the columns and autocorrelated.
        Returns:
            tuple: rupture length and width
        """
        dx = self._event['dx']
        dz = self._event['dz']
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
        dx = self._event['dx']
        dz = self._event['dz']

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
        return len(self._segments)

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
        if idx > len(self._segments)-1 or idx < 0:
            fmt = 'Index %i exceeds number of segments %i'
            raise IndexError(fmt % (idx,len(self._segments)))
        return self._segments[idx]

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
