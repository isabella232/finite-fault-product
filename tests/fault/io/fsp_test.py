#!/usr/bin/env python

#stdlib imports
import os
import glob

# local imports
from fault.io.fsp import read_from_file


def test_fsp():
    homedir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(homedir, '..', '..', 'data', 'fsp')
    fsp_locations = []
    for file_path in glob.glob(input_directory + '/*.fsp'):
            fsp_locations += [file_path]
    for fspfile in fsp_locations:
        read_from_file(fspfile)

if __name__ == '__main__':
    test_fsp()
