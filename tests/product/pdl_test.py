#!/usr/bin/env python

# stdlib imports
import glob
import json
import os
import shutil
import tempfile
import vcr
import warnings

# third party imports
from lxml import etree
import numpy as np

# local imports
from product.pdl import get_fault

TARGET_1000dyad = {
    "average-rise-time": "2.13",
    "average-rupture-velocity": "1.2",
    "crustal-model": "1D crustal model interpolated from CRUST2.0 (Bassin et al., 2000).",
    "depth": 8.0,
    "derived-magnitude": 6.88,
    "derived-magnitude-type": "Mw",
    "eventsource": "us",
    "eventsourcecode": "1000dyad",
    "eventtime": "2018-05-04T00:00:00.000000Z",
    "hypocenter-x": 54.0,
    "hypocenter-z": 11.25,
    "latitude": 19.37,
    "location": "19km SSW of Leilani Estates, Hawaii",
    "longitude": -155.03,
    "maximum-frequency": 1.0,
    "maximum-rise": 4.0,
    "maximum-slip": 2.686,
    "minimum-frequency": 0.002,
    "model-dip": 20.0,
    "model-length": 108.0,
    "model-rake": 114.0,
    "model-strike": 240.0,
    "model-top": 4.15,
    "model-width": 25.0,
    "number-longwaves": 75,
    "number-pwaves": 42,
    "number-shwaves": 28,
    "scalar-moment": 2.7660745e+19,
    "segment-1-dip": 20.0,
    "segment-1-strike": 240.0,
    "segments": 1,
    "subfault-1-area": 843.8598782352279,
    "subfault-1-length": 64.5265136154769,
    "subfault-1-width": 13.077723108735032,
    "time-windows": 5,
    "velocity-function": "Asymetriccosine"
}

TARGET_10004u1y_1 = {
    "average-rise-time": "3.83",
    "average-rupture-velocity": "1.29",
    "crustal-model": "1D crustal model interpolated from CRUST2.0 (Bassin et al., 2000).",
    "depth": 24.0,
    "derived-magnitude": 7.77,
    "derived-magnitude-type": "Mw",
    "eventsource": "us",
    "eventsourcecode": "10004u1y",
    "eventtime": "2016-03-02T00:00:00.000000Z",
    "hypocenter-x": 125.0,
    "hypocenter-z": 22.5,
    "latitude": -4.905,
    "location": "Southwest of Sumatra, Indonesia",
    "longitude": 94.236,
    "maximum-frequency": 1.0,
    "maximum-rise": 8.8,
    "maximum-slip": 11.8709,
    "minimum-frequency": 0.002,
    "model-dip": 84.0,
    "model-length": 250.0,
    "model-rake": 164.0,
    "model-strike": 274.0,
    "model-top": 1.62,
    "model-width": 45.0,
    "number-longwaves": 72,
    "number-pwaves": 50,
    "number-shwaves": 17,
    "scalar-moment": 6.0159401e+20,
    "segment-1-dip": 84.0,
    "segment-1-strike": 274.0,
    "segments": 1,
    "subfault-1-area": 1621.830894196068,
    "subfault-1-length": 63.616710166585996,
    "subfault-1-width": 25.49378755910452,
    "time-windows": 8,
    "velocity-function": "Asymetriccosine"
}

TARGET_10004u1y_2 = {
    "average-rise-time": "4.26",
    "average-rupture-velocity": "1.3",
    "crustal-model": "1D crustal model interpolated from CRUST2.0 (Bassin et al., 2000).",
    "depth": 23.0,
    "derived-magnitude": 7.77,
    "derived-magnitude-type": "Mw",
    "eventsource": "us",
    "eventsourcecode": "10004u1y",
    "eventtime": "2016-03-02T00:00:00.000000Z",
    "hypocenter-x": 125.0,
    "hypocenter-z": 22.5,
    "latitude": -4.905,
    "location": "Southwest of Sumatra, Indonesia",
    "longitude": 94.236,
    "maximum-frequency": 1.0,
    "maximum-rise": 8.8,
    "maximum-slip": 18.8876,
    "minimum-frequency": 0.002,
    "model-dip": 79.0,
    "model-length": 250.0,
    "model-number": 2,
    "model-rake": 6.0,
    "model-strike": 5.0,
    "model-top": 0.91,
    "model-width": 45.0,
    "number-longwaves": 72,
    "number-pwaves": 50,
    "number-shwaves": 17,
    "scalar-moment": 6.0034719e+20,
    "segment-1-dip": 79.0,
    "segment-1-strike": 5.0,
    "segments": 1,
    "subfault-1-area": 1237.7901834426573,
    "subfault-1-length": 87.32899713172054,
    "subfault-1-width": 14.173873788744729,
    "time-windows": 8,
    "velocity-function": "Asymetriccosine"
}


def _compare(data, target):
    for key in target:
        assert key in data
        assert data[key] == target[key]


def test_get_one():
    homedir = os.path.dirname(os.path.abspath(__file__))
    cassette1 = os.path.join(homedir, 'get_onefault_cassette_nowrite.yaml')
    with vcr.use_cassette(cassette1):
        get_fault('us', '1000dyad', comcat_host='dev02-earthquake.cr.usgs.gov',
                  write_directory=None)

    cassette2 = os.path.join(homedir, 'get_onefault_cassette.yaml')
    tmp = tempfile.mkdtemp()

    with vcr.use_cassette(cassette2):
        get_fault('us', '1000dyad',
                  comcat_host='dev02-earthquake.cr.usgs.gov',
                  write_directory=tmp)
        folderstr = glob.glob(os.path.join(tmp, 'us1000dyad*'))[0]
        filestr = glob.glob(os.path.join(folderstr, 'properties.json'))[0]
        with open(filestr, 'r') as f:
            data_dict = json.load(f)
        _compare(data_dict, TARGET_1000dyad)

        shutil.rmtree(tmp)


def test_get_two():
    homedir = os.path.dirname(os.path.abspath(__file__))
    cassette3 = os.path.join(homedir, 'get_twofault_cassette_1.yaml')
    cassette4 = os.path.join(homedir, 'get_twofault_cassette_2.yaml')

    with vcr.use_cassette(cassette3):
        tmp1 = tempfile.mkdtemp()
        get_fault('us', '10004u1y', comcat_host='dev02-earthquake.cr.usgs.gov',
                  model=1, write_directory=tmp1)
        folderstr = glob.glob(os.path.join(tmp1, 'us10004u1y_1*'))[0]
        filestr = glob.glob(os.path.join(folderstr, 'properties.json'))[0]
        with open(filestr, 'r') as f:
            data_dict1 = json.load(f)
        _compare(data_dict1, TARGET_10004u1y_1)
        shutil.rmtree(tmp1)

    with vcr.use_cassette(cassette4):
        tmp2 = tempfile.mkdtemp()
        get_fault('us', '10004u1y', comcat_host='dev02-earthquake.cr.usgs.gov',
                  model=2, write_directory=tmp2)
        folderstr = glob.glob(os.path.join(tmp2, 'us10004u1y_2*'))[0]
        filestr = glob.glob(os.path.join(folderstr, 'properties.json'))[0]
        with open(filestr, 'r') as f:
            data_dict2 = json.load(f)
        _compare(data_dict2, TARGET_10004u1y_2)
        shutil.rmtree(tmp2)


if __name__ == '__main__':
    test_get_one()
    test_get_two()
