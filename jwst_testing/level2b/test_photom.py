"""
py.test module for unit testing the photom step.
"""

import pytest
from jwst.photom import PhotomStep
from jwst.datamodels import PhotomModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def photom_model(request):
    ref_path = request.config.model.meta.ref_file.photom.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return PhotomModel(ref_path)

@pytest.fixture(scope='module')
def photom_hdul(request):
    ref_path = request.config.model.meta.ref_file.photom.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_photom_step(request, input_model):
    request.config.model = PhotomStep.call(input_model)
