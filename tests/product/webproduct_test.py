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

# local imports
from fault.fault import Fault
from product.web_product import WebProduct


def test_fromFault():
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        product = WebProduct.fromDirectory(
            directory, '10004u1y', multiple=True)
    product.writeContents(directory)
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

    target_contents_str = """
    <contents>
      <file id="modelmaps" title="Finite Fault Model Maps ">
        <caption><![CDATA[Map representation of the finite fault model ]]></caption>
        <format href="FFM.geojson" type="text/plain"/>
        <format href="finite_fault.kml" type="application/vnd.google-earth.kml+xml"/>
        <format href="finite_fault.kmz" type="application/vnd.google-earth.kmz"/>
        <format href="basemap.png" type="image/png"/>
      </file>
      <file id="waveplots" title="Wave Plots ">
        <caption><![CDATA[Body and surface wave plots ]]></caption>
        <format href="waveplots.zip" type="application/zip"/>
      </file>
      <file id="inpfiles" title="Inversion Parameters ">
        <caption><![CDATA[Files of inversion parameters for the finite fault ]]></caption>
        <format href="basic_inversion.param" type="text/plain"/>
        <format href="complete_inversion.fsp" type="text/plain"/>
      </file>
      <file id="coulomb" title="Coulomb Input File ">
        <caption><![CDATA[Format necessary for compatibility with Coulomb3 (http://earthquake.usgs.gov/research/software/coulomb/) ]]></caption>
        <format href="coulomb.inp" type="text/plain"/>
      </file>
      <file id="momentrate" title="Moment Rate Function Files ">
        <caption><![CDATA[Files of time vs. moment rate for source time functions ]]></caption>
        <format href="moment_rate.mr" type="text/plain"/>
        <format href="moment_rate.png" type="image/png"/>
      </file>
    </contents>"""
    directory = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        product = WebProduct.fromDirectory(directory, '1000dyad')
    product.writeContents(directory)
    assert product.properties['maximum-slip'] == 2.6860
    assert product.properties['maximum-rise'] == 4.0000

    target_contents = etree.fromstring(target_contents_str)
    contents = etree.parse(os.path.join(directory, 'contents.xml'))
    target_contents = etree.tostring(
        target_contents).decode().strip().replace(' ', '')
    contents = etree.tostring(contents).decode().strip().replace(' ', '')
    assert contents == target_contents

    directory = os.path.join(homedir, '..', 'data', 'timeseries')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        product = WebProduct.fromDirectory(directory, '1000dyad')
    product.createTimeseriesGeoJSON()
    product.writeTimeseries(directory)


def test_fromDirectory():
    homedir = os.path.dirname(os.path.abspath(__file__))
    directory1 = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
    directory2 = os.path.join(homedir, '..', 'data', 'products', '10004u1y_2')
    # Fault 1
    product = WebProduct.fromDirectory(directory1, '10004u1y', multiple=True)
    html1 = os.path.join(directory1, '10004u1y.html')
    with open(html1, 'r') as f1:
        lines1 = f1.readlines()
    join1 = ' '.join(lines1[24:30]).replace(' ', '').replace('\n', '')
    target_str = """The solutions of two nodal planes explain the
    data equally well. Both solutions are presented. Here we
    present results for the nodal plane with strike = 274.0 deg.
    and dip = 84.0 deg. The seismic moment release based upon
    this plane is 6.0e+27 N.m (Mw = 7.8) using a 1D crustal model
    interpolated from CRUST2.0 (Bassin et al., 2000).""".replace(' ', '').replace('\n', '')
    assert join1 == target_str
    # Fault 2
    product = WebProduct.fromDirectory(directory2, '10004u1y', multiple=True)
    html2 = os.path.join(directory2, '10004u1y.html')
    with open(html2, 'r') as f2:
        lines2 = f2.readlines()
    join2 = ' '.join(lines2[24:30]).replace(' ', '').replace('\n', '')
    target_str = """The solutions of two nodal planes explain the
    data equally well. Both solutions are presented. Here we
    present results for the nodal plane with strike = 5.0 deg.
    and dip = 79.0 deg. The seismic moment release based upon
    this plane is 6.0e+27 N.m (Mw = 7.8) using a 1D crustal model
    interpolated from CRUST2.0 (Bassin et al., 2000).""".replace(' ', '').replace('\n', '')
    assert join2 == target_str


def test_exceptions():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'products', '000714t')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        product = WebProduct.fromDirectory(ts_directory, '000714t')
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
    test_fromFault()
    test_exceptions()
    test_fromDirectory()
