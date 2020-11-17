#!/usr/bin/env

# stdlib imports
from collections import OrderedDict
import copy
import datetime
import glob
import json
import os
import shutil
from urllib.request import urlopen
import warnings

# third party imports
from lxml import etree
import numpy as np

# local imports
from fault.fault import Fault
from product.constants import TIMEFMT, DEFAULT_MODEL


class WebProduct(object):
    """Class for creating web products."""

    def __init__(self):
        self._contents = None
        self._event = None
        self._grid = None
        self._paths = None
        self._properties = None
        self._segments = None
        self._timeseries_dict = None
        self._timeseries_geojson = None

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
        if self.paths is None:
            self._paths = {}
        contents = etree.Element('contents')

        # Look for  and add basemaps
        if not os.path.exists(os.path.join(directory, 'FFM.geojson')):
            raise FileNotFoundError('Missing FFM geojson file.')
        file_attrib, format_attrib = self._getAttributes('modelmaps',
                                                         "Finite Fault Model Maps ", 'FFM.geojson', "text/plain")
        maps = etree.SubElement(contents, 'file',
                                file_attrib)
        grid_caption = etree.SubElement(maps, 'caption')
        caption_str = ("Map representation of the finite fault model ")
        grid_caption.text = etree.CDATA(caption_str)
        etree.SubElement(maps, 'format', format_attrib)

        basemap = self._checkDownload(directory, "*base*.png")
        kmls = self._checkDownload(directory, "*.kml")
        kmzs = self._checkDownload(directory, "*.kmz")
        if len(kmls) > 0:
            self._paths['kmls'] = (kmls[0], "finite_fault.kml")
            file_attrib, format_attrib = self._getAttributes('', '',
                                                             "finite_fault.kml", "application/vnd.google-earth.kml+xml")
            etree.SubElement(maps, 'format', format_attrib)
        if len(kmzs) > 0:
            self._paths['kmzs'] = (kmzs[0], "finite_fault.kmz")
            file_attrib, format_attrib = self._getAttributes('', '',
                                                             "finite_fault.kmz", "application/vnd.google-earth.kmz")
            etree.SubElement(maps, 'format', format_attrib)
        if len(basemap) > 0:
            self._paths['basemap'] = (basemap[0], "basemap.png")
            file_attrib, format_attrib = self._getAttributes('basemap',
                                                             "Base Map ", "basemap.png", "image/png")
            etree.SubElement(maps, 'format', format_attrib)

        # look for shakemap rupture polygon
        polygon = self._checkDownload(directory, "shakemap_polygon.txt")
        if len(polygon) > 0:
            self._paths['shakemap_polygon'] = (polygon[0],
                                               "shakemap_polygon.txt")
            file_attrib, format_attrib = self._getAttributes('shakemap_polygon',
                                                             "ShakeMap Rupture Polygon",
                                                             "basemap.png", "text/plain")
            etree.SubElement(maps, 'format', format_attrib)

        # Look for body and surface wave plots
        plots = self._checkDownload(directory, "waveplots.zip")
        if len(plots) > 0:
            self._paths['waveplots'] = (plots[0], "waveplots.zip")
            file_attrib, format_attrib = self._getAttributes('waveplots',
                                                             "Wave Plots ", "waveplots.zip", "application/zip")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                "Body and surface wave plots ")
            etree.SubElement(file_tree, 'format', format_attrib)
        else:
            zipped = self.zip_waveplots(directory)
            if zipped != '':
                self._paths['waveplots'] = (zipped, "waveplots.zip")
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
            self._paths['cmtsolution'] = (cmt[0], "CMTSOLUTION")
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
                self._paths['inpfile1'] = (param[0], "basic_inversion.param")
                file_attrib, format_attrib = self._getAttributes('inpfiles',
                                                                 "Inversion Parameters ", "basic_inversion.param", "text/plain")
                file_tree = etree.SubElement(contents, 'file', file_attrib)
                caption = etree.SubElement(file_tree, 'caption')
                caption.text = etree.CDATA(
                    "Files of inversion parameters for the finite fault ")
                etree.SubElement(file_tree, 'format', format_attrib)
                self._paths['inpfile2'] = (fsp[0], "complete_inversion.fsp")
                file_attrib, format_attrib = self._getAttributes(
                    'inpfiles', "Inversion Parameters ",
                    "complete_inversion.fsp", "text/plain")
                etree.SubElement(file_tree, 'format', format_attrib)
            else:
                self._paths['inpfile2'] = (fsp[0], "complete_inversion.fsp")
                file_attrib, format_attrib = self._getAttributes(
                    'inpfiles', "Inversion Parameters ",
                    "complete_inversion.fsp", "text/plain")
                file_tree = etree.SubElement(contents, 'file', file_attrib)
                caption = etree.SubElement(file_tree, 'caption')
                caption.text = etree.CDATA(
                    "Files of inversion parameters for the finite fault ")
                etree.SubElement(file_tree, 'format', format_attrib)

        # Coulomb inp
        coul = self._checkDownload(directory, "*coulomb.inp")
        if len(coul) > 0:
            self._paths['coulomb'] = (coul[0], "coulomb.inp")
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
            self._paths['momentrate1'] = (mr_ascii[0], "moment_rate.mr")
            file_attrib, format_attrib = self._getAttributes(
                'momentrate', "Moment Rate Function Files ",
                "moment_rate.mr", "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                "Files of time vs. moment rate for source time "
                "functions ")
            etree.SubElement(file_tree, 'format', format_attrib)
            self._paths['momentrate2'] = (mr_plot[0], "moment_rate.png")
            file_attrib, format_attrib = self._getAttributes('momentrate',
                                                             "Moment Rate Function Files ", "moment_rate.png",
                                                             "image/png")
            etree.SubElement(file_tree, 'format', format_attrib)
        else:
            self._paths['momentrate2'] = (mr_plot[0], "moment_rate.png")
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
            self._paths['deformation'] = (surf[0], "surface_deformation.disp")
            file_attrib, format_attrib = self._getAttributes('surface',
                                                             "Surface Deformation File ",
                                                             "surface_deformation.disp", "text/plain")
            file_tree = etree.SubElement(contents, 'file', file_attrib)
            caption = etree.SubElement(file_tree, 'caption')
            caption.text = etree.CDATA(
                "Surface displacement resulting from finite fault, "
                "calculated using Okada-style deformation codes ")
            etree.SubElement(file_tree, 'format', format_attrib)

        tree = etree.ElementTree(contents)
        self._contents = tree
        return tree

    def createTimeseriesGeoJSON(self):
        """
        Create the timerseries geojson file.
        """
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
    def fromDirectory(cls, directory, eventid, model_number,
                      crustal_model=DEFAULT_MODEL,
                      comment=None, version=1, suppress_model=False):
        """
        Create instance based upon a directory and eventid.

        Args:
            directory (string): Path to directory.
            eventid (string): Eventid used for file naming. Default is empty
                    string.
            version (int): Product version number. Default is 1.

        Returns:
            WebProduct: Instance set for information for the web product.
        """
        product = cls()
        wave_prop = os.path.join(directory, "wave_properties.json")
        if os.path.exists(wave_prop):
            with open(wave_prop, 'r') as f:
                wave_dict = json.loads(f.read())
            if ('num_pwaves' not in wave_dict or
                    'num_shwaves' not in wave_dict or
                    'num_longwaves' not in wave_dict):
                raise Exception('Missing one of the required properties: '
                                'num_pwaves, num_shwaves, num_longwaves.')
            else:
                product._properties = {}
                product._properties['number-pwaves'] = wave_dict['num_pwaves']
                product._properties['number-shwaves'] = wave_dict['num_shwaves']
                product._properties['number-longwaves'] = wave_dict['num_longwaves']
                provided = True
        else:
            provided = False
        unavailable, files = product._files_unavailable(directory,
                                                        waves_provided=provided)
        file_strs = [f[0] + ': ' + f[1] for f in files]
        if unavailable is True:
            raise Exception('Missing required files %r' % file_strs)
        try:
            with open(directory + '/analysis.txt', 'r') as f:
                analysis = "".join(f.readlines())

            product.writeAnalysis(analysis, directory, eventid)
        except:
            analysis = "Not available yet."
        fsp_file = glob.glob(directory + "/" + "*.fsp")[0]
        fault = Fault.fromFiles(fsp_file, directory)
        product.event = fault.event
        product.segments = fault.segments
        fault.createGeoJSON()
        fault.corners['metadata']['eventid'] = eventid
        product.grid = fault.corners
        product.solution = model_number
        product.crustal_model = crustal_model
        product.comment = comment
        product.suppress_model = suppress_model
        product._timeseries_dict = fault.timeseries_dict
        calculated_sizes = fault.segment_sizes
        product.writeGrid(directory)
        product.storeProperties(directory, eventid, calculated_sizes)
        product.writeContents(directory)
        return product

    @property
    def paths(self):
        """
        Helper to return path dictionary.

        Returns:
            dictionary: Path information.
        """
        return self._paths

    @property
    def properties(self):
        """
        Helper to return properties dictionary.

        Returns:
            dictionary: Properties information.
        """
        return self._properties

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

    def storeProperties(self, directory, eventid, calculated_sizes=None):
        """
        Store PDL properties and creates properties.json.

        Args:
            directory (string): Path to directory.
            eventid (string): Eventid used for file naming.
            calculated_sizes (dict): Dictionary of calculated sizes.
        """
        props = {}
        props['eventsourcecode'] = eventid
        props['eventsource'] = 'us'
        if os.path.exists(os.path.join(directory, 'Readlp.das')):
            wave_file = os.path.join(directory, 'Readlp.das')
            props['number-pwaves'], props['number-shwaves'] = self._countWaveforms(
                wave_file)
        if os.path.exists(os.path.join(directory, 'synm.str_low')):
            try:
                with open(os.path.join(directory, 'synm.str_low'), 'rt') as f:
                    props['number-longwaves'] = int(f.readline().strip())
            except:
                props['number-longwaves'] = 0
        elif not os.path.exists(os.path.join(directory, 'wave_properties.json')):
            props['number-longwaves'] = 0
        URL_TEMPLATE = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/[EVENTID].geojson'
        url = URL_TEMPLATE.replace('[EVENTID]', 'us' + eventid)
        try:
            fh = urlopen(url)
            data = fh.read()
            fh.close()
            jdict = json.loads(data.decode())
            locstr = jdict['properties']['place']
        except:
            locstr = '%.4f, %.4f' % (self.event['lat'], self.event['lon'])
        props['latitude'] = self.event['lat']
        props['longitude'] = self.event['lon']
        props['location'] = locstr
        props['derived-magnitude'] = self.event['mag']
        props['scalar-moment'] = self.event['moment']
        props['derived-magnitude-type'] = 'Mw'
        props['depth'] = self.event['depth']
        props['eventtime'] = self.event['date']
        props['average-rise-time'] = self.event['avTr']
        props['average-rupture-velocity'] = self.event['avVr']
        props['hypocenter-x'] = float(self.event['Hypx'])
        props['hypocenter-z'] = float(self.event['Hypz'])
        props['maximum-frequency'] = float(self.event['Fmax'])
        props['minimum-frequency'] = float(self.event['Fmin'])
        props['model-dip'] = self.event['dip']
        props['model-length'] = self.event['length']
        props['model-rake'] = self.event['rake']
        props['model-strike'] = self.event['strike']
        props['model-top'] = self.event['htop']
        props['model-width'] = self.event['width']
        props['time-windows'] = int(self.event['time_windows'])
        props['velocity-function'] = self.event['velocity_func']
        props['segments'] = len(self.segments)
        max_vals = {'slip': [], 'depth': [], 'rise': []}
        for i, segment in enumerate(self.segments):
            idx = str(i + 1)
            if calculated_sizes is not None:
                props['subfault-' + idx + '-width'] = calculated_sizes[i]['width']
                props['subfault-' + idx +
                      '-length'] = calculated_sizes[i]['length']
                props['subfault-' + idx + '-area'] = calculated_sizes[i]['area']
            props['segment-' + idx + '-strike'] = segment['strike']
            props['segment-' + idx + '-dip'] = segment['dip']
            slips = segment['slip'].flatten()
            depths = segment['depth'].flatten()
            rises = segment['rise'].flatten()
            max_vals['slip'] += [slips[np.argmax(slips)]]
            max_vals['depth'] += [depths[np.argmax(depths)]]
            max_vals['rise'] += [rises[np.argmax(rises)]]
        props['maximum-slip'] = max_vals['slip'][np.argmax(max_vals['slip'])]
        props['maximum-rise'] = max_vals['rise'][np.argmax(max_vals['rise'])]
        props['crustal-model'] = self.crustal_model
        if not self.suppress_model:
            props['model-number'] = self.solution
        if self.comment is not None:
            props['comment'] = self.comment
        if self.properties is None:
            self._properties = props
        else:
            copy_props = copy.deepcopy(self._properties)
            copy_props.update(props)
            self._properties = copy_props

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

        Args:
            timeseries_dictents (dictionary): Dictionary of time series for
                each station.
        """
        self._timeseries_dict = timeseries_dict

    def writeAnalysis(self, analysis, directory, eventid):
        """
        Write the analysis.html file.

        Args:
            analysis (str): Analysis string.
            directory (str): Path to directory where contents.xml will be
                    written.
        """
        outfile = os.path.join(directory, "analysis.html")
        with open(outfile, 'w') as analysis_file:
            analysis_file.write(analysis)
        if self.paths is None:
            self._paths = {}
        self._paths['analysis'] = (outfile, "analysis.html")

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
        if self.paths is None:
            self._paths = {}
        self._paths['contents'] = (outdir, "contents.xml")
        # Add other files
        slip = self._checkDownload(directory, "*slip*.png")
        if len(slip) > 0:
            self._paths['slip'] = (slip[0], "slip.png")
        else:
            raise Exception('No slip image provided.')
        # Write property json for review
        prop_file = os.path.join(directory, "properties.json")
        serialized_prop = self._serialize(self.properties)
        with open(prop_file, 'w') as f:
            json.dump(serialized_prop, f, indent=4, sort_keys=True)
        self._paths['properties'] = (prop_file, "properties.json")

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
            json.dump(self.grid, outfile, indent=4, sort_keys=True)
        if self.paths is None:
            self._paths = {}
        self._paths['geojson'] = (write_path, "FFM.geojson")

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
            json.dump(self.timeseries_dict, outfile, indent=4, sort_keys=True)

    def zip_waveplots(self, directory):
        """
        Zips up wave plot images into "waveplots.zip".

        Args:
            directory (str): Directory where the file will be written.

        Returns:
            string: path to directory if wave plots are found or '' if they
                    are not.
        """
        wave_plots = glob.glob(os.path.join(directory, '*wave_*.png'))
        if len(wave_plots) > 0:
            path = os.path.join(directory, 'waveplots')
            if not os.path.exists(path):
                os.makedirs(path)
            for plot_path in wave_plots:
                base_file = os.path.basename(plot_path)
                new_file = os.path.join(path, base_file)
                shutil.copy(plot_path, new_file)
            shutil.make_archive(path, 'zip', path)
            shutil.rmtree(path)
            return path + '.zip'
        else:
            return ''

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
            file_path = file_paths[0]
            files += [file_path]
        return files

    def _countWaveforms(self, filename):
        """
        Count the number of wave forms.

        Args:
            filename (str): Path to wave file.
        """
        with open(filename, 'rt') as f:
            lines = f.readlines()
        num_lines = int(lines[4].strip())
        ns = 0
        np = 0
        # read the int value of the 8th column of each line.
        # if greater than 2, increment ns, otherwise increment np
        for i in range(5, num_lines):
            parts = lines[i].split()
            if float(parts[8]) > 2:
                ns += 1
            else:
                np += 1
        return (np, ns)

    def _files_unavailable(self, directory, waves_provided=False):
        """
        Helper to check for required files.

        Args:
            directory (string): Path to directory of FFM data.
            waves_provided (bool): Values for wave numbers have been provided.
        """
        if waves_provided:
            required = {
                'Moment Rate PNG': '*mr*.png',
                'Base Map PNG': '*base*.png',
                'Slip PNG': '*slip*.png',
                'FSP File': '*.fsp'
            }
        else:
            required = {
                'Moment Rate PNG': '*mr*.png',
                'Base Map PNG': '*base*.png',
                'Slip PNG': '*slip*.png',
                'FSP File': '*.fsp',
                'Wave File': 'Readlp.das'
            }
        unavailable = []
        for file_type in required:
            path = os.path.join(directory, required[file_type])
            if len(glob.glob(path)) < 1:
                unavailable += [(file_type, required[file_type])]
        if len(unavailable) > 0:
            return (True, unavailable)
        else:
            return (False, [])

    def _getAttributes(self, id, title, href, type):
        """
        Created contents attributes.

        Args:
            id (string): File id.
            title (string): File title.
            href (string): File name.
            type (string): File type
        """
        file_attrib = {'id': id, 'title': title}
        format_attrib = {'href': href, 'type': type}
        return file_attrib, format_attrib

    def _serialize(self, properties):
        """
        Helper function for making dictionary json serializable.

        Args:
            properties (dict): Dictionary of properties.

        Returns:
            dictionary: Dictionary of cleaned properties.
        """
        for key, value in properties.items():
            if isinstance(value, dict):
                properties[key] = dict(self._serialize(value))
            elif isinstance(value, datetime.datetime):
                properties[key] = value.strftime(TIMEFMT)
        return properties
