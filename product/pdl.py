# third party imports
from impactutils.transfer.pdlsender import PDLSender


def store_fault (configfile, eventsource, eventsourcecode, jarfile, java,
        pdlfolder, privatekey, product_source, properties, number=None):
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
    props['source'] = 'us'
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
