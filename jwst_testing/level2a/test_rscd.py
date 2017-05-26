"""
py.test module for unit testing the rscd step.
"""

from jwst_testing.rscd import rscd_utils

import pytest
from jwst.rscd import RSCD_Step
from jwst.datamodels import RSCDModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def superbias_model(request):
    ref_path = request.config.model.meta.ref_file.rscd.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return RSCDModel(ref_path)

@pytest.fixture(scope='module')
def superbias_hdul(request):
    ref_path = request.config.model.meta.ref_file.rscd.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_rscd_step(request, input_model):
    request.config.model = RSCD_Step.call(input_model)

