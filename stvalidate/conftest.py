import pytest
import ConfigParser

def pytest_addoption(parser):
    """
    Specifies the files used for certain tests
    """
    parser.addoption("--config_file", action="store",
        help="specifies the file used for the dq_init test")

@pytest.fixture(scope="module")
def config(request):
    config = ConfigParser.ConfigParser()
    config.read(request.config.getoption("--config_file"))
    return config