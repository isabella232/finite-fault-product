# third party imports
import datetime
from impactutils.transfer.pdlsender import PDLSender
from libcomcat.search import get_event_by_id, search
from libcomcat.classes import VersionOption, Product
import numpy as np
import os

# local imports
from product.constants import BASE_PDL_FOLDER, PRODUCT_TYPE, TIMEFMT


def store_fault (configfile, eventsource, eventsourcecode, jarfile, java,
        pdlfolder, privatekey, product_source, properties,
        number=None):
    """Store parametric data.

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
        number (int): Number of product (used for two plane solutions).
                Default is None.
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
    if number is not None:
        props['code'] += '_' + str(number)
    props['type'] = 'finite-fault'
    sender = PDLSender(properties=props, local_directory=pdlfolder,
                       product_properties=properties)
    nfiles, msg = sender.send()
    return (nfiles, msg)

def delete_fault(configfile, eventsource, eventsourcecode, jarfile, java,
        privatekey, product_source, two_solution=False, number=None):
    """Store parametric data.

    Args:
        configfile (str): Location of PDL config file.
        eventsource (str): Network that originated the event.
        eventsourcecode (str): Event code.
        jarfile (str): Location of PDL jar file.
        java (str): Location of Java binary.
        privatekey (str): Location of PDL private key.
        product_source (str): Network contributing this product to ComCat.
        two_solution (bool): Is it a two solution finite fault product.
        number (int): Number of product (used for two plane solutions).
                Default is None.
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
    if two_solution:
        if number is not None:
            props['code'] += '_' + str(number)
        else:
            raise Exception('Number (model number) to delete must be specified.')
    props['type'] = 'finite-fault'
    sender = PDLSender(properties=props)
    msg = sender.cancel()
    return (msg)

def get_fault(eventsource, eventsourcecode, comcat_host='earthquake.usgs.gov',
        two_model=False, write_directory=None):
    """Retrieve the latest finite_fault data for a given event.
    Args:
        eventsource (str): Network that originated the event.
        eventsourcecode (str): Event code from network that originated
                               the event.
        comcat_host (str): (for testing) Specify an alternate comcat host.
    Returns:
        Dictionary data structure containing parametric data for event.
    """
    eventid = eventsource + eventsourcecode
    try:
        detail = get_event_by_id(eventid, host=comcat_host)
    except Exception as e:
        raise(e)
    if not detail.hasProduct(PRODUCT_TYPE):
        raise Exception('Event %r has no finite-fault product.' % eventid)
    if two_model:
        mod1 = ''
        mod2 = ''
        for prod in detail._jdict['properties']['products'][PRODUCT_TYPE]:
            if prod['code'].endswith('_1'):
                if mod1 == '':
                    latest_time1 = get_date(prod['updateTime'])
                if get_date(prod['updateTime']) >= latest_time1:
                    latest_time1 = get_date(prod['updateTime'])
                    mod1 = Product('finite-fault', VersionOption.LAST, prod)
            elif prod['code'].endswith('_2'):
                if mod2 == '':
                    latest_time2 = get_date(prod['updateTime'])
                if get_date(prod['updateTime']) >= latest_time2:
                    latest_time2 = get_date(prod['updateTime'])
                    mod2 = Product('finite-fault', VersionOption.LAST, prod)
        if mod1 == '' or mod2 == '':
            raise Exception('Two models were not found for this finite fault '
                    'product %r' % eventid)
    else:
        mod1 = detail.getProducts(PRODUCT_TYPE,  version=VersionOption.LAST)[0]

    if write_directory is not None:
        now = datetime.datetime.utcnow()
        date_str = now.strftime(TIMEFMT.replace(':', '_').replace('.%f', ''))
        if two_model:
            dir1 = os.path.join(write_directory,
                    eventid + '_1_' + date_str)
            dir2 = os.path.join(write_directory,
                    eventid + '_2_' + date_str)
            if not os.path.exists(dir1):
                os.makedirs(dir1, exist_ok=True)
            if not os.path.exists(dir2):
                os.makedirs(dir2, exist_ok=True)
            for file1, file2 in zip(mod1.contents, mod1.contents):
                filename1 = os.path.join(dir1, os.path.basename(file1))
                filename2 = os.path.join(dir2, os.path.basename(file1))
                mod1.getContent(file1, filename1)
                mod2.getContent(file2, filename2)
        else:
            dir = os.path.join(write_directory, eventid + '_' + date_str)
            if not os.path.exists(dir):
                os.makedirs(dir, exist_ok=True)
            for file in mod1.contents:
                filename = os.path.join(dir, os.path.basename(file))
                mod1.getContent(file, filename)


def get_date(milliseconds):
    seconds = milliseconds / 1000
    sub_seconds  = (milliseconds % 1000.0) / 1000.0
    date = datetime.datetime.fromtimestamp(seconds + sub_seconds)
    return date


if __name__ == '__main__':
    from product.constants import BASE_PDL_FOLDER, CFG, JAR, JAVA, PRIVATEKEY
    delete_fault(CFG, 'us', '1000dyad', JAR, JAVA,
            PRIVATEKEY, 'us', two_solution=False, number=None)
