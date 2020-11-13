#!/usr/bin/env python

# stdlib imports
import glob
import os
import shutil
import tempfile
import warnings

# third party imports
from lxml import etree
import numpy as np
import pytest

# local imports
from fault.fault import Fault
from product.web_product import WebProduct


def test_fromDirectory():
    # test 10004u1y_1
    print('Testing basic model...')
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
    product = WebProduct.fromDirectory(directory, '10004u1y', 1)
    assert '%.1f' % product.properties['derived-magnitude'] == '7.8'
    assert '%.2e' % product.properties['scalar-moment'] == '6.02e+20'
    assert product.properties['model-strike'] == 274
    assert product.properties['model-dip'] == 84
    assert product.properties['model-rake'] == 164
    assert product.properties['number-pwaves'] == 50
    assert product.properties['number-shwaves'] == 17
    assert product.properties['number-longwaves'] == 72
    assert product.properties['maximum-slip'] == 11.8709
    assert product.properties['maximum-rise'] == 8.8
    assert product.properties['model-number'] == 1
    assert product.properties['crustal-model'] == ("1D crustal model "
                                                   "interpolated from CRUST2.0 "
                                                   "(Bassin et al., 2000).")
    with pytest.raises(KeyError) as e_info:
        product.properties['comment']
    assert str(e_info) == "<ExceptionInfo KeyError('comment',) tblen=1>"

    # test 10004u1y_1
    print('Testing comment...')
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
    product = WebProduct.fromDirectory(directory, '10004u1y', 2,
                                       comment="Nodal plane 1.",
                                       crustal_model="another model.")
    assert '%.1f' % product.properties['derived-magnitude'] == '7.8'
    assert '%.2e' % product.properties['scalar-moment'] == '6.02e+20'
    assert product.properties['model-number'] == 2
    assert product.properties['crustal-model'] == "another model."
    assert product.properties['comment'] == "Nodal plane 1."

    # Test default for 70008fi4
    print('Testing suppressing the multisegment number...')
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(homedir, '..', 'data', 'products', '000714t')
    product = WebProduct.fromDirectory(directory, '000714t', 1)
    assert product.properties["average-rise-time"] == "6.93"
    assert product.properties["average-rupture-velocity"] == "2.27"
    assert product.properties["depth"] == 36.0
    assert product.properties["derived-magnitude"] == 8.15
    assert product.properties["derived-magnitude-type"] == "Mw"
    assert product.properties["eventsource"] == "us"
    assert product.properties["eventsourcecode"] == "000714t"
    assert product.properties["eventtime"] == "1995-07-30T00:00:00.000000Z"
    assert product.properties["hypocenter-x"] == 172.5
    assert product.properties["hypocenter-z"] == 15.0
    assert product.properties["latitude"] == -23.36
    assert product.properties["location"] == "-23.3600, -70.3100"
    assert product.properties["longitude"] == -70.31
    assert product.properties["maximum-frequency"] == 1.0
    assert product.properties["maximum-rise"] == 14.4
    assert product.properties["maximum-slip"] == 5.3734
    assert product.properties["minimum-frequency"] == 0.002
    assert product.properties["model-dip"] == 22.0
    assert product.properties["model-length"] == 225.0
    assert product.properties["model-rake"] == 87.0
    assert product.properties["model-strike"] == 6.0
    assert product.properties["model-top"] == 11.51
    assert product.properties["model-width"] == 70.0
    assert product.properties["number-longwaves"] == 22
    assert product.properties["number-pwaves"] == 14
    assert product.properties["number-shwaves"] == 3
    assert product.properties["scalar-moment"] == 2.1948157e+21
    assert product.properties["segment-1-dip"] == 22.0
    assert product.properties["segment-1-strike"] == 6.0
    assert product.properties["segment-2-dip"] == 18.0
    assert product.properties["segment-2-strike"] == 6.0
    assert product.properties["segments"] == 2
    np.testing.assert_almost_equal(
        product.properties["subfault-1-area"], 6868.218733977082, decimal=5)
    np.testing.assert_almost_equal(
        product.properties["subfault-1-length"], 138.18999403455956, decimal=5)
    np.testing.assert_almost_equal(
        product.properties["subfault-1-width"], 49.701273829271805, decimal=5)
    np.testing.assert_almost_equal(
        product.properties["subfault-2-area"], 3996.269894642578, decimal=5)
    np.testing.assert_almost_equal(
        product.properties["subfault-2-length"], 113.8298717959322, decimal=5)
    np.testing.assert_almost_equal(
        product.properties["subfault-2-width"], 35.107391685434436, decimal=5)
    assert product.properties["time-windows"] == 8
    assert product.properties["velocity-function"] == "Asymetriccosine"
    assert product.properties["velocity-function"] == "Asymetriccosine"
    assert product.properties['crustal-model'] == ("1D crustal model "
                                                   "interpolated from CRUST2.0 "
                                                   "(Bassin et al., 2000).")
    with pytest.raises(KeyError) as e_info:
        product.properties['comment']
    assert str(e_info) == "<ExceptionInfo KeyError('comment',) tblen=1>"

    # test suppress model number
    print('Testing suppressing the model number...')
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
    product = WebProduct.fromDirectory(directory, '10004u1y', 1,
                                       suppress_model=True)
    with pytest.raises(KeyError) as e_info:
        product.properties['model-number']
    assert str(e_info) == "<ExceptionInfo KeyError('model-number',) tblen=1>"


def test_exceptions():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'products', '000714t')
    product = WebProduct.fromDirectory(ts_directory, '000714t', 1)
    product.writeContents(ts_directory)

    os.remove(ts_directory + '/FFM.geojson')
    try:
        product.writeContents(ts_directory)
        success = True
    except FileNotFoundError:
        success = False
    assert success == False
    product.writeGrid(ts_directory)


if __name__ == '__main__':
    test_exceptions()
    test_fromDirectory()
