"""
py.test module for unit testing the linearity step.
"""

from . import linearity_utils

import os
import ConfigParser

from astropy.io import fits
import pytest

# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

@pytest.fixture(scope="module")
def input_hdul(request, config):
    if  config.has_option("linearity", "input_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("linearity", "input_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs linearity input_file")

@pytest.fixture(scope="module")
def output_hdul(request, config):
    if  config.has_option("linearity", "output_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("linearity", "output_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs linearity output_file")

@pytest.fixture(scope="module")
def reference_hdul(output_hdul, config):
    CRDS = '/grp/crds/cache/references/jwst/'
    ref_file = CRDS+output_hdul[0].header['R_LINEAR'][7:]
    return fits.open(ref_file)

# Unit Tests

def test_linearity_correction(output_hdul, reference_hdul, input_hdul):
    assert linearity_utils.linearity_correction(output_hdul, reference_hdul, input_hdul)

def test_pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    assert linearity_utils.pixeldq_propagation(output_hdul, reference_hdul, input_hdul)
