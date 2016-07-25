"""
Configuration file for py.test
"""

import pytest

def pytest_addoption(parser):
    parser.addoption("--skip_dq_init", action="store_true", 
        help="skip the dq_init step tests")
    parser.addoption("--fname", action="store", 
        help="fname: input fits file to be validated")

@pytest.fixture(scope='class')
def fname(request):
    return request.config.getoption("--fname")

def pytest_runtest_setup(item):
    if 'dq_init' in item.keywords and item.config.getvalue("--skip_dq_init"):
        pytest.skip("skipping dq_init tests")