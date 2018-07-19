import getpass

#PDL command stuff
JARFILE = 'ProductClient.jar'
CONFIGFILE = 'dev_config.ini'

#depending on whether user is "gavin" or "mhearne", choose one of these
DEVPDLPATH = '/Users/%s/ProductClient' % getpass.getuser()
PRODPDLPATH = '/Users/%s/Desktop/ProductClient' % getpass.getuser()

#folder where all pdl output should go
BASE_PDL_FOLDER = '/Users/%s/pdloutput/' % getpass.getuser()
