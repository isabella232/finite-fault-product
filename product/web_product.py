#!/usr/bin/env

# stdlib imports
from collections import OrderedDict
import glob
import json
import os
import warnings

# third party imports
from lxml import etree
import numpy as np

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
        self._real_paths = {}
        contents = etree.Element('contents')
        # Look for  and add basemap
        basemap = self._checkDownload(directory, "*_basemap.png")
        if len(basemap) > 0:
            self._real_paths['basemap'] = (basemap[0], "basemap.png")
            file_attrib, format_attrib = self._getAttributes('basemap',
                    "Base Map ", "basemap.png", "image/png")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Map of finite fault showing it's geographic context ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # Look for body and surace wave plots
        plots = self._checkDownload(directory, "waveplots.zip")
        if len(plots) > 0:
            self._real_paths['waveplots'] = (plots[0], "waveplots.zip")
            file_attrib, format_attrib = self._getAttributes('waveplots',
                    "Wave Plots ", "waveplots.zip", "application/zip")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Body and surface wave plots ")
            etree.SubElement(file_tree, 'format', format_attrib)

        # CMT solution
        cmt = self._checkDownload(directory, "*CMTSOLUTION*")
        if len(cmt) > 0:
            self._real_paths['cmtsolution'] = (cmt[0], "CMTSOLUTION")
            file_attrib, format_attrib = self._getAttributes('cmtsolution',
                    "CMT Solution ", "CMTSOLUTION", "text/plain")
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
                self._real_paths['inpfile1'] = (param[0], "basic_inversion.param")
                file_attrib, format_attrib = self._getAttributes('inpfiles',
                        "Inversion Parameters ", "basic_inversion.param", "text/plain")
                file_tree = etree.SubElement(contents, 'file', file_attrib)
                caption = etree.SubElement(file_tree, 'caption')
                caption.text = etree.CDATA(
                        "Files of inversion parameters for the finite fault ")
                etree.SubElement(file_tree, 'format', format_attrib)
                self._real_paths['inpfile2'] = (fsp[0], "complete_inversion.fsp")
                file_attrib, format_attrib = self._getAttributes(
                        'inpfiles', "Inversion Parameters ",
                        "complete_inversion.fsp", "text/plain")
                etree.SubElement(file_tree, 'format', format_attrib)
            else:
                self._real_paths['inpfile2'] = (fsp[0], "complete_inversion.fsp")
                file_attrib, format_attrib = self._getAttributes(
                        'inpfiles', "Inversion Parameters ",
                        "complete_inversion.fsp", "text/plain")
                file_tree = etree.SubElement(contents, 'file', file_attrib)
                caption = etree.SubElement(file_tree, 'caption')
                caption.text = etree.CDATA(
                        "Files of inversion parameters for the finite fault ")
                etree.SubElement(file_tree, 'format', format_attrib)

        # Coulomb inp
        coul = self._checkDownload(directory, "*_coulomb.inp")
        if len(coul) > 0:
            self._real_paths['coulomb'] = (coul[0], "coulomb.inp")
            file_attrib, format_attrib = self._getAttributes('coulomb',
                    "Coulomb Input File ", "coulomb.inp", "text/plain")
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
            self._real_paths['momentrate1'] = (mr_ascii[0], "moment_rate.mr")
            file_attrib, format_attrib = self._getAttributes(
                    'momentrate', "Moment Rate Function Files ",
                    "moment_rate.mr", "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                    "Files of time vs. moment rate for source time "
                    "functions ")
            etree.SubElement(file_tree, 'format', format_attrib)
            self._real_paths['momentrate2'] = (mr_plot[0], "moment_rate.png")
            file_attrib, format_attrib = self._getAttributes('momentrate',
                    "Moment Rate Function Files ", "moment_rate.png",
                    "image/png")
            etree.SubElement(file_tree, 'format', format_attrib)
        else:
            self._real_paths['momentrate2'] = (mr_plot[0], "moment_rate.png")
            file_attrib, format_attrib = self._getAttributes('momentrate',
                    "Moment Rate Function Files ", "moment_rate.png",
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
            self._real_paths['deformation'] = (surf[0], "surface_deformation.disp")
            file_attrib, format_attrib = self._getAttributes('surface',
                    "Surface Deformation File ",
                    "surface_deformation.disp", "text/plain")
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
                "FFM GeoJSON ", 'FFM.geojson', "text/plain")
        grid_file = etree.SubElement(contents, 'file',
                file_attrib)
        grid_caption = etree.SubElement(grid_file, 'caption')
        caption_str = ("GeoJSON file of the finite fault model grid ")
        grid_caption.text = etree.CDATA(caption_str)
        etree.SubElement(grid_file, 'format', format_attrib)

        # Comment JSON
        if not os.path.exists(os.path.join(directory, 'analysis.html')):
            raise FileNotFoundError('Missing analysis html file.')
        file_attrib, format_attrib = self._getAttributes('analysis',
                "Analysis HTML ", 'analysis.html', "text/plain")
        analysis_file = etree.SubElement(contents, 'file', file_attrib)
        analysis_caption = etree.SubElement(analysis_file, 'caption')
        caption_str = ("Analysis of results ")
        analysis_caption.text = etree.CDATA(caption_str)
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
    def fromDirectory(cls, directory, eventid):
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
        file_strs = [f[0] + ': ' + f[1] for f in files]
        if unavailable is True:
            raise Exception('Missing required files %r' % file_strs)
        with open(directory + '/analysis.txt', 'r') as f:
                analysis = "".join(f.readlines())
        product.writeAnalysis(analysis, directory)
        fsp_file = glob.glob(directory + "/" + "*.fsp")[0]
        fault = Fault.fromFiles(fsp_file, directory)
        product.event = fault.event
        product.segments = fault.segments
        fault.createGeoJSON()
        product.grid = fault.corners
        product.writeGrid(directory)
        product.writeContents(directory)
        product.storeProperties(directory, eventid)
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

    def storeProperties(self, directory, eventid):
        """
        Store PDL properties.

        Args:
            directory (string): Path to directory.
            eventid (string): Eventid used for file naming.
        """
        props = {}
        props['eventsourcecode'] = eventid
        props['eventsource'] = 'us'
        wave_file = os.path.join(directory, 'Readlp.das')
        props['num_pwaves'], props['num_shwaves'] = self._countWaveforms(
                wave_file)
        try:
            with open(os.path.join(directory, 'synm.str_low'), 'rt') as f:
                number_low = int(f.readline().strip())
        except:
            number_low = 0
        props['num_longwaves'] = number_low
        props['latitude'] = self.event['lat']
        props['longitude'] = self.event['lon']
        props['location'] = self.event['location']
        props['magnitude'] = self.event['mag']
        props['moment'] = self.event['moment']
        props['moment_units'] = 'Nm'
        props['depth'] = self.event['depth']
        props['date'] = self.event['date']
        props['num_segments'] = len(self.segments)
        props['slip_units'] = 'm'
        props['rake_units'] = 'deg'
        props['rise_units'] = 's'
        props['trup_units'] = 's'
        counter = 1
        max_vals = {}
        for segment in self.segments:
            idx = str(counter) + str(len(self.segments))
            props['strike' + idx] = segment['strike']
            props['strike' + idx + '_units'] = 'deg'
            props['dip' + idx] = segment['dip']
            props['dip' + idx + '_units'] = 'deg'
            props['width' + idx] = segment['width']
            props['width' + idx + '_units'] = 'km'
            props['length' + idx] = segment['length']
            props['length' + idx + '_units'] = 'km'
            props['area' + idx] = segment['length'] * segment['length']
            props['area' + idx + '_units'] = 'km*km'
            props['depth' + idx + '_units'] = 'km'
            counter += 1
            for key in segment.keys():
                key = key.lower()
                if (key != 'lat' and key != 'lon' and key != 'x==ew' and
                    key != 'y==ns' and key != 'z' and key != 'strike' and
                    key != 'dip' and key != 'length' and key != 'width'):
                    if key not in max_vals:
                        max_vals[key] = []
                    values = segment[key].flatten()
                    max_vals[key] += [values[np.argmax(values)]]
        for key in max_vals:
            props['max_' + key] = max_vals[key][np.argmax(max_vals[key])]
        self._pdl_properties = props

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
            'Slip PNG': '*slip*.png',
            'FSP File': '*.fsp',
            'Low File': 'synm.str_low',
            'Wave File': 'Readlp.das',
            'Analysis Text File': 'analysis.txt'
        }
        unavailable = []
        for file_type in required:
            path = os.path.join(directory, required[file_type])
            if len(glob.glob(path)) < 1:
                unavailable += [(file_type, required[file_type] )]
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
            file_path = os.path.join(os.path.basename(file_paths[0]))
            files += [file_path]
        return files

    def _countWaveforms(self, filename):
        """
        Count the number of wave forms.

        Args:
            filename (str): Path to wave file.
        """
        with open(filename,'rt') as f:
            lines = f.readlines()
        num_lines = int(lines[4].strip())
        ns = 0
        np = 0
        #read the int value of the 8th column of each line.
        # if greater than 2, increment ns, otherwise increment np
        for i in range(5, num_lines):
            parts = lines[i].split()
            if float(parts[8]) > 2:
                ns += 1
            else:
                np += 1
        return (np,ns)

    def _getAttributes(self, id, title, href, type):
        """
        Created contents attributes.

        Args:
            file_patterns (string): File patterns to check.
        """
        file_attrib = {'id': id, 'title': title}
        format_attrib = {'href': href, 'type': type}
        return file_attrib, format_attrib
