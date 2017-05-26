"""
py.test module for unit testing the lastframe step.
"""

from jwst_testing.lastframe import lastframe_utils

import pytest
from jwst.lastframe import LastFrameStep
from jwst.datamodels import LastFrameModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def lastframe_model(request):
    ref_path = request.config.model.meta.ref_file.lastframe.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return LastFrameModel(ref_path)

@pytest.fixture(scope='module')
def lastframe_hdul(request):
    ref_path = request.config.model.meta.ref_file.lastframe.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_lastframe_step(request, input_model):
    request.config.model = LastFrameStep.call(input_model)
