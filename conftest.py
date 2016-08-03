"""
Configuration file for py.test
"""

import pytest
from astropy.io import fits

def pytest_addoption(parser):
    """
    Adds options for the command line flags from py.test

    Options
    =======

    --skip_dq_init  -  skips the test associated with the dq_init step
    --fname - the path to the file to perform the test on
    """
    # parser.addoption("--skip_dq_init", action="store_true", 
    #     help="skip the dq_init step tests")
    parser.addoption("--dq_init_file", action="store", default=None,
        help="dq_init_file: output of dq_init step to be validated")
    parser.addoption("--sat_file", action="store", default=None,
        help="sat_file: output of saturation step to be validated")

@pytest.fixture
def dq_init_hdu(request):
        """
        Takes the --dqint_file cmd line arg and opens the fits file
        this allows hdulist to be accessible by all test in the class.
        """
        dq_init_file = request.config.getoption("--dq_init_file")
        return fits.open(dq_init_file)

@pytest.fixture()
def sat_hdu(request):
    """
    fixture to get the path input with --fname. The input string is now
    available as fname in the the test module
    """
    sat_file = request.config.getoption("--sat_file")
    return fits.open(sat_file)

def pytest_runtest_setup(item):
    
    if 'dq_init' in item.keywords and item.config.getvalue("--dq_init_file") is None:
        pytest.skip("skipping dq_init tests")
    if 'saturation' in item.keywords and item.config.getvalue("--sat_file") is None:
        pytest.skip("skipping dq_init tests")
