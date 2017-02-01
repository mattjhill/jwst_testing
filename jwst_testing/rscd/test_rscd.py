"""
py.test module for unit testing the rscd step.
"""

from . import rscd_utils

import os
import ConfigParser

from astropy.io import fits
import pytest

# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

@pytest.fixture(scope="module")
def input_hdul(request, config):
    if  config.has_option("rscd", "input_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("rscd", "input_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs rscd input_file")

@pytest.fixture(scope="module")
def output_hdul(request, config):
    if  config.has_option("rscd", "output_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("rscd", "output_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs rscd output_file")

@pytest.fixture(scope="module")
def reference_hdul(output_hdul, config):
    CRDS = '/grp/crds/cache/references/jwst/'
    ref_file = CRDS+output_hdul[0].header['R_RSCD'][7:]
    return fits.open(ref_file)

# Unit Tests

def test_rscd_correction(input_hdul, reference_hdul, output_hdul):
    assert rscd_utils.rscd_correction(input_hdul, reference_hdul, output_hdul)

def test_rscd_pixeldq_propagation(input_hdul, reference_hdul, output_hdul):
    assert rscd_utils.pixeldq_propagation(input_hdul, reference_hdul, output_hdul)

