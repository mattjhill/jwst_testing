"""
py.test module for unit testing the superbias step.
"""

from . import superbias_utils

import os
import ConfigParser

from astropy.io import fits
import pytest

# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

@pytest.fixture(scope="module")
def input_hdul(request, config):
    if  config.has_option("superbias", "input_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("superbias", "input_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs superbias input_file")

@pytest.fixture(scope="module")
def output_hdul(request, config):
    if  config.has_option("superbias", "output_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("superbias", "output_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs superbias output_file")

@pytest.fixture(scope="module")
def reference_hdul(output_hdul, config):
    CRDS = '/grp/crds/cache/references/jwst/'
    ref_file = CRDS+output_hdul[0].header['R_BIAS'][7:]
    return fits.open(ref_file)

# Unit Tests

def test_superbias_subtraction(output_hdul, reference_hdul, input_hdul):
    assert superbias_subtraction(output_hdul, reference_hdul, input_hdul)

def test_pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    assert pixeldq_propagation(output_hdul, reference_hdul, input_hdul)
    