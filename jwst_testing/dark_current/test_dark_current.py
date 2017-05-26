"""
py.test module for unit testing the dark_current step.
"""

import pytest
from jwst.dark_current import DarkCurrentStep
from jwst.datamodels import DarkModel, DarkMIRIModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def dark_model(request):
    ref_path = request.config.model.meta.ref_file.dark.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    if request.config.model.meta.instrument.name == 'MIRI':
        return DarkMIRIModel(ref_path)
    else:
        return DarkModel(ref_path)

@pytest.fixture(scope='module')
def dark_hdul(request):
    ref_path = request.config.model.meta.ref_file.dark.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_dark_current_step(request, input_model):
    request.config.model = DarkCurrentStep.call(input_model)
