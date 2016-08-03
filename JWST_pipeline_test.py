"""
This module contains the front end interface for the JWST Calibration
Pipeline validation
"""

import sys
import pytest
import ConfigParser

def get_config_file_names(config):
    """
    Reads file names for each step from set_values.cfg and runs them through
    pytest if its value is not None
    """
<<<<<<< HEAD
    parser.add_argument("input_file", help="the file to be put through pipeline testing")
    parser.add_argument("expected_output_file", help="once the input file goes through the pipeline, it will be compared to this file for validation")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("--dq_init_file", action="store", help="output of the dq_init step of the pipeline", default=None)
    parser.add_argument("--sat_file", action="store", help="output of the saturation step of the pipeline", default=None)
=======
    config.read("set_values.cfg")
    dq_init_file = config.get("dq_init","dq_init_file")
    sat_file = config.get("saturation","sat_file")
    ipc_file = config.get("ipc","ipc_file")
    superbias_file = config.get("superbias","superbias_file")
    refpix_file = config.get("refpix","refpix_file")
    reset_file = config.get("reset","reset_file")
    lastframe_file = config.get("lastframe","lastframe_file")
    linearity_file = config.get("linearity","linearity_file")
    dark_current_file = config.get("dark_current","dark_current_file")
    jump_file = config.get("jump","jump_file")
    ramp_fit_file = config.get("ramp_fit","ramp_fit_file")
    pytest.main(['-v', '--dq_init_file='+dq_init_file, '--sat_file='+sat_file,
        '--ipc_file='+ipc_file, '--superbias_file='+superbias_file,
        '--refpix='+refpix_file, '--lastframe='+lastframe_file,
        '--linearity_file='+linearity_file, '--dark_current_file='+ dark_current_file,
        '--jump_file='+jump_file, '--ramp_fit_file='+ramp_fit_file])
>>>>>>> master

# def check_if_input_fits(args):
#     """
#     Checks to make sure that the FITS file being input contains the appropriate
#     headers, which are SCI and PRIMARY
#     """
#     try:
#         hdulist = fits.open(args.input_file)
#         if hdulist['SCI'] and hdulist['PRIMARY']:
#             return True
#     except IOError:
#         print("ERROR, {} not a FITS file".format(args.input_file))
#     return False

<<<<<<< HEAD
def get_file_names(args):
    """
    Takes arguments from the command line in order of <input> <expected output>
    and returns the names of both files; to be called by the testing suite file
    """
    input_file = args.input_file
    expected_output_file = args.expected_output_file
    print ("Running tests now...")
    return (input_file, expected_output_file)

def start_tests(args):
    """
    Calls pytest in order to begin testing the validity of the pipeline using
    the input_file and expected_output_file
    """
    pytest_args = ['-v']
    if args.dq_init_file:
        pytest_args.append('--dq_init_file='+args.dq_init_file)
    if args.sat_file:
        pytest_args.append('--sat_file='+args.sat_file)

    pytest_args.append('test_pipeline.py')
    pytest.main(pytest_args)

parser = argparse.ArgumentParser()
args = setup_parser(parser)
# (input_file, expected_output_file) = get_file_names(args)
start_tests(args)
# print (input_file, expected_output_file)
=======

config = ConfigParser.ConfigParser()
get_config_file_names(config)
# check_for_fits = check_if_input_fits(args)
# if check_for_fits:
#     start_tests(input_file, instrument_team)
#     print ("Input file: {} \nExpected output file: {} \nInstrument Team: {}"
#         .format(input_file, expected_output_file,instrument_team))
# else:
#     print ("Input file {} is not in the correct FITS format".format(input_file))
>>>>>>> master
