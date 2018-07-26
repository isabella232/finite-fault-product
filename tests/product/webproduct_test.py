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
from fault.fault import Fault
from product.web_product import WebProduct


def test_fromFault():
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        product = WebProduct.fromDirectory(directory, '10004u1y_1')
    product.writeContents(directory)
    assert '%.1f' % product.properties['magnitude'] == '7.8'
    assert '%.2e' % product.properties['moment'] == '6.02e+27'
    assert product.properties['mechanism_strike'] == 274
    assert product.properties['mechanism_dip'] == 84
    assert product.properties['mechanism_rake'] == 164
    assert product.properties['num_pwaves'] == 50
    assert product.properties['num_shwaves'] == 17
    assert product.properties['num_longwaves'] == 72


def test_exceptions():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'products', '000714t')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        product = WebProduct.fromDirectory(ts_directory, '000714t')
    product.writeContents(ts_directory)
    product.createTimeseriesGeoJSON()
    product.writeTimeseries(ts_directory)


    os.remove(ts_directory + '/FFM.geojson')
    try:
        product.writeContents(ts_directory)
        success = True
    except FileNotFoundError:
        success = False
    assert success == False
    product.writeGrid(ts_directory)


if __name__ == '__main__':
    test_fromFault()
    test_exceptions()
