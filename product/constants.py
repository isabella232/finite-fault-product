# stdlib imports
import getpass
import os
import shutil
import yaml

base = os.path.expanduser("~")
yaml_config = os.path.join(base, ".faultproduct.yaml")

with open(yaml_config, 'r') as config:
    config_dict = yaml.load(config)
try:
    BASE_PDL_FOLDER = config_dict["outputfolder"]
    JAR = config_dict["pdl"]["jarfile"]
    CFG = config_dict["pdl"]["configfile"]
    PRIVATEKEY = config_dict["pdl"]["privatekey"]
except:
    raise Exception("The following configuration keys are required in the "
            "~/.faultproduct.yaml file."
            "\noutputfolder: <path to folder where products will be written>"
            "\npdl:"
            "\n    configfile: <path to PDL config"
            "\n    jarfile: <path to PDL jar file>"
            "\n    privatekey: <path to PDL privatekey file>")
JAVA = shutil.which("java")
PRODUCT_TYPE = 'finite-fault'

TIMEFMT = "%Y-%m-%dT%H:%M:%S.%fZ"

PAGE_TEMPLATE = """<html>
<head>
</head>
<h1>[STATUS] Finite Fault Results for the [DATE] Mw [MAG] [LOCATION]
Earthquake (Version [VERSION]) </h1>
<hr/>

<h1>DATA Process and Inversion </h1>
<p>
We used GSN broadband waveforms downloaded from the NEIC waveform server.
We analyzed [PWAVE] teleseismic broadband P waveforms, [SHWAVE] broadband SH waveforms,
and [LONGWAVE] long period surface waves selected based on data quality and azimuthal
distribution. Waveforms are first converted to displacement by removing the
instrument response and are then used to constrain the slip history using a finite
fault inverse algorithm (Ji et al., 2002). We begin modeling using a hypocenter
matching or adjusted slightly from the initial NEIC solution (Lon. = [LON] deg.; Lat. =
[LAT] deg., Dep. = [DEPTH] km), and a fault plane defined using either the rapid W-Phase
moment tensor (for near-real time solutions), or the gCMT moment tensor (for
historic solutions).
</p>
<hr />
<h2>Result</h2>
<p>
[RESULT]
</p>

<img SRC="basemap.png"><br /><br />
<p>
Surface projection of the slip distribution superimposed on GEBCO bathymetry. Red lines indicate major plate boundaries [Bird, 2003]. Gray circles, if present, are aftershock locations (up to 7 days), sized by magnitude.

<!-- Surface projection of the slip distribution superimposed on GEBCO -->
<!-- bathymetry. Thick white lines indicate major plate boundaries [Bird, 2003]. Gray circles, if present, are aftershock locations, sized by magnitude. -->
</p><hr />

<h2>Cross-section of slip distribution</h2>
<img SRC="slip.png"><br /><br />
<p>
Cross-section of slip distribution. The strike direction is indicated
above each fault plane and the hypocenter location is denoted by a
star. Slip amplitude is shown in color and the motion direction of the
hanging wall relative to the footwall (rake angle) is indicated with
arrows. Contours show the rupture initiation time in seconds.
</p>
<hr />
<h2>Moment Rate Function</h2><br />
<img SRC="moment_rate.png"><br /><br />
<p>
Source time function, describing the rate of moment release with time
after earthquake origin, relative to the peak moment rate (listed in
the top right corner of the plot).
</p>


<h2>Scientific Analysis:</h2>
[ANALYSIS]
<hr />

<h2>Slip Distribution:</h2>
The plots above and a variety of data files for the finite fault solution
in different formats can be obtained by clicking on the Downloads
tab below.
<hr />

<h2>References</h2>
<p>

Ji, C., D.J. Wald, and D.V. Helmberger, Source description of the 1999
Hector Mine, California earthquake; Part I: Wavelet domain inversion
theory and resolution analysis, <em>Bull. Seism. Soc. Am.</em>, Vol
92, No. 4. pp. 1192-1207, 2002.

<br /> <br />

Bassin, C., Laske, G. and Masters, G., The Current Limits of
Resolution for Surface Wave Tomography in North America, <em>EOS Trans
AGU</em>, 81, F897, 2000.

<br /> <br />

Ji, C., D. V. Helmberger, D. J. Wald, and K. F. Ma (2003), Slip
history and dynamic implications of the 1999 Chi-Chi, Taiwan,
earthquake, <em>J Geophys Res-Sol Ea</em>, 108(B9).

<br /> <br />

Shao, G. F., X. Y. Li, C. Ji, and T. Maeda (2011), Focal mechanism and
slip history of the 2011 M-w 9.1 off the Pacific coast of Tohoku
Earthquake, constrained with teleseismic body and surface waves, <em>Earth
Planets Space</em>, 63(7), 559-564.


</p>

<hr />
<h2>Acknowledgement and Contact Information</h2>
<p>
This work is supported by the National Earthquake Information Center (NEIC) of United States Geological Survey. This web page is built and maintained by <a href="mailto:ghayes@usgs.gov"> Dr. G. Hayes </a> at the NEIC. </p>
</body>
</html>
"""
