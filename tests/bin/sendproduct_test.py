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
        # TEST for sending basic
        homedir = os.path.dirname(os.path.abspath(
            __file__))  # where is this script?
        indir = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
        send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
        eventid = '100dyad_test'
        net = 'us'
        source = 'us'
        try:
            cmd = f'{send_product} {net} {source} {eventid} {indir} 1 -d'
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
        except Exception as e:
            raise(e)

        stdout = stdout.decode('utf8').split(
            "command: ")[-1].split('--privateKey')[0].split('ProductClient.jar ')[-1]
        target_stdout = ('--send --status=UPDATE '
                         '--source=us --type=finite-fault --code=us10'
                         '0dyad_test_1 --eventsource=us --eventsource'
                         'code=100dyad_test --property-version=1 --property-eventsourcecode'
                         '="100dyad_test" --property-eventsource="us" '
                         '--property-number-pwaves=42 --property-number'
                         '-shwaves=28 --property-number-longwaves=75 --'
                         'property-latitude=19.3700 --property-longitude'
                         '=-155.0300 --property-location="19.3700, -155.'
                         '0300" --property-derived-magnitude=6.8800 --pro'
                         'perty-scalar-moment=27660745000000000000.0000 --'
                         'property-derived-magnitude-type="Mw" --property-'
                         'depth=8.0000 --property-eventtime="2018-05-04T00'
                         ':00:00.000000Z" --property-average-rise-time="2.13"'
                         ' --property-average-rupture-velocity="1.2" --property'
                         '-hypocenter-x=54.0000 --property-hypocenter-z=11.2500'
                         ' --property-maximum-frequency=1.0000 --property-minimum'
                         '-frequency=0.0020 --property-model-dip=20.0000 --property'
                         '-model-length=108.0000 --property-model-rake=114.0000 '
                         '--property-model-strike=240.0000 --property-model-top='
                         '4.1500 --property-model-width=25.0000 --property-time-'
                         'windows=5 --property-velocity-function="Asymetriccosine"'
                         ' --property-segments=1 --property-subfault-1-width=13.0777'
                         ' --property-subfault-1-length=64.5265 --property-subfault'
                         '-1-area=843.8599 --property-segment-1-strike=240.0000 --'
                         'property-segment-1-dip=20.0000 --property-maximum-slip=2.'
                         '6860 --property-maximum-rise=4.0000 --property-crustal-'
                         'model="1D crustal model interpolated from CRUST2.0 (Bassin'
                         ' et al., 2000)." --property-model-number=1 --property-review'
                         '-status="reviewed"  ')
        assert stdout == target_stdout

        # TEST for sending basic
        print("Testing suppressing model number...")
        homedir = os.path.dirname(os.path.abspath(
            __file__))  # where is this script?
        indir = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
        send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
        eventid = '100dyad_test'
        net = 'us'
        source = 'us'
        try:
            cmd = f'{send_product} {net} {source} {eventid} {indir} 1 -d -s'
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
        except Exception as e:
            raise(e)

        stdout = stdout.decode('utf8').split(
            "command: ")[-1].split('--privateKey')[0].split('ProductClient.jar ')[-1]
        target_stdout = ('--send --status=UPDATE '
                         '--source=us --type=finite-fault --code=us10'
                         '0dyad_test --eventsource=us --eventsource'
                         'code=100dyad_test --property-version=1 --property-eventsourcecode'
                         '="100dyad_test" --property-eventsource="us" '
                         '--property-number-pwaves=42 --property-number'
                         '-shwaves=28 --property-number-longwaves=75 --'
                         'property-latitude=19.3700 --property-longitude'
                         '=-155.0300 --property-location="19.3700, -155.'
                         '0300" --property-derived-magnitude=6.8800 --pro'
                         'perty-scalar-moment=27660745000000000000.0000 --'
                         'property-derived-magnitude-type="Mw" --property-'
                         'depth=8.0000 --property-eventtime="2018-05-04T00'
                         ':00:00.000000Z" --property-average-rise-time="2.13"'
                         ' --property-average-rupture-velocity="1.2" --property'
                         '-hypocenter-x=54.0000 --property-hypocenter-z=11.2500'
                         ' --property-maximum-frequency=1.0000 --property-minimum'
                         '-frequency=0.0020 --property-model-dip=20.0000 --property'
                         '-model-length=108.0000 --property-model-rake=114.0000 '
                         '--property-model-strike=240.0000 --property-model-top='
                         '4.1500 --property-model-width=25.0000 --property-time-'
                         'windows=5 --property-velocity-function="Asymetriccosine"'
                         ' --property-segments=1 --property-subfault-1-width=13.0777'
                         ' --property-subfault-1-length=64.5265 --property-subfault'
                         '-1-area=843.8599 --property-segment-1-strike=240.0000 --'
                         'property-segment-1-dip=20.0000 --property-maximum-slip=2.'
                         '6860 --property-maximum-rise=4.0000 --property-crustal-'
                         'model="1D crustal model interpolated from CRUST2.0 (Bassin'
                         ' et al., 2000)." --property-review'
                         '-status="reviewed"  ')
        assert stdout == target_stdout

        # TEST for sending basic
        print("Testing custom comment...")
        homedir = os.path.dirname(os.path.abspath(
            __file__))  # where is this script?
        indir = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
        send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
        eventid = '100dyad_test'
        net = 'us'
        source = 'us'
        try:
            cmd = (f'{send_product} {net} {source} {eventid} {indir} 1 -d -s'
                   ' -c "comment here"')
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
        except Exception as e:
            raise(e)

        stdout = stdout.decode('utf8').split(
            "command: ")[-1].split('--privateKey')[0].split('ProductClient.jar ')[-1]
        target_stdout = ('--send --status=UPDATE '
                         '--source=us --type=finite-fault --code=us10'
                         '0dyad_test --eventsource=us --eventsource'
                         'code=100dyad_test --property-version=1 --property-eventsourcecode'
                         '="100dyad_test" --property-eventsource="us" '
                         '--property-number-pwaves=42 --property-number'
                         '-shwaves=28 --property-number-longwaves=75 --'
                         'property-latitude=19.3700 --property-longitude'
                         '=-155.0300 --property-location="19.3700, -155.'
                         '0300" --property-derived-magnitude=6.8800 --pro'
                         'perty-scalar-moment=27660745000000000000.0000 --'
                         'property-derived-magnitude-type="Mw" --property-'
                         'depth=8.0000 --property-eventtime="2018-05-04T00'
                         ':00:00.000000Z" --property-average-rise-time="2.13"'
                         ' --property-average-rupture-velocity="1.2" --property'
                         '-hypocenter-x=54.0000 --property-hypocenter-z=11.2500'
                         ' --property-maximum-frequency=1.0000 --property-minimum'
                         '-frequency=0.0020 --property-model-dip=20.0000 --property'
                         '-model-length=108.0000 --property-model-rake=114.0000 '
                         '--property-model-strike=240.0000 --property-model-top='
                         '4.1500 --property-model-width=25.0000 --property-time-'
                         'windows=5 --property-velocity-function="Asymetriccosine"'
                         ' --property-segments=1 --property-subfault-1-width=13.0777'
                         ' --property-subfault-1-length=64.5265 --property-subfault'
                         '-1-area=843.8599 --property-segment-1-strike=240.0000 --'
                         'property-segment-1-dip=20.0000 --property-maximum-slip=2.'
                         '6860 --property-maximum-rise=4.0000 --property-crustal-'
                         'model="1D crustal model interpolated from CRUST2.0 (Bassin'
                         ' et al., 2000)." --property-comment="comment here" --property-review'
                         '-status="reviewed"  ')
        assert stdout == target_stdout

        # TEST for sending basic
        print("Testing custom crustal model...")
        homedir = os.path.dirname(os.path.abspath(
            __file__))  # where is this script?
        indir = os.path.join(homedir, '..', 'data', 'products', '1000dyad')
        send_product = os.path.join(homedir, '..', '..', 'bin', 'sendproduct')
        eventid = '100dyad_test'
        net = 'us'
        source = 'us'
        try:
            cmd = (f'{send_product} {net} {source} {eventid} {indir} 1 -d -s'
                   ' -c "comment here" -m "new crustal model" -v 3')
            res, stdout, stderr = get_command_output(cmd)
            if not res:
                raise AssertionError(
                    'sendproduct command %s failed with errors "%s"' % (cmd,
                                                                        stderr))
        except Exception as e:
            raise(e)

        stdout = stdout.decode('utf8').split(
            "command: ")[-1].split('--privateKey')[0].split('ProductClient.jar ')[-1]
        target_stdout = ('--send --status=UPDATE '
                         '--source=us --type=finite-fault --code=us10'
                         '0dyad_test --eventsource=us --eventsource'
                         'code=100dyad_test --property-version=3 --property-eventsourcecode'
                         '="100dyad_test" --property-eventsource="us" '
                         '--property-number-pwaves=42 --property-number'
                         '-shwaves=28 --property-number-longwaves=75 --'
                         'property-latitude=19.3700 --property-longitude'
                         '=-155.0300 --property-location="19.3700, -155.'
                         '0300" --property-derived-magnitude=6.8800 --pro'
                         'perty-scalar-moment=27660745000000000000.0000 --'
                         'property-derived-magnitude-type="Mw" --property-'
                         'depth=8.0000 --property-eventtime="2018-05-04T00'
                         ':00:00.000000Z" --property-average-rise-time="2.13"'
                         ' --property-average-rupture-velocity="1.2" --property'
                         '-hypocenter-x=54.0000 --property-hypocenter-z=11.2500'
                         ' --property-maximum-frequency=1.0000 --property-minimum'
                         '-frequency=0.0020 --property-model-dip=20.0000 --property'
                         '-model-length=108.0000 --property-model-rake=114.0000 '
                         '--property-model-strike=240.0000 --property-model-top='
                         '4.1500 --property-model-width=25.0000 --property-time-'
                         'windows=5 --property-velocity-function="Asymetriccosine"'
                         ' --property-segments=1 --property-subfault-1-width=13.0777'
                         ' --property-subfault-1-length=64.5265 --property-subfault'
                         '-1-area=843.8599 --property-segment-1-strike=240.0000 --'
                         'property-segment-1-dip=20.0000 --property-maximum-slip=2.'
                         '6860 --property-maximum-rise=4.0000 --property-crustal-'
                         'model="new crustal model" --property-comment="comment '
                         'here" --property-review'
                         '-status="reviewed"  ')
        assert stdout == target_stdout


if __name__ == '__main__':
    test_sendproduct()
