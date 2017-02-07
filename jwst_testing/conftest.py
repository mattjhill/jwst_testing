"""
py.test configuration for the *entire* test suite
"""

import pytest
import ConfigParser

def pytest_addoption(parser):
    """
    Specifies the files used for certain tests
    """
    parser.addoption("--config_file", action="store",
        help="specifies the file used for the dq_init test")
    parser.addoption("--gen_report", action="store_true",
        help="generate a report or not")
    
@pytest.fixture(scope="session")
def config(request):
    config = ConfigParser.ConfigParser()
    try:
        config.read(request.config.getoption("--config_file"))
    except:
        # skip tests that use the config file if one isn't specified
        pytest.skip("Must supply pipeline I/O with a config file.")

    return config