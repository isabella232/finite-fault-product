#!/usr/bin/env python

#stdlib imports
import os

# third party imports
import pandas as pd
import numpy as np


# local imports
from fault.io.timeseries import read_from_directory


def test_timeseries():
    homedir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(homedir, '..', '..', 'data', 'timeseries')
    read_from_directory(input_directory)
    try:
        read_from_directory('INVALID')
        success = True
    except:
        success = False
    assert success == False


if __name__ == '__main__':
    test_timeseries()
