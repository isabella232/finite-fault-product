Status
=======

[![Build Status](https://travis-ci.org/usgs/finite-fault-product.svg?branch=master)](https://travis-ci.org/usgs/finite-fault-product)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/81d612b63c864f3fb894f4e5bec90b49)](https://www.codacy.com/app/usgs/finite-fault-product?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=usgs/finite-fault-product&amp;utm_campaign=Badge_Grade)

[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/81d612b63c864f3fb894f4e5bec90b49)](https://www.codacy.com/app/usgs/finite-fault-product?utm_source=github.com&utm_medium=referral&utm_content=usgs/finite-fault-product&utm_campaign=Badge_Coverage)


# Introduction

finite-fault-product is a project designed to provide a number of functions in support of the ShakeMap
project and earthquake event pages.

# Installing

If you already have a miniconda or anaconda Python 3.X environment:

 - `conda install impactutils`
 - `conda install libcomcat`
 - `conda install lxml`
 - `conda install numpy`
 - `conda install openquake.engine`
 - `conda install openpyxl`
 - `conda install pandas`
 - `pip install git+https://github.com/usgs/finite-fault-product.git`

 Automatic environment creation using miniconda:

 - `git clone https://github.com/usgs/finite-fault-product.git`
 - `cd finite-fault-product`
 - `bash install.sh`
 - `conda activate faultproduct`


## Config file for PDL constants
A config file will automatically be created if one doesn't already exists.
The file (~/.faultproduct.yaml) should look similary to:
<pre>
outputfolder: [path to folder where products will be written]
pdl:
    configfile: [path to PDL config]
    jarfile: [path to PDL jar file]
    privatekey: [path to PDL privatekey file]
</pre>

The locations of these files will default to:
<pre>
outputfolder: [home directory]/pdlout
pdl:
    configfile: [home directory]/ProductClient/config.ini
    jarfile: [home directory]/ProductClient/ProductClient.jar
    privatekey: [home directory]/ProductClient/id_dsa_ffm
</pre>

These paths can be updated in the config file.

## Updating

Updating automated install:
- `cd finite-fault-product`
- `conda activate faultproduct`
- `git pull --ff-only https://github.com/usgs/finite-fault-product.git master`
- `bash install.sh`

If no new dependencies have been added, `pip install -e .` may be used instead of `bash install.sh`.


Updating manually installed:
 - `pip install --upgrade git+https://github.com/usgs/finite-fault-product.git`

 If new dependencies have been added, they must be installed first.


# Tools

Load finite fault data and create products.

## fault
Designed to analyze finite fault models and time series.
* `fault.py` Class to analyze fault models.

### fault.io
fault.io is designed to read finite fault data from fsp, dat, and syn files.

 * `fsp.py` Load rupture model.
 * `timeseries.py` Load data and synthetic seismograms.

## product
product is designed to create eventpages and ShakeMap products.
* `web_product.py` Create web product from time series and fault data. (Under construction)
* `pdl.py` Contains methods for sending products to pdl.
* `shakemap_product.py` Create shakemap product from time series and fault data. (Unavailable)

## sendproduct
Includes functionality to send a finite fault product.

usage: sendproduct [-h] [-ffm2 FFM2] [-v COMMENT] [-r] net eventid ffm1

Send a finite fault product for event pages.

<table>
  <tr>
    <th colspan="2">Positional arguments</th>
  </tr>
  <tr>
    <td>eventsource</td>
    <td>Source of the original event ID. (example: us, usp,
                        ci).</td>
  </tr>
  <tr>
    <td>source</td>
    <td>Source of this product (i.e., contributor of the
                        product. example: us).</td>
  </tr>
  <tr>
    <td>eventid</td>
    <td>Event identification code.</td>
  </tr>
  <tr>
    <td>ffm1</td>
    <td>Directory where all files are contained for the finite fault model</td>
  </tr>
</table>

<table>
  <tr>
    <th colspan="2">Optional arguments</th>
  </tr>
  <tr>
    <td>-h, --help</td>
    <td>Show the help message and exit</td>
  </tr>
  <tr>
    <td>-ffm2 FFM2</td>
    <td>Directory where all files are contained for the second finite fault model</td>
  </tr>
  <tr>
    <td>-v COMMENT, --version COMMENT</td>
    <td>Add a version number to the finite fault output</td>
  </tr>
  <tr>
    <td>-r, --review</td>
    <td>Don't send products to PDL. Only create the product folder</td>
  </tr>
  <tr>
    <td>-x, --not-reviewed</td>
    <td>Mark that the sent product was not reviewed by a scientist. This will cause a flag to be displayed on the web page</td>
  </tr>
</table>

## getproduct
Includes functionality to view a finite fault product.

usage: getproduct [-h] [-t] [-c HOST] source eventid directory

Get the latest finite-fault product for an event.

<table>
  <tr>
    <th colspan="2">Positional arguments</th>
  </tr>
  <tr>
    <td>source</td>
    <td>Source code (example: us).</td>
  </tr>
  <tr>
    <td>eventid</td>
    <td>Event identification code.</td>
  </tr>
  <tr>
    <td>directory</td>
    <td>Directory where all files will be written.</td>
  </tr>
</table>

<table>
  <tr>
    <th colspan="2">Optional arguments</th>
  </tr>
  <tr>
    <td>-h, --help</td>
    <td>Show the help message and exit</td>
  </tr>
  <tr>
    <td> -t, --two-model</td>
    <td>This finite fault has two solutions.</td>
  </tr>
  <tr>
    <td>-c HOST, --comcat-host HOST</td>
    <td>Comcat host. Default is earthquake.usgs.gov</td>
  </tr>
</table>


## deleteproduct
Includes functionality to delete a finite fault product.
usage: deleteproduct [-h] [-t] [-m MODEL] eventsource source eventid

Delete a finite-fault product for an event.

<table>
  <tr>
    <th colspan="2">Positional arguments</th>
  </tr>
  <tr>
    <td>eventsource</td>
    <td>Source of the original event ID. (example: us, usp,
                        ci).</td>
  </tr>
  <tr>
    <td>source</td>
    <td>Source of this product (i.e., contributor of the
                        product. example: us).</td>
  </tr>
  <tr>
    <td>eventid</td>
    <td>Event identification code.</td>
  </tr>
</table>

<table>
  <tr>
    <th colspan="2">Optional arguments</th>
  </tr>
  <tr>
    <td>-h, --help</td>
    <td>Show the help message and exit</td>
  </tr>
  <tr>
    <td> -t, --two-model</td>
    <td>This finite fault has two solutions.</td>
  </tr>
  <tr>
    <td>-m MODEL, --model-number MODEL</td>
    <td>Model number to delete.</td>
  </tr>
</table>

See [docs](https://github.com/usgs/finite-fault-product/tree/master/docs) for more detailed explanations.
