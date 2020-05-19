#!/usr/bin/env python

# stdlib imports
import os.path
import subprocess

# local imports
from product.constants import CFG


def get_command_output(cmd):
    """
    Method for calling external system command.

    Args:
        cmd: String command (e.g., 'ls -l', etc.).

    Returns:
        Three-element tuple containing a boolean indicating success or failure,
        the stdout from running the command, and stderr.
    """
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    stdout, stderr = proc.communicate()
    retcode = proc.returncode
    if retcode == 0:
        retcode = True
    else:
        retcode = False
    return (retcode, stdout, stderr)


def test_sendproduct():
    if os.path.exists(CFG):
        # TEST for sending
        homedir = os.path.dirname(os.path.abspath(
            __file__))  # where is this script?
        indir = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
        send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
        eventid = '100dyad_test'
        net = 'us'
        source = 'us'
        try:
            cmd = '%s %s %s %s %s -r' % (send_product, net, source,
                                         eventid, indir)
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
            print(stdout)
        except Exception as e:
            raise(e)

        # Send multiple products
        try:
            cmd = '%s %s %s %s %s -ffm2 %s -v 2 -r' % (send_product, net,
                                                       source, eventid, indir, indir)
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
            print(stdout)
        except Exception as e:
            raise(e)

        ndir1 = os.path.join(homedir, '..', 'data', 'products', '10004u1y_1')
        ndir2 = os.path.join(homedir, '..', 'data', 'products', '10004u1y_2')
        send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
        eventid = '10004u1y_test'
        net = 'us'
        source = 'us'
        try:
            cmd = '%s %s %s %s %s -ffm2 %s -r' % (send_product, net, source,
                                                  eventid, ndir1, ndir2)
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
            print(stdout)
        except Exception as e:
            raise(e)


if __name__ == '__main__':
    test_sendproduct()
