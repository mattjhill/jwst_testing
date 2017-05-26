from collections import OrderedDict

import pytest
from datetime import datetime
from py.xml import html

import jwst
from jwst import datamodels
import crds
from astropy.io import fits

############# Fixtures ##################

@pytest.fixture(scope='session', autouse=True)
def open_model(request):
    """
    hack to make a datamodel globally available and persistent throughout 
    the test suite
    """
    request.config.model = datamodels.open(request.config.getoption('uncal'))

@pytest.fixture(scope='module', autouse=True)
def input_model(request):
    """
    make the model before any step is run accessible to module tests.
    autouse = True ensures the instance is returned before the step test is run
    """
    return request.config.model

@pytest.fixture(scope='module')
def output_model(request):
    """
    make the model after any step is run accessible to module tests
    the step test must be run before any test using this fixture
    """
    return request.config.model

############### Hooks ###################

def pytest_addoption(parser):
    parser.addoption('--uncal', action='store', help='the uncalibrated level 1B file')

def get_keyword(header, keyword):
    if keyword in header:
        return header[keyword]
    else:
        return ''

def pytest_configure(config):
    config._metadata['jwst'] = jwst.__version__
    config._metadata['crds_context'] = crds.heavy_client.get_processing_mode('jwst')[1]

    header = fits.getheader(config.getoption('uncal'))
    config._modelmeta = OrderedDict()
    config._modelmeta['meta.observation.template'] = get_keyword(header, 'TEMPLATE')
    config._modelmeta['meta.instrument.name'] = get_keyword(header, 'INSTRUME')
    config._modelmeta['meta.instrument.detector'] = get_keyword(header, 'DETECTOR')
    config._modelmeta['meta.instrument.filter'] = get_keyword(header, 'FILTER')
    config._modelmeta['meta.instrument.pupil'] = get_keyword(header, 'PUPIL')
    config._modelmeta['meta.instrument.grating'] = get_keyword(header, 'GRATING')
    config._modelmeta['meta.instrument.channel'] = get_keyword(header, 'CHANNEL')
    config._modelmeta['meta.instrument.band'] = get_keyword(header, 'BAND')

    config._modelmeta['meta.exposure.type'] = get_keyword(header, 'EXP_TYPE')
    config._modelmeta['meta.exposure.readpatt'] = get_keyword(header, 'READPATT')
    config._modelmeta['meta.exposure.nints'] = get_keyword(header, 'NINTS')
    config._modelmeta['meta.exposure.ngroups'] = get_keyword(header, 'NGROUPS')

    config._modelmeta['meta.subarray.name'] = get_keyword(header, 'SUBARRAY')
    config._modelmeta['meta.subarray.xstart'] = get_keyword(header, 'SUBSTRT1')
    config._modelmeta['meta.subarray.xsize'] = get_keyword(header, 'SUBSIZE1')
    config._modelmeta['meta.subarray.ystart'] = get_keyword(header, 'SUBSTRT2')
    config._modelmeta['meta.subarray.ysize'] = get_keyword(header, 'SUBSIZE2')


def pytest_runtest_setup(item):
    stepfailed = getattr(item, "_stepfailed", None)
    if stepfailed is not None:
        pytest.skip("The last pipeline step failed")

    uncal_marker = item.get_marker("needs_uncal")
    if uncal_marker is not None:
        if item.config.getoption("uncal") is None:
            pytest.skip("test requires uncal input file")

def pytest_runtest_makereport(item, call):
    if "step" in item.keywords:
        if call.excinfo is not None:
            item._stepfailed = True

def pytest_runtest_teardown(item, nextitem):
    stepfailed = getattr(item, "_stepfailed", None)
    if stepfailed is not None and nextitem is not None:
        nextitem._stepfailed = item

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(0, html.th('Time', class_='sortable time', col='time'))
    cells.insert(2, html.th('Test', class_='sortable', col='shortname'))
    cells.pop()
    cells.pop(-2)

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(0, html.td(datetime.utcnow(), class_='col-time'))
    cells.insert(2, html.td(report.nodeid.split('/')[-1], class_='col-time'))
    cells.pop()
    cells.pop(-2)
