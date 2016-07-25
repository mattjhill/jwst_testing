"""
Configuration file for py.test
"""

import pytest

def pytest_addoption(parser):
    """
    Adds options for the command line flags from py.test

    Options
    =======

    --skip_dq_init  -  skips the test associated with the dq_init step
    --fname - the path to the file to perform the test on
    """
    parser.addoption("--skip_dq_init", action="store_true", 
        help="skip the dq_init step tests")
    parser.addoption("--fname", action="store", 
        help="fname: input fits file to be validated")

@pytest.fixture()
def fname(request):
    """
    fixture to get the path input with --fname. The input string is now
    available as fname in the the test module
    """
    return request.config.getoption("--fname")

def pytest_runtest_setup(item):
    
    if 'dq_init' in item.keywords and item.config.getvalue("--skip_dq_init"):
        pytest.skip("skipping dq_init tests")