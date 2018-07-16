#!/usr/bin/env python

#stdlib imports
import glob
import os
import shutil
import tempfile

# third party imports
from lxml import etree

# local imports
from fault.fault import Fault
from product.web_product import WebProduct


def test_fromFault():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'timeseries')
    fspfile = os.path.join(homedir, '..', 'data', 'timeseries', '1000dyad.fsp')
    product = WebProduct.fromDirectory(ts_directory, '1000dyad')
    product.createContents(ts_directory)
    xml = """<contents>
	<file id="basemap" title="Base Map ">
	<caption>
	<![CDATA[ Map of finite fault showing it's geographic context ]]>
	</caption>
	<format href="web/1000dyad_basemap.png" type="image/png"/>
	</file>
	<file id="cmtsolution1" title="CMT Solution ">
	<caption>
	<![CDATA[ Full CMT solution for every point in finite fault region ]]>
	</caption>
	<format href="web/CMTSOLUTION" type="text/plain"/>
	</file>
	<file id="inpfile1_1" title="Inversion Parameters File 1 ">
	<caption>
	<![CDATA[ Basic inversion parameters for each node in the finite fault ]]>
	</caption>
	<format href="web/1000dyad.param" type="text/plain"/>
	</file>
	<file id="inpfile2_1" title="Inversion Parameters File 2 ">
    <caption>
	<![CDATA[ Complete inversion parameters for the finite fault, following the SRCMOD FSP format (http://equake-rc.info/) ]]>
    </caption>
    <format href="web/1000dyad.fsp" type="text/plain"/>
	</file>
	<file id="coulomb_1" title="Coulomb Input File ">
	<caption>
	<![CDATA[ Format necessary for compatibility with Coulomb3 (http://earthquake.usgs.gov/research/software/coulomb/) ]]>
	</caption>
	<format href="web/1000dyad_coulomb.inp" type="text/plain"/>
	</file>
	<file id="momentrate1" title="Moment Rate Function File ">
    <caption>
	<![CDATA[ Ascii file of time vs. moment rate, used for plotting source time function ]]>
    </caption>
    <format href="web/1000dyad.mr" type="text/plain"/>
	</file>
	<file id="surface1" title="Surface Deformation File ">
	<caption>
	<![CDATA[ Surface displacement resulting from finite fault, calculated using Okada-style deformation codes ]]>
	</caption>
	<format href="web/1000dyad.disp" type="text/plain"/>
	</file>
    </contents>"""
    tree = product.contents
    geojson = tree.xpath("//file[@id='geojson']")[0]
    geojson.getparent().remove(geojson)
    timeseries = tree.xpath("//file[@id='timeseries']")[0]
    timeseries.getparent().remove(timeseries)
    comments = tree.xpath("//file[@id='comments']")[0]
    comments.getparent().remove(comments)
    tree = etree.tostring(tree).decode()
    tree = tree.strip().replace('\n', '').replace('\t', '').replace(' ', '')
    target_xml = xml.strip().replace('\n', '').replace('\t', '').replace(' ', '')
    assert tree == target_xml

def test_exceptions():
    homedir = os.path.dirname(os.path.abspath(__file__))
    ts_directory = os.path.join(homedir, '..', 'data', 'timeseries')
    fspfile = os.path.join(homedir, '..', 'data', 'timeseries', '1000dyad.fsp')
    product = WebProduct.fromDirectory(ts_directory, '1000dyad')
    product.writeContents(ts_directory)
    
    os.remove(ts_directory + '/comments.json')
    try:
        product.createContents(ts_directory)
        success = True
    except FileNotFoundError:
        success = False
    assert success == False
    product.writeComments(ts_directory)

    os.remove(ts_directory + '/timeseries.json')
    try:
        product.createContents(ts_directory)
        success = True
    except FileNotFoundError:
        success = False
    assert success == False
    product.writeTimeseries(ts_directory)

    os.remove(ts_directory + '/FFM.geojson')
    try:
        product.createContents(ts_directory)
        success = True
    except FileNotFoundError:
        success = False
    assert success == False
    product.writeGrid(ts_directory)

if __name__ == '__main__':
    test_fromFault()
    test_exceptions()
