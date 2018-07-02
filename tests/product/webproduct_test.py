#!/usr/bin/env python

#stdlib imports
import os
import glob

# local imports
from fault.fault import Fault
from product.web_product import WebProduct
import shutil
import tempfile


def test_from_fault():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'timeseries')
    fspfile = os.path.join(homedir, '..', 'data', 'fsp', '1000dyad.fsp')
    fault = Fault.from_files(fspfile, ts_directory)
    webproduct = WebProduct.from_fault(fault)
    assert isinstance(webproduct.event, dict)
    assert isinstance(webproduct.segments, list)
    assert isinstance(webproduct.timeseries_dict, dict)
    tmp = tempfile.mkstemp()[1]
    webproduct.write_timeseries(tmp)
    os.remove(tmp)
    try:
        webproduct = WebProduct.from_fault('')
        success = True
    except Exception:
        success = False
    assert success == False
    try:
        webproduct = WebProduct()
        webproduct.write_timeseries('test.txt')
        success = True
    except Exception:
        success = False
    assert success == False


if __name__ == '__main__':
    test_from_fault()
