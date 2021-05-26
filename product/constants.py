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
    try:
        SMTP_SERVER = config_dict['email']["smtp"]
        EMAIL_SENDER = config_dict['email']["sender"]
    except KeyError:
        SMTP_SERVER = None
        EMAIL_SENDER = None
        arguments = ("\nemail:\n    smtp: <SMTP SERVER>\n    sender: "
                     "<SENDER EMAIL ADDRESS>")
        print("No SMTP server and/or sender specified, so email "
              "functionality will not be available. Specify these "
              f"arguments in .faultproduct.yaml as '{arguments}'")
    try:
        DEFAULT_ALERT_RECIPIENTS = config_dict['email']["default_alert_recipients"].split(',')
    except:
        DEFAULT_ALERT_RECIPIENTS = None
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
