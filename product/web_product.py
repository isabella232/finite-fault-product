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
    def __init__(self, inversion_process, result, analysis):
        self._result = result
        self._inversion_process = inversion_process
        self._analysis = analysis
        self._timeseries_dict = None
        self._event = None
        self._segments = None
        self._grid = None
        self._downloads = None
        self._contents = None

    @property
    def analysis(self):
        """
        Helper to return analysis information.

        Returns:
            string: _analysis information.
        """
        return self._analysis

    def collectDownloads(self, directory, eventid):
        """
        Create a dictionary of the downloads for web pages.

        Args:
            directory (string): Path to directory.
            eventid (string): Eventid used for file naming.

        Returns:
            dictionary: dictionary of downloads.

        Notes:
            Currently assumes one fault model per event.
        """
        eventid = eventid.lower()
        # Look for  and add basemap
        basemap = self._setDownload(
                "Map of finite fault showing it's geographic context ",
                "web/" + eventid + ".png", directory, "/*_basemap.png",
                "Base Map ", "image/png")
        # CMT solution
        cmt = self._setDownload(
                "Full CMT solution for every point in finite fault region ",
                "web/CMTSOLUTION", directory, "/*CMTSOLUTION*",
                "CMT Solution ", "text/plain")
        # inversion files
        basic_inversion = self._setDownload(
                "Basic inversion parameters for each node in the finite fault ",
                "web/" + eventid + ".param", directory, "/*.param",
                "Inversion Parameters File 1 ", "text/plain")
        full_inversion = self._setDownload(
                "Complete inversion parameters for the finite fault, "
                "following the SRCMOD FSP format (http://equake-rc.info/) ",
                "web/" + eventid + ".fsp", directory, "/*.fsp",
                "Inversion Parameters File 2 ", "text/plain")
        # Coulomb inp
        coulomb = self._setDownload(
                "Format necessary for compatibility with Coulomb3 "
                "(http://earthquake.usgs.gov/research/software/coulomb/) ",
                "web/" + eventid + "_coulomb.inp", directory,
                "/*_coulomb.inp", "Coulomb Input File ", "text/plain")
        # Moment rate
        rate = self._setDownload(
                "Ascii file of time vs. moment rate, used for plotting "
                "source time function ",
                "web/" + eventid + ".mr", directory, "/*.mr",
                "Moment Rate Function File ", "text/plain")
        # surface displacement
        displacement = self._setDownload(
                "Surface displacement resulting from finite fault, "
                "calculated using Okada-style deformation codes ",
                "web/" + eventid + ".disp", directory, "/*.disp",
                "Surface Deformation File ", "text/plain")
        # store information
        downloads = OrderedDict()
        downloads['basemap'] = basemap
        downloads['basemap']['id'] = 'basemap'
        downloads['cmtsolution1'] = cmt
        downloads['cmtsolution1']['id'] = 'cmtsolution1'
        downloads['inpfile1_1'] = basic_inversion
        downloads['inpfile1_1']['id'] = 'inpfile1_1'
        downloads['inpfile2_1'] = full_inversion
        downloads['inpfile2_1']['id'] = 'inpfile2_1'
        downloads['coulomb_1'] = coulomb
        downloads['coulomb_1']['id'] = 'coulomb_1'
        downloads['momentrate1'] = rate
        downloads['momentrate1']['id'] = 'momentrate1'
        downloads['surface1'] = displacement
        downloads['surface1']['id'] = 'surface1'
        for file_id in downloads:
            download_file = downloads[file_id]['file'].lower()
            if file_id.find('cmt') < 0 :
                assert download_file.find(eventid) >= 0
        self.downloads = downloads

    @property
    def contents(self):
        """
        Helper to return contents information.

        Returns:
            string: contents information.
        """
        return self._contents

    def createContents(self, directory):
        """
        Create the contents.xml file.

        Args:
            directory (str): Directory path to validate existance of files.
        """
        if (self.timeseries_dict is None or self.grid is None or
                self.result is None or self.analysis is None or
                self.segments is None or self.inversion_process is None or
                self.downloads is None):
            raise Exception('All attributes of WebProduct must be populated '
                    'before the contents.xml can ve created.')
        contents = etree.Element('contents')

        for id in self.downloads:
            params = self.downloads[id].copy()
            file_attributes = {'id': params['id'], 'title': params['title']}
            download_file = etree.SubElement(contents, 'file',
                    file_attributes)
            caption = etree.SubElement(download_file, 'caption')
            caption.text = etree.CDATA(params['caption'])
            format_attributes = {'href': params['file'],
                    'type': params['type']}
            etree.SubElement(download_file, 'format', format_attributes)
        # GeoJSON grid
        if not os.path.exists(os.path.join(directory, 'FFM.geojson')):
            raise FileNotFoundError('Missing FFM geojson file.')
        grid_attributes = {'id': 'geojson', 'title': 'FFM GeoJSON '}
        grid_file = etree.SubElement(contents, 'file',
                grid_attributes)
        grid_caption = etree.SubElement(grid_file, 'caption')
        caption_str = ("GeoJSON file of the finite fault model grid and "
                "earthquake location ")
        grid_caption.text = etree.CDATA(caption_str)
        grid_format = {'href': 'web/FFM.geojson',
                'type': "text/plain"}
        etree.SubElement(grid_file, 'format', grid_format)

        # Time series JSON
        if not os.path.exists(os.path.join(directory, 'timeseries.json')):
            raise FileNotFoundError('Missing timeseries file.')
        timeseries_attributes = {'id': 'timeseries',
                'title': 'Time Series JSON '}
        timeseries_file = etree.SubElement(contents, 'file',
                timeseries_attributes)
        timeseries_caption = etree.SubElement(timeseries_file, 'caption')
        caption_str = "JSON file of time series data and synthetic models "
        timeseries_caption.text = etree.CDATA(caption_str)
        timeseries_format = {'href': 'web/timeseries.json',
                'type': "text/plain"}
        etree.SubElement(timeseries_file, 'format', timeseries_format)

        # Comment JSON
        if not os.path.exists(os.path.join(directory, 'comments.json')):
            raise FileNotFoundError('Missing comments file.')
        timeseries_attributes = {'id': 'comments', 'title': 'Comment JSON '}
        timeseries_file = etree.SubElement(contents, 'file',
                timeseries_attributes)
        timeseries_caption = etree.SubElement(timeseries_file, 'caption')
        caption_str = ("JSON file of processing and result comments for this "
                "finite fault model ")
        timeseries_caption.text = etree.CDATA(caption_str)
        timeseries_format = {'href': 'web/comments.json',
                'type': "text/plain"}
        etree.SubElement(timeseries_file, 'format', timeseries_format)

        tree = etree.ElementTree(contents)
        self._contents = tree

    @property
    def downloads(self):
        """
        Helper to return downloads dictionary.

        Returns:
            dictionary: Downloads information.
        """
        return self._downloads

    @downloads.setter
    def downloads(self, downloads):
        """
        Helper to set downloads dictionary.

        downloads (dictionary): Downloads information.
        """
        self._downloads = downloads

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

    @property
    def inversion_process(self):
        """
        Helper to return inversion information.

        Returns:
            string: Inversion information.
        """
        return self._inversion_process

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
        inversion_file = os.path.join(directory, 'inversion_process.txt')
        with open (inversion_file, "r") as myfile:
            inversion = myfile.readlines()
        analysis_file = os.path.join(directory, 'analysis.txt')
        with open (analysis_file, "r") as myfile:
            analysis = myfile.readlines()
        result_file = os.path.join(directory, 'result.txt')
        with open (result_file, "r") as myfile:
            result = myfile.readlines()
        fsp_file = glob.glob(directory + "/" + "*.fsp")[0]
        assert fsp_file.find(eventid) >= 0
        fault = Fault.fromFiles(fsp_file, directory)
        product = cls(inversion, result, analysis)
        product.writeComments(directory)
        product.timeseries_dict = fault.timeseries_dict
        product.writeTimeseries(directory)
        product.event = fault.event
        product.segments = fault.segments
        fault.createGeoJSON()
        product.grid = fault.corners
        product.writeGrid(directory)
        if include_downloads:
            product.collectDownloads(directory, eventid)
        return product

    @property
    def result(self):
        """
        Helper to return result information.

        Returns:
            string: Result information.
        """
        return self._result

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

    @timeseries_dict.setter
    def timeseries_dict(self, timeseries_dict):
        """
        Helper to set time series dictionary.

        segmtimeseries_dictents (dictionary): Dictionary of time series for
                each station.
        """
        self._timeseries_dict = timeseries_dict

    def writeComments(self, directory):
        """
        Writes comments on inversion, analysis, and results in a JSON format.

        Args:
            directory (str): Directory where the file will be written.
        """
        write_path = os.path.join(directory, 'comments.json')
        comments = OrderedDict()
        comments['inversion_process'] = self.inversion_process
        comments['result'] =  self.result
        comments['analysis'] = self.analysis
        with open(write_path, 'w') as outfile:
            json.dump(comments, outfile)

    def writeContents(self, directory):
        """
        Write the contents.xml file.

        Args:
            directory (str): Path to directory where contents.xml will be
                    written.
        """
        if  self.contents is None:
            self.createContents(directory)
        tree = self.contents
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
            json.dump(self.grid, outfile)

    def writeTimeseries(self, directory):
        """
        Writes time series in a JSON format.

        Args:
            directory (str): Directory where the file will be written.
        """
        if self.timeseries_dict is None:
            raise Exception('The time series dictionary has not been set.')
        write_path = os.path.join(directory, 'timeseries.json')
        with open(write_path, 'w') as outfile:
            json.dump(self.timeseries_dict, outfile)

    def _setDownload(self, caption, default, directory, file_pattern,
            title, file_type):
        """
        Helper to check for a file and set download dictionary section.

        Args:
            caption (string): Caption for download file.
            default (string): Default file path.
            directory (string): Path to directory of download data.
            file_pattern (string): Pattern of file name.
            title (string): Title of download file.
            file_type (string): Type of file.
        """
        # attempt to find file or use default
        try:
            file_path = os.path.join('web', os.path.basename(
                    glob.glob(directory + file_pattern)[0]))
        except IndexError:
            warnings.warn('Missing file %r file. Setting to '
                    'default file path: %r' % (title, default))
            file_path = default
        download = {}
        download['file'] = file_path
        download['caption'] = caption
        download['title'] = title
        download['type'] = file_type
        return download
