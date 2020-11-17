# stdlib imports
import getpass
import os
import shutil
import yaml

base = os.path.expanduser("~")
yaml_config = os.path.join(base, ".faultproduct.yaml")

with open(yaml_config, 'r') as config:
    config_dict = yaml.load(config, Loader=yaml.SafeLoader)
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
DEFAULT_MODEL = ("1D crustal model interpolated from CRUST2.0 "
                 "(Bassin et al., 2000).")

JAVA = shutil.which("java")
PRODUCT_TYPE = 'finite-fault'

TIMEFMT = "%Y-%m-%dT%H:%M:%S.%fZ"
