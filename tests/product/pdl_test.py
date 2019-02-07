#!/usr/bin/env python

#stdlib imports
import glob
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


def test_get_one():
    homedir = os.path.dirname(os.path.abspath(__file__))

    get_fault('us', '1000dyad', comcat_host='dev01-earthquake.cr.usgs.gov',
            two_model=False, write_directory=None)

    cassette1 = os.path.join(homedir, 'get_onefault_cassette.yaml')
    tmp = tempfile.mkdtemp()

    with vcr.use_cassette(cassette1):
        get_fault('us', '1000dyad', comcat_host='dev01-earthquake.cr.usgs.gov',
                    two_model=False, write_directory=tmp)
    shutil.rmtree(tmp)

def test_get_two():
    homedir = os.path.dirname(os.path.abspath(__file__))
    tmp = tempfile.mkdtemp()
    cassette2 = os.path.join(homedir, 'get_twofault_cassette.yaml')
    with vcr.use_cassette(cassette2):
        get_fault('us', '10004u1y', comcat_host='dev01-earthquake.cr.usgs.gov',
                    two_model=True, write_directory=tmp)
    shutil.rmtree(tmp)

if __name__ == '__main__':
    test_get_one()
    test_get_two()
