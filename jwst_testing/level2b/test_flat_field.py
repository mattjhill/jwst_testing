"""
py.test module for unit testing the flat_field step.
"""

import pytest
from jwst.flatfield import FlatFieldStep
from jwst.datamodels import FlatModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def flatfield_model(request):
    ref_path = request.config.model.meta.ref_file.flat.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return FlatModel(ref_path)

@pytest.fixture(scope='module')
def flatfield_hdul(request):
    ref_path = request.config.model.meta.ref_file.flat.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_flat_field_step(request, input_model):
    request.config.model = FlatFieldStep.call(input_model)
