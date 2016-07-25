"""
This module contains the front end interface for the JWST Calibration
Pipeline validation
"""

import sys
from PIL import Image
import glob
from astropy.io import fits
import pytest
import argparse

def setup_parser(parser):
    """
    Establishes the arguments this application will look for, including -h for
    help and the input_file and expected_output_file
    """
    parser.add_argument("input_file", help="the file to be put through pipeline testing")
    parser.add_argument("expected_output_file", help="once the input file goes through the pipeline, it will be compared to this file for validation")
    parser.add_argument("-v", "--verbosity", action="count", default=0)

    args = parser.parse_args()
    return args

def get_file_names(args):
    """
    Takes arguments from the command line in order of <input> <expected output>
    and returns the names of both files; to be called by the testing suite file
    """
    input_file = args.input_file
    expected_output_file = args.expected_output_file
    print ("Running tests now...")
    return (input_file, expected_output_file)

def start_tests(input_file):
    """
    Calls pytest in order to begin testing the validity of the pipeline using
    the input_file and expected_output_file
    """
    pytest.main(['-v', '--fname='+input_file])

parser = argparse.ArgumentParser()
args = setup_parser(parser)
(input_file, expected_output_file) = get_file_names(args)
start_tests(input_file)
print (input_file, expected_output_file)
