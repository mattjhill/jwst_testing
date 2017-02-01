"""
py.test module for unit testing the dq_init step.
"""

from . import dq_init_utils

import os
import ConfigParser

from astropy.io import fits
import pytest

# Set up the fixtures needed for all of the tests, i.e. open up all of the FITS files

@pytest.fixture(scope="module")
def input_hdul(request, config):
    if  config.has_option("dq_init", "input_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("dq_init", "input_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs dq_init input_file")

@pytest.fixture(scope="module")
def output_hdul(request, config):
    if  config.has_option("dq_init", "output_file"):
        curdir = os.getcwd()
        config_dir = os.path.dirname(request.config.getoption("--config_file"))
        os.chdir(config_dir)
        hdul = fits.open(config.get("dq_init", "output_file"))
        os.chdir(curdir)
        return hdul
    else:
        pytest.skip("needs dq_init output_file")

@pytest.fixture(scope="module")
def reference_hdul(output_hdul, config):
    CRDS = '/grp/crds/cache/references/jwst/'
    ref_file = CRDS+output_hdul[0].header['R_MASK'][7:]
    return fits.open(ref_file)


# Unit Tests

def test_pixeldq_ext_exists(output_hdul):
    assert dq_init_utils.pixeldq_ext_exists(output_hdul)

def test_groupdq_vals_all_zero(output_hdul):
    assert dq_init_utils.groupdq_vals_all_zero(output_hdul)

def test_err_ext_exists(output_hdul):
    assert dq_init_utils.err_ext_exists(output_hdul)

def test_err_vals_all_zero(output_hdul):
    assert dq_init_utils.err_vals_all_zero(output_hdul)

def test_pixeldq_propagation(output_hdul, reference_hdul):
    assert dq_init_utils.pixeldq_propagation(output_hdul, reference_hdul)
