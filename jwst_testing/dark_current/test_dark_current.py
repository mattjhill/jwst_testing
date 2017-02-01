"""
py.test module for unit testing the dark_current step.
"""

from . import dark_current_utils

import os
import ConfigParser

from astropy.io import fits
import pytest

# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

@pytest.fixture(scope="module")
def input_hdul(request, config):
    if  config.has_option("dark_current", "input_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("dark_current", "input_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs dark_current input_file")

@pytest.fixture(scope="module")
def output_hdul(request, config):
    if  config.has_option("dark_current", "output_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("dark_current", "output_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs dark_current output_file")

@pytest.fixture(scope="module")
def reference_hdul(output_hdul, config):
    CRDS = '/grp/crds/cache/references/jwst/'
    ref_file = CRDS+output_hdul[0].header['R_DARK'][7:]
    return fits.open(ref_file)

# Unit Tests

def test_dark_current_subtraction(output_hdul, reference_hdul, input_hdul):
    assert dark_current_utils.dark_current_subtraction(output_hdul, reference_hdul, input_hdul)

def test_pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    assert dark_current_utils.pixeldq_propagation(output_hdul, reference_hdul, input_hdul)
