#!/usr/bin/env

# stdlib imports
from collections import OrderedDict
import glob
import json
import os
import warnings

# third party imports
from lxml import etree

# local imports
from fault.fault import Fault


class WebProduct(object):
    """Class for creating web products."""
    def __init__(self):
        self._timeseries_dict = None
        self._timeseries_geojson = None
        self._event = None
        self._segments = None
        self._grid = None
        self._contents = None
        self._pdl_information = None

    @property
    def contents(self):
        """
        Helper to return the contents:
        """
        return self._contents

    def createContents(self, directory):
        """
        Create the contents.xml file.

        Args:
            directory (str): Directory path to validate existance of files.

        Returns:
            Element Tree
        """
        contents = etree.Element('contents')
        # Look for  and add basemap
        basemap = self._checkDownload(directory, "*_basemap.png")
        if len(basemap) > 0:
            file_attrib, format_attrib = self._getAttributes('basemap',
                    "Base Map ", basemap[0], "image/png")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Map of finite fault showing it's geographic context ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # Look for body and surace wave plots
        plots = self._checkDownload(directory, "waveplots.zip")
        if len(plots) > 0:
            file_attrib, format_attrib = self._getAttributes('waveplots',
                    "Wave Plots ", plots[0], "application/zip")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Body and surface wave plots ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # CMT solution
        cmt = self._checkDownload(directory, "*CMTSOLUTION*")
        if len(cmt) > 0:
            file_attrib, format_attrib = self._getAttributes('cmtsolution1',
                    "CMT Solution ", cmt[0], "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Full CMT solution for every point in finite fault "
                    "region ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # inversion files
        param = self._checkDownload(directory, "*.param")
        fsp = self._checkDownload(directory, "*.fsp")
        if len(fsp) > 0 or len(param) > 0:
            if len(param) > 0:
                file_attrib, format_attrib = self._getAttributes('inpfiles',
                        "Inversion Parameters ", param[0], "text/plain")
                file_tree = etree.SubElement(contents, 'file', file_attrib)
                caption = etree.SubElement(file_tree, 'caption')
                caption.text = etree.CDATA(
                        "Files of inversion parameters for the finite fault ")
                etree.SubElement(file_tree, 'format', format_attrib)
                if len(fsp) > 0:
                    file_attrib, format_attrib = self._getAttributes(
                            'inpfiles', "Inversion Parameters ", fsp[0],
                            "text/plain")
                    etree.SubElement(file_tree, 'format', format_attrib)
            elif len(fsp) > 0:
                file_attrib, format_attrib = self._getAttributes('inpfiles',
                        "Inversion Parameters ", fsp[0], "text/plain")
                file_tree = etree.SubElement(contents, 'file', file_attrib)
                caption = etree.SubElement(file_tree, 'caption')
                caption.text = etree.CDATA(
                        "Files of inversion parameters for the finite fault ")
                etree.SubElement(file_tree, 'format', format_attrib)
                if len(param) > 0:
                    file_attrib, format_attrib = self._getAttributes(
                            'inpfiles', "Inversion Parameters ", param[0],
                            "text/plain")
                    etree.SubElement(file_tree, 'format', format_attrib)

        # Coulomb inp
        coul = self._checkDownload(directory, "*_coulomb.inp")
        if len(coul) > 0:
            file_attrib, format_attrib = self._getAttributes('coulomb',
                    "Coulomb Input File ", coul[0], "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Format necessary for compatibility with Coulomb3 "
                    "(http://earthquake.usgs.gov/research/software/coulomb/) ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # Moment rate
        mr_plot = self._checkDownload(directory, "*mr*.png")
        mr_ascii = self._checkDownload(directory, "*.mr")
        if len(mr_ascii) > 0:
            file_attrib, format_attrib = self._getAttributes(
                    'momentrate', "Moment Rate Function Files ", mr_ascii[0],
                    "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Files of time vs. moment rate for source time "
                    "functions ")
            etree.SubElement(file_tree, 'format', format_attrib)
            file_attrib, format_attrib = self._getAttributes('momentrate',
                    "Moment Rate Function Files ", mr_plot[0],
                    "image/png")
            etree.SubElement(file_tree, 'format', format_attrib)
        else:
            file_attrib, format_attrib = self._getAttributes('momentrate',
                    "Moment Rate Function Files ", mr_plot[0],
                    "image/png")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Files of time vs. moment rate for source time "
                    "functions ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # surface displacement
        surf = self._checkDownload(directory, "*.disp")
        if len(surf) > 0:
            file_attrib, format_attrib = self._getAttributes('surface',
                    "Surface Deformation File ", surf[0], "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Surface displacement resulting from finite fault, "
                    "calculated using Okada-style deformation codes ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # GeoJSON grid
        if not os.path.exists(os.path.join(directory, 'FFM.geojson')):
            raise FileNotFoundError('Missing FFM geojson file.')
        file_attrib, format_attrib = self._getAttributes('geojson',
                "FFM GeoJSON ", 'web/FFM.geojson', "text/plain")
        grid_file = etree.SubElement(contents, 'file',
                file_attrib)
        grid_caption = etree.SubElement(grid_file, 'caption')
        caption_str = ("GeoJSON file of the finite fault model grid ")
        grid_caption.text = etree.CDATA(caption_str)
        etree.SubElement(grid_file, 'format', format_attrib)

        # Time series JSON
        if not os.path.exists(os.path.join(directory, 'timeseries.geojson')):
            raise FileNotFoundError('Missing timeseries file.')
        file_attrib, format_attrib = self._getAttributes('timeseries',
                "Time Series JSON ", 'web/timeseries.geojson', "text/plain")
        timeseries_file = etree.SubElement(contents, 'file', file_attrib)
        timeseries_caption = etree.SubElement(timeseries_file, 'caption')
        caption_str = "JSON file of time series data and synthetic models "
        timeseries_caption.text = etree.CDATA(caption_str)
        etree.SubElement(timeseries_file, 'format', format_attrib)

        # Comment JSON
        if not os.path.exists(os.path.join(directory, 'analysis.html')):
            raise FileNotFoundError('Missing analysis html file.')
        file_attrib, format_attrib = self._getAttributes('analysis',
                "Analysis HTML ", 'web/analysis.html', "text/plain")
        analysis_file = etree.SubElement(contents, 'file', file_attrib)
        analysis_caption = etree.SubElement(analysis_file, 'caption')
        caption_str = ("Analysis of results ")
        analysis_caption.text = etree.CDATA(caption_str)
        timeseries_format = {'href': 'web/analysis.html',
                'type': "text/plain"}
        etree.SubElement(analysis_file, 'format', format_attrib)

        tree = etree.ElementTree(contents)
        self._contents = tree
        return tree

    def createTimeseriesGeoJSON(self):
        station_points = []
        for key in self.timeseries_dict:
            props = {}
            props['station'] = key
            station = self.timeseries_dict[key]
            props['data'] = station['data']
            props['metadata'] = station['data']

            station_points += [{
              "type": "Feature",
              "properties": props,
              "geometry": {
                "type": "Point",
                "coordinates": []
              }
            }]
        geo = {
          "type": "FeatureCollection",
          "features": station_points
        }
        self._timeseries_geojson = geo

    @property
    def event(self):
        """
        Helper to return event dictionary.

        Returns:
            dictionary: Event information.
        """
        return self._event

    @event.setter
    def event(self, event):
        """
        Helper to set event dictionary.

        event (dictionary): Event information.
        """
        self._event = event

    @property
    def grid(self):
        """
        Helper to return grid dictionary.

        Returns:
            dictionary: Grid information.
        """
        return self._grid

    @grid.setter
    def grid(self, grid):
        """
        Helper to set grid dictionary.

        grid (dictionary): Grid information.
        """
        self._grid = grid

    @classmethod
    def fromDirectory(cls, directory, eventid='', include_downloads=True):
        """
        Create instance based upon a director and eventid.

        Args:
            directory (string): Path to directory.
            eventid (string): Eventid used for file naming. Default is empty
                    string.
            include_downloads (bool): Include the basic download files.
                    Default is True.
        Returns:
            WebProduct: Instance set for information for the web product.
        """
        product = cls()
        unavailable, files = product._files_unavailable(directory)
        if unavailable is True:
            raise Exception('Missing required files: %r' % files)
        with open(directory + '/analysis.txt', 'r') as f:
                analysis = "".join(f.readlines())
        product.writeAnalysis(analysis, directory)
        fsp_file = glob.glob(directory + "/" + "*.fsp")[0]
        fault = Fault.fromFiles(fsp_file, directory)
        product.timeseries_dict = fault.timeseries_dict
        product.createTimeseriesGeoJSON()
        product.writeTimeseries(directory)
        product.event = fault.event
        product.segments = fault.segments
        fault.createGeoJSON()
        product.grid = fault.corners
        product.writeGrid(directory)
        product.writeContents(directory)
        return product

    @property
    def segments(self):
        """
        Helper to return list of segments.

        Returns:
            list: List of segments (dict)
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Helper to set list of segments.

        segments (list): List of segments (dict)
        """
        self._segments = segments

    @property
    def timeseries_dict(self):
        """
        Helper to return time series dictionary.

        Returns:
            dictionary: Dictionary of time series for each station.
        """
        return self._timeseries_dict

    @property
    def timeseries_geojson(self):
        """
        Helper to return time series geojson.

        Returns:
            dictionary: geojson of time series for each station.
        """
        return self._timeseries_geojson

    @timeseries_dict.setter
    def timeseries_dict(self, timeseries_dict):
        """
        Helper to set time series dictionary.

        segmtimeseries_dictents (dictionary): Dictionary of time series for
                each station.
        """
        self._timeseries_dict = timeseries_dict

    def writeAnalysis(self, analysis, directory):
        """
        Write the analysis.html file.

        Args:
            analysis (str): Analysis string.
            directory (str): Path to directory where contents.xml will be
                    written.
        """
        outfile = os.path.join(directory, 'analysis.html')
        if os.path.exists(outfile):
            return
        with open(outfile, 'w') as analysis_file:
            analysis_file.write('<h3>Scientific Analysis</h3>')
            analysis_file.write(analysis)

    def writeContents(self, directory):
        """
        Write the contents.xml file.

        Args:
            directory (str): Path to directory where contents.xml will be
                    written.
        """
        tree = self.createContents(directory)
        outdir = os.path.join(directory, 'contents.xml')
        tree.write(outdir, pretty_print=True, encoding="utf8")

    def writeGrid(self, directory):
        """
        Writes grid in a GeoJSON format.

        Args:
            directory (str): Directory where the file will be written.
        """
        if self.grid is None:
            raise Exception('The FFM grid dictionary has not been set.')
        write_path = os.path.join(directory, 'FFM.geojson')
        with open(write_path, 'w') as outfile:
            json.dump(self.grid, outfile, indent=4)


    def writeTimeseries(self, directory):
        """
        Writes time series in a JSON format.

        Args:
            directory (str): Directory where the file will be written.
        """
        if self.timeseries_geojson is None:
            raise Exception('The time series geojson has not been set.')
        write_path = os.path.join(directory, 'timeseries.geojson')
        with open(write_path, 'w') as outfile:
            json.dump(self.timeseries_dict, outfile, indent=4)

    def _files_unavailable(self, directory):
        """
        Helper to check for required files.

        Args:
            directory (string): Path to directory of FFM data.
        """
        required = {
            'Moment Rate PNG': '*mr*.png',
            'Base Map PNG': '*base*.png',
            'Slip PNG': '*base*.png',
            'FSP Files': '*.fsp',
            'Analysis Text File': 'analysis.txt'
        }
        unavailable = []
        for file_type in required:
            path = os.path.join(directory, required[file_type])
            if len(glob.glob(path)) < 1:
                unavailable += [file_type]
        if len(unavailable) > 0:
            return (True, unavailable)
        else:
            return (False, [])

    def _checkDownload(self, directory, pattern):
        """
        Helper to check for a file and set download dictionary section.

        Args:
            directory (str): Path to directory.
            pattern (string): File patterns to check.
        """
        files = []
        # attempt to find file or use default
        file_paths = glob.glob(os.path.join(directory, pattern))
        if len(file_paths) > 0:
            file_path = os.path.join('web',
                    os.path.basename(file_paths[0]))
            files += [file_path]
        return files

    def _getAttributes(self, id, title, href, type):
        """
        Created contents attributes.

        Args:
            file_patterns (string): File patterns to check.
        """
        file_attrib = {'id': id, 'title': title}
        format_attrib = {'href': href, 'type': type}
        return file_attrib, format_attrib
