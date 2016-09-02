"""
Configuration file for py.test
"""

import pytest
from astropy.io import fits

def pytest_addoption(parser):
    """
    Specifies the files used for certain tests
    """
    parser.addoption("--dq_init_file", action="store",
        help="specifies the file used for the dq_init test")
    parser.addoption("--sat_file", action="store",
        help="specifies the file used for the saturationtest")
    parser.addoption("--ipc_file", action="store",
        help="specifies the file used for the ipc test")
    parser.addoption("--superbias_file", action="store",
        help="specifies the file used for the superbias test")
    parser.addoption("--refpix_file", action="store",
        help="specifies the file used for the refpix test")
    parser.addoption("--reset_file", action="store",
        help="specifies the file used for the reset test")
    parser.addoption("--lastframe_file", action="store",
        help="specifies the file used for the lastframe test")
    parser.addoption("--linearity_file", action="store",
        help="specifies the file used for the linearity test")
    parser.addoption("--dark_current_file", action="store",
        help="specifies the file used for the dark current test")
    parser.addoption("--jump_file", action="store",
        help="specifies the file used for the jump test")
    parser.addoption("--ramp_fit_file", action="store",
        help="specifies the file used for the ramp fit test")

    # 2B Image Steps

    parser.addoption("--assign_wcs_file", action="store",
        help="specifies the file used for the assign_wcs test")
    parser.addoption("--flat_field_file", action="store",
        help="specifies the file used for the flat_field test")
    parser.addoption("--persistence_file", action="store",
        help="specifies the file used for the persistence test")
    parser.addoption("--emission_file", action="store",
        help="specifies the file used for the emission test")
    parser.addoption("--photom_file", action="store",
        help="specifies the file used for the photom test")

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
    Takes the --sat_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    sat_file = request.config.getoption("--sat_file")
    return fits.open(sat_file)

@pytest.fixture
def ipc_hdu(request):
    """
    Takes the --ipc_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    ipc_file = request.config.getoption("--ipc_file")
    return fits.open(ipc_file)

@pytest.fixture()
def superbias_hdu(request):
    """
    Takes the --superbias_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    superbias_file = request.config.getoption("--superbias_file")
    return fits.open(superbias_file)

@pytest.fixture
def refpix_hdu(request):
    """
    Takes the --refpix_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    refpix_file = request.config.getoption("--refpix_file")
    return fits.open(refpix_file)

@pytest.fixture()
def reset_hdu(request):
    """
    Takes the --reset_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    reset_file = request.config.getoption("--reset_file")
    return fits.open(reset_file)

@pytest.fixture
def lastframe_hdu(request):
    """
    Takes the --lastframe_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    lastframe_file = request.config.getoption("--lastframe_file")
    return fits.open(lastframe_file)

@pytest.fixture(scope="module")
def linearity_hdu(request):
    """
    Takes the --linearity_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    linearity_file = request.config.getoption("--linearity_file")
    return fits.open(linearity_file)

@pytest.fixture()
def dark_current_hdu(request):
    """
    Takes the --dark_current_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    dark_current_file = request.config.getoption("--dark_current_file")
    return fits.open(dark_current_file)

@pytest.fixture
def jump_hdu(request):
    """
    Takes the --jump_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    jump_file = request.config.getoption("--jump_file")
    return fits.open(jump_file)

@pytest.fixture()
def ramp_fit_hdu(request):
    """
    Takes the --ramp_fit_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    ramp_fit_file = request.config.getoption("--ramp_fit_file")
    return fits.open(ramp_fit_file)

@pytest.fixture()
def assign_wcs_hdu(request):
    """
    Takes the --assign_wcs_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    assign_wcs_file = request.config.getoption("--assign_wcs_file")
    return fits.open(assign_wcs_file)

@pytest.fixture()
def flat_field_hdu(request):
    """
    Takes the --flat_field_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    flat_field_file = request.config.getoption("--flat_field_file")
    return fits.open(flat_field_file)

@pytest.fixture()
def persistence_hdu(request):
    """
    Takes the --persistence_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    persistence_file = request.config.getoption("--persistence_file")
    return fits.open(persistence_file)

@pytest.fixture()
def emission_hdu(request):
    """
    Takes the --emission_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    emission_file = request.config.getoption("--emission_file")
    return fits.open(emission_file)

@pytest.fixture()
def photom_hdu(request):
    """
    Takes the --photom_file cmd line arg and opens the fits file
    this allows hdulist to be accessible by all test in the class.
    """
    photom_file = request.config.getoption("--photom_file")
    return fits.open(photom_file)
    
def pytest_runtest_setup(item):

    if 'dq_init' in item.keywords and item.config.getvalue("--dq_init_file") == 'None':
        pytest.skip("requires a dq_init_file")
    if 'saturation' in item.keywords and item.config.getvalue("--sat_file") == 'None':
        pytest.skip("requires a sat_file")
    if 'ipc' in item.keywords and item.config.getvalue("--ipc_file") == 'None':
        pytest.skip("requires a ipc_file")
    if 'superbias' in item.keywords and item.config.getvalue("--superbias_file") == 'None':
        pytest.skip("requires a superbias_file")
    if 'refix' in item.keywords and item.config.getvalue("--refpix_file") == 'None':
        pytest.skip("requires a refpix_file")
    if 'reset' in item.keywords and item.config.getvalue("--reset_file") == 'None':
        pytest.skip("requires a reset_file")
    if 'lastframe' in item.keywords and item.config.getvalue("--lastframe_file") == 'None':
        pytest.skip("requires a lastframe_file")
    if 'linearity' in item.keywords and item.config.getvalue("--linearity_file") == 'None':
        pytest.skip("requires a linearity_file")
    if 'dark_current' in item.keywords and item.config.getvalue("--dark_current_file") == 'None':
        pytest.skip("requires a dark_current_file")
    if 'jump' in item.keywords and item.config.getvalue("--jump_file") == 'None':
        pytest.skip("requires a jump_file")
    if 'ramp_fit' in item.keywords and item.config.getvalue("--ramp_fit_file") == 'None':
        pytest.skip("requires a ramp_fit_file")

    if 'assign_wcs' in item.keywords and item.config.getvalue("--assign_wcs_file") == 'None':
        pytest.skip("requires an assign_wcs_file")
    if 'flat_field' in item.keywords and item.config.getvalue("--flat_field_file") == 'None':
        pytest.skip("requires a flat_field_file")
    if 'persistence' in item.keywords and item.config.getvalue("--persistence_file") == 'None':
        pytest.skip("requires a persistence_file")
    if 'emission' in item.keywords and item.config.getvalue("--emission_file") == 'None':
        pytest.skip("requires a emission_file")
    if 'photom' in item.keywords and item.config.getvalue("--photom_file") == 'None':
        pytest.skip("requires a photom_file")
