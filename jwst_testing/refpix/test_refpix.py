"""
py.test module for unit testing the refpix step.
"""

from . import refpix_utils


import pytest
from jwst.refpix import RefPixStep
from jwst.datamodels import SuperBiasModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def superbias_model(request):
    ref_path = request.config.model.meta.ref_file.refpix.name
    if ref_path:
        ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
        return SuperBiasModel(ref_path)
    else:
        return None


@pytest.fixture(scope='module')
def superbias_hdul(request):
    ref_path = request.config.model.meta.ref_file.refpix.name
    if ref_path:
        ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
        return fits.open(ref_path)
    else:
        return None

# Unit Tests

@pytest.mark.step
def test_refpix_step(request, input_model):
    request.config.model = RefPixStep.call(input_model)
