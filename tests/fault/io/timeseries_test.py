#!/usr/bin/env python

#stdlib imports
import glob
import os
import shutil
import tempfile

# third party imports
import pandas as pd
import numpy as np


# local imports
from fault.io.timeseries import directory2JSON


def test_timeseries():
    homedir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(homedir, '..', '..', 'data', 'timeseries')
    tmp = tempfile.mkstemp()[1]
    directory2JSON(input_directory, tmp)
    os.remove(tmp)
    

if __name__ == '__main__':
    test_timeseries()
