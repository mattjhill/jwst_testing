"""
This module contains the front end interface for the JWST Calibration
Pipeline validation
"""

import sys
import pytest
import ConfigParser
import argparse

def get_config_file_names(config,args):
    """
    Reads file names for each step from set_values.cfg and runs them through
    pytest if its value is not None
    """
    config.read(args.chosen_config)
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

    pytest_args = ['-v', 
        '--dq_init_file='+dq_init_file, 
        '--sat_file='+sat_file,
        '--ipc_file='+ipc_file, 
        '--superbias_file='+superbias_file,
        '--refpix_file='+refpix_file, 
        '--reset_file='+reset_file,
        '--lastframe_file='+lastframe_file,
        '--linearity_file='+linearity_file, 
        '--dark_current_file='+ dark_current_file,
        '--jump_file='+jump_file, 
        '--ramp_fit_file='+ramp_fit_file]

    # select specific tests if the option is set in the config file
    try:
        pytest_args.append('-k '+config.get("options","tests"))
    except ConfigParser.NoSectionError:
        pass

    # make sure only test_pipeline.py is used
    pytest_args.append('test_pipeline.py')  
    pytest.main(pytest_args)

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

parser = argparse.ArgumentParser()
parser.add_argument("chosen_config")
args = parser.parse_args()

config = ConfigParser.ConfigParser()
get_config_file_names(config,args)
# check_for_fits = check_if_input_fits(args)
# if check_for_fits:
#     start_tests(input_file, instrument_team)
#     print ("Input file: {} \nExpected output file: {} \nInstrument Team: {}"
#         .format(input_file, expected_output_file,instrument_team))
# else:
#     print ("Input file {} is not in the correct FITS format".format(input_file))
