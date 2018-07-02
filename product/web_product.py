 #!/usr/bin/env

# stdlib imports
import json

# local imports
from fault.fault import Fault


class WebProduct(object):
    """Class for creating web products."""
    def __init__(self):
        self._timeseries_dict = None
        self._event = None
        self._segments = None

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

    @classmethod
    def from_fault(cls, fault):
        """
        Create instance based upon a Fault object.

        Args:
            fault (fault.fault.Fault): Fault object.

        Returns:
            WebProduct: Instance set for information for the web product.
        """
        if not isinstance(fault, Fault):
            raise Exception('Not a Fault object.')
        product = cls()
        product.timeseries_dict = fault.timeseries_dict
        product.event = fault.event
        product.segments = fault.segments
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

    @timeseries_dict.setter
    def timeseries_dict(self, timeseries_dict):
        """
        Helper to set time series dictionary.

        segmtimeseries_dictents (dictionary): Dictionary of time series for
                each station.
    """
        self._timeseries_dict = timeseries_dict

    def write_timeseries(self, output_file):
        """
        Writes timeseries in a GeoJSON format.

        ArgsL
            output_file (str): Path to written file.
        """
        if self.timeseries_dict is None:
            raise Exception('The time series dictionary has not been set.')
        with open(output_file, 'w') as outfile:
            json.dump(self.timeseries_dict, outfile)
