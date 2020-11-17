# third party imports
import datetime
from impactutils.transfer.pdlsender import PDLSender
from libcomcat.search import get_event_by_id, search
from libcomcat.classes import Product
import numpy as np
import os

# local imports
from product.constants import BASE_PDL_FOLDER, PRODUCT_TYPE, TIMEFMT


def delete_fault(configfile, eventsource, eventsourcecode, jarfile, java,
                 privatekey, product_source, number=None):
    """Delete finite fault product.

    Args:
        configfile (str): Location of PDL config file.
        eventsource (str): Network that originated the event.
        eventsourcecode (str): Event code.
        jarfile (str): Location of PDL jar file.
        java (str): Location of Java binary.
        privatekey (str): Location of PDL private key.
        product_source (str): Network contributing this product to ComCat.
        number (int): Number of product (used for two plane solutions).
                Default is None.
    Returns:
        str: Message with any error information.
    """
    props = {}
    props['java'] = java
    props['jarfile'] = jarfile
    props['privatekey'] = privatekey
    props['configfile'] = configfile
    props['source'] = product_source
    props['eventsource'] = eventsource
    props['eventsourcecode'] = eventsourcecode
    props['code'] = eventsource + eventsourcecode
    if number is not None:
        props['code'] += '_' + str(number)
    props['type'] = 'finite-fault'
    sender = PDLSender(properties=props)
    msg = sender.cancel()
    return (msg)


def get_date(milliseconds):
    """Helper function to convert from java ms timestamp to datetime.

    Args:
        milliseconds (float, int): Timestamp in milliseconds.

    Returns:
        datetime.datetime: Datetime object.
    """
    seconds = milliseconds / 1000
    sub_seconds = (milliseconds % 1000.0) / 1000.0
    date = datetime.datetime.fromtimestamp(seconds + sub_seconds)
    return date


def get_fault(eventsource, eventsourcecode, comcat_host='earthquake.usgs.gov',
              model=None, write_directory=None):
    """Retrieve the latest finite_fault data for a given event.
    Args:
        eventsource (str): Network that originated the event.
        eventsourcecode (str): Event code from network that originated
                               the event.
        comcat_host (str): (for testing) Specify an alternate comcat host.
        two_model (bool): Whether the ffm has two equally valid solutions.
                Default is False.
        write_directory (str): Path to directory where files will be written.
                Default is None.
    """
    eventid = eventsource + eventsourcecode
    try:
        detail = get_event_by_id(eventid, host=comcat_host)
    except Exception as e:
        raise(e)
    if not detail.hasProduct(PRODUCT_TYPE):
        raise Exception('Event %r has no finite-fault product.' % eventid)
    if model is not None:
        mod1 = ''
        for prod in detail._jdict['properties']['products'][PRODUCT_TYPE]:
            if prod['code'].endswith(f'_{model}'):
                if mod1 == '':
                    latest_time1 = get_date(prod['updateTime'])
                if get_date(prod['updateTime']) >= latest_time1:
                    latest_time1 = get_date(prod['updateTime'])
                    mod1 = Product('finite-fault', 'last', prod)
        if mod1 == '':
            raise Exception(f'Model number, {model}, was not found for this '
                            'finite fault product %r' % eventid)
    else:
        mod1 = detail.getProducts(PRODUCT_TYPE, version='last')[0]

    if write_directory is not None:
        now = datetime.datetime.utcnow()
        date_str = now.strftime(TIMEFMT.replace(':', '_').replace('.%f', ''))
        if model is not None:
            dir1 = os.path.join(write_directory,
                                eventid + f'_{model}_' + date_str)
            if not os.path.exists(dir1):
                os.makedirs(dir1, exist_ok=True)
            for file1 in mod1.contents:
                filename1 = os.path.join(dir1, os.path.basename(file1))
                mod1.getContent(file1, filename1)
        else:
            dir = os.path.join(write_directory, eventid + '_' + date_str)
            if not os.path.exists(dir):
                os.makedirs(dir, exist_ok=True)
            for download_file in mod1.contents:
                filename = os.path.join(dir, os.path.basename(download_file))
                mod1.getContent(download_file, filename)


def store_fault(configfile, eventsource, eventsourcecode, jarfile, java,
                pdlfolder, privatekey, product_source, properties, reviewed,
                number, dry_run=False, suppress=False):
    """Store finite fault product using pdl.

    Args:
        configfile (str): Location of PDL config file.
        eventsource (str): Network that originated the event.
        eventsourcecode (str): Event code.
        jarfile (str): Location of PDL jar file.
        java (str): Location of Java binary.
        pdlfolder (str): Folder to send.
        privatekey (str): Location of PDL private key.
        product_source (str): Network contributing this product to ComCat.
        properties (str): Dictionary of product properties.
        number (int): Number of product (used to distinguish multiple solutions).
        dry_run (bool): Should this be a dry run that only outputs the pdl command
            without sending the product. Default is False.
        suppress (bool): Suppress the number suffix on the event code.

    Returns:
        int: Number of files transferred
        str: Message with any error information.
    """
    props = {}
    props['java'] = java
    props['jarfile'] = jarfile
    props['privatekey'] = privatekey
    props['configfile'] = configfile
    props['source'] = product_source
    props['eventsource'] = eventsource
    props['eventsourcecode'] = eventsourcecode
    props['code'] = eventsource + eventsourcecode
    if not suppress:
        props['code'] += '_' + str(number)
    props['type'] = 'finite-fault'
    if reviewed:
        properties["review-status"] = "reviewed"
    sender = PDLSender(properties=props, local_directory=pdlfolder,
                       product_properties=properties)
    if dry_run:
        nfiles = 0
        cmd = sender._pdlcmd
        cmd = cmd.replace('[STATUS]', 'UPDATE')
        cmd = sender._replace_required_properties(cmd)
        cmd = sender._replace_files(cmd)
        cmd = sender._replace_product_properties(cmd)
        cmd = sender._replace_optional_properties(cmd)
        msg = cmd
    else:
        nfiles, msg = sender.send()
    return (nfiles, msg)
