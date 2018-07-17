#!/usr/bin/env python

import subprocess
import os.path


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
    # TEST for sending
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    indir = os.path.join(homedir, '..', 'data', 'timeseries')
    send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
    eventid = '100dyad'
    try:
        cmd = '%s %s' % (send_product, indir)
        res, stdout, stderr = get_command_output(cmd)
        if not res:
            raise AssertionError(
                'sendproduct command %s failed with errors "%s"' % (cmd,
                        stderr))
        print(stdout)
    except Exception as e:
        raise(e)

    # TEST for creation of files
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    indir = os.path.join(homedir, '..', 'data', 'timeseries')
    send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
    eventid = '100dyad'
    try:
        cmd = '%s %s -c' % (send_product, indir)
        res, stdout, stderr = get_command_output(cmd)
        if not res:
            raise AssertionError(
                'sendproduct command %s failed with errors "%s"' % (cmd,
                        stderr))
    except Exception as e:
        raise(e)


if __name__ == '__main__':
    test_sendproduct()
