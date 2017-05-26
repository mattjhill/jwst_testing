"""
py.test module for unit testing the ramp fitting step.
"""

import pytest
from jwst.ramp_fitting import RampFitStep
from jwst.datamodels import GainModel, ReadnoiseModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def gain_model(request):
    ref_path = request.config.model.meta.ref_file.gain.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return GainModel(ref_path)

@pytest.fixture(scope='module')
def gain_hdul(request):
    ref_path = request.config.model.meta.ref_file.gain.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

@pytest.fixture(scope='module')
def readnoise_model(request):
    ref_path = request.config.model.meta.ref_file.readnoise.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return ReadnoiseModel(ref_path)

@pytest.fixture(scope='module')
def readnoise_hdul(request):
    ref_path = request.config.model.meta.ref_file.readnoise.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_ramp_fit_step(request, input_model):
    request.config.model = RampFitStep.call(input_model)
