#!/usr/bin/env

# Standard library imports
import re
from datetime import datetime

# Third party imports
import numpy as np

DEFAULT_HEADERS = ['LAT', 'LON', 'X==EW', 'Y==NS', 'Z', 'SLIP', 'RAKE',
        'TRUP', 'RISE', 'SF_MOMENT']


def read_from_file(fspfile, headers=DEFAULT_HEADERS):
    """
    Read all relevant data from Finite Fault FSP file.

    Args:
        fspfile (str or file-like object): Input FSP file.
    """
    if isinstance(fspfile,str):
        _fspfile = open(fspfile,'r')
    else:
        _fspfile = fspfile

    # create an event dictionary with:
    # location
    # date (no time)
    # lat
    # lon
    # depth
    # magnitude
    # moment
    event = {}
    is_multi = False
    lc = 0

    # Read event information
    for line in _fspfile.readlines():
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
                event['date'] = datetime.strptime(datestring,'%Y%m%d')
            except:
                event['date'] = 'UNK'
            event['location'] = newline.split(':')[1].strip()
        if 'Loc ' in line:
            parts = line.split(':')[1].strip().split()
            event['lat'] = float(parts[2])
            event['lon'] = float(parts[5])
            event['depth'] = float(parts[8])
        if 'Size' in line:
            parts = line.split(':')[1].strip().split()
            length = float(parts[2])
            width = float(parts[6])
            event['mag'] = float(parts[10])
            event['moment'] = float(parts[13])
        if 'Dx' in line:
            parts = line.split(':')[1].strip().split()
            dx = float(parts[2])
            dz = float(parts[6])
            event['dx'] = dx
            event['dz'] = dz
        if 'MULTISEGMENT' in line:
            is_multi = True
        if 'Mech' in line:
            parts = line.split(':')[1].strip().split()
            event['strike'] = float(parts[2])
            event['dip'] = float(parts[5])
            event['rake'] = float(parts[8])
            event['htop'] = float(parts[11])
        if is_multi == True and '% SEGMENT # 1:' in line:
            parts = line.split(':')[1].strip().split()
            strike = float(parts[2])
            dip = float(parts[6])
    if is_multi == False:
        strike = event['strike']
        dip = event['dip']

    # Get segment dimensions
    _fspfile.close()
    nx = int(np.round_(length/dx, 2))
    nz = int(np.round_(width/dz, 2))
    # in some versions of numpy, you can't read open text files.
    data = np.genfromtxt(fspfile,max_rows=nx*nz,skip_header=lc-1).T
    lc += (nx*nz)-1
    _fspfile = open(fspfile,'r')
    for _ in range(lc):
        line = next(_fspfile)

    # Store segment
    segment = {'strike':strike,
       'dip':dip,
       'length': length,
       'width': width}
    for idx, header in enumerate(headers):
        if header.lower() == 'z':
            header = 'depth'
        segment[header.lower()] = data[idx].reshape(nz,nx).copy()
    segments = [segment]

    # Get multiple segments
    if is_multi:
        while True:
            for line in _fspfile.readlines():
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
            _fspfile.close()
            nx = int(np.round_(length/dx, 2))
            nz = int(np.round_(width/dz, 2))

            # Import data
            data = np.genfromtxt(fspfile,max_rows=nx*nz,skip_header=lc-1).T
            lc += (nx*nz)-1

            # Reshape data into the proper dimensions
            _fspfile = open(fspfile,'r')
            for _ in range(lc):
                next(_fspfile)

            # Store segment
            segment = {'strike':strike,
               'dip':dip,
               'length': length,
               'width': width}
            for idx, header in enumerate(headers):
                if header.lower() == 'z':
                    header = 'depth'
                segment[header.lower()] = data[idx].reshape(nz,nx).copy()
            segments.append(segment)

    # close fspfile object when done
    _fspfile.close()
    return event, segments
