"""
py.test module for unit testing the dq_init step.
"""

import pytest
from jwst.superbias import SuperBiasStep
from jwst.datamodels import SuperBiasModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def superbias_model(request):
    ref_path = request.config.model.meta.ref_file.superbias.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return SuperBiasModel(ref_path)

@pytest.fixture(scope='module')
def superbias_hdul(request):
    ref_path = request.config.model.meta.ref_file.superbias.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_superbias_step(request, input_model):
    request.config.model = SuperBiasStep.call(input_model)

