 #!/usr/bin/env

# stdlib imports
from collections import OrderedDict
import glob
import json
import os

# third party imports
import numpy as np


def read_from_directory(input_directory):
    """Collects directory of finite fault time series data into JSON.

    Args:
        input_directory (str): Path to finite fault files.
        output_file (str): Path to output JSON file.
    """
    if not os.path.exists(input_directory):
        raise Exception('Input directory does not exist: %s' % input_directory)

    s_data_paths = glob.glob(os.path.join(input_directory, '*.S.dat'))
    s_synth_paths = glob.glob(os.path.join(input_directory, '*.S.syn'))
    p_data_paths = glob.glob(os.path.join(input_directory, '*.P.dat'))
    p_synth_paths = glob.glob(os.path.join(input_directory, '*.P.syn'))
    z_data_paths = glob.glob(os.path.join(input_directory, '*.Z.swave.dat'))
    z_synth_paths = glob.glob(os.path.join(input_directory, '*.Z.swave.syn'))
    t_data_paths = glob.glob(os.path.join(input_directory, '*.T.swave.dat'))
    t_synth_paths = glob.glob(os.path.join(input_directory, '*.T.swave.syn'))

    wave_dict = create_wave_dict(s_data_paths, s_synth_paths, p_data_paths,
                     p_synth_paths, z_data_paths, z_synth_paths,
                     t_data_paths, t_synth_paths)
    return wave_dict

def _add_data(data_paths, synth_paths, wave_type, wave_dict):
    """Helper to read data from finite fault files into a dictionary.

    Args:
        data_paths (list): List of paths (str) to time series data.
        synth_paths (list): List of paths (str) to synthetic time series.
        wave_type (str): Phase of time series.
        wave_dict (list): Dictionary or time series.
    """
    # Loop through all data paths of a certain type
    for idx, data_path in enumerate(data_paths):
        data_station, time, displacement = read_file(data_path)
        data_dict = {}
        data_dict['time'] = time.tolist()
        data_dict['displacement'] = displacement.tolist()
        # Check if the station key already exists in the dictionary
        if data_station not in wave_dict:
            wave_dict[data_station] =  OrderedDict()
            metadata = _get_metadata(data_station)
            wave_dict[data_station]['metadata'] = metadata
        if wave_type not in wave_dict[data_station]:
            wave_dict[data_station][wave_type] = {}
        wave_dict[data_station][wave_type]['data'] = data_dict
    # Loop through all synthetic paths of a certain type
    for idx, synth_path in enumerate(synth_paths):
        synth_station, time, displacement = read_file(synth_path)
        synth_dict = {}
        synth_dict['time'] = time.tolist()
        synth_dict['displacement'] = displacement.tolist()
        # Check if the station key already exists in the dictionary
        if synth_station not in wave_dict:
            wave_dict[synth_station] = OrderedDict()
            metadata = _get_metadata(synth_station)
            wave_dict[synth_station]['metadata'] = metadata
        if wave_type not in wave_dict[synth_station]:
            wave_dict[synth_station][wave_type] = {}
        wave_dict[synth_station][wave_type]['synthetic'] = synth_dict
    return wave_dict


def create_wave_dict(s_data_paths, s_synth_paths, p_data_paths,
                     p_synth_paths, z_data_paths, z_synth_paths,
                     t_data_paths, t_synth_paths):
    """Stores data from finite fault files into a dictionary.

    Args:
        s_data_paths (list): List of paths (str) to s time series data.
        s_synth_paths (list): List of paths (str) to s synthetic.
        p_data_paths (list): List of paths (str) to p time series data.
        p_synth_paths (list): List of paths (str) to p synthetic.
        z_data_paths (list): List of paths (str) to z time series data.
        z_synth_paths (list): List of paths (str) to z synthetic.
        t_data_paths (list): List of paths (str) to t time series data.
        t_synth_paths (list): List of paths (str) to t synthetic.

    Returns:
        dictionary: Dictionary of time series data.


    Notes: The dictionary of timeseries data is formatted as follows
        {
            <STATION>: {
                "metadata": {
                    "site": str,
                    "station": str,
                    "network": str,
                    "channel": str,
                    "location": str
                },
                <PHASE>: {
                    "data": {
                        "time": ndarray,
                        "displacement": ndarray
                    },
                    "synthetic": {
                        "time": ndarray,
                        "displacement": ndarray
                    }
                },
                ...
            },
            ...
        }
    """
    wave_dict = {}
    # Add S-Data
    wave_dict = _add_data(s_data_paths, s_synth_paths, 'S', wave_dict)
    # Add P-Data
    wave_dict = _add_data(p_data_paths, p_synth_paths, 'P', wave_dict)
    # Add Z-Data
    wave_dict = _add_data(z_data_paths, z_synth_paths, 'Z', wave_dict)
    # Add T-Data
    wave_dict = _add_data(t_data_paths, t_synth_paths, 'T', wave_dict)
    return wave_dict

def _get_metadata(station):
    """Helper to get the metadata for a specific station.

    Args:
        station (str): Station code.
    """
    metadata_dict = {}
    metadata_dict['station'] = station
    return metadata_dict

def read_file(path):
    """Helper to read data from a finite fault file.

    Args:
        path (str): Path to finite fault file.

    Returns:
        tuple: (Station name (str), Array of time stamps (ndarray),
            Displacement (ndarray))
    """
    filename = os.path.basename(path)
    station_idx =  filename.find('.')
    station_name = filename[0 : station_idx]
    time, displacement = np.genfromtxt(path, usecols=(0,1),
            dtype=float, unpack=True)
    return station_name, time, displacement
