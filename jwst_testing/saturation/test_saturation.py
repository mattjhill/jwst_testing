"""
py.test module for unit testing the saturation step.
"""

from . import saturation_utils

import os
import ConfigParser

from astropy.io import fits
import pytest

# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

@pytest.fixture(scope="module")
def input_hdul(request, config):
    if  config.has_option("saturation", "input_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("saturation", "input_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs saturation input_file")

@pytest.fixture(scope="module")
def output_hdul(request, config):
    if  config.has_option("saturation", "output_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("saturation", "output_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs saturation output_file")

@pytest.fixture(scope="module")
def reference_hdul(output_hdul, config):
    CRDS = '/grp/crds/cache/references/jwst/'
    ref_file = CRDS+output_hdul[0].header['R_SATURA'][7:]
    return fits.open(ref_file)

# Unit Tests

def test_groupdq_flagging(output_hdul, reference_hdul):
    assert saturation_utils.groupdq_flagging(output_hdul, reference_hdul)

def test_saturation_pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    assert saturation_utils.pixeldq_propagation(output_hdul, reference_hdul, input_hdul)
