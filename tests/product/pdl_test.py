#!/usr/bin/env python

#stdlib imports
import glob
import os
import shutil
import tempfile
import warnings

# third party imports
from lxml import etree
import numpy as np

# local imports
from product.pdl import get_fault


def test_get():
    get_fault('us', '1000dyad', comcat_host='dev01-earthquake.cr.usgs.gov',
            two_model=False, write_directory=None)

    tmp = tempfile.mkdtemp()
    get_fault('us', '1000dyad', comcat_host='dev01-earthquake.cr.usgs.gov',
            two_model=False, write_directory=tmp)

    get_fault('us', '10004u1y', comcat_host='dev01-earthquake.cr.usgs.gov',
            two_model=True, write_directory=tmp)

    shutil.rmtree(tmp)

if __name__ == '__main__':
    test_get()
