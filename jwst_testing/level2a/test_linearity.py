"""
py.test module for unit testing the linearity step.
"""

from jwst_testing.linearity import linearity_utils


import pytest
from jwst.linearity import LinearityStep
from jwst.datamodels import LinearityModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def superbias_model(request):
    ref_path = request.config.model.meta.ref_file.linearity.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return LinearityModel(ref_path)

@pytest.fixture(scope='module')
def superbias_hdul(request):
    ref_path = request.config.model.meta.ref_file.linearity.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_linearity_step(request, input_model):
    request.config.model = LinearityStep.call(input_model)
