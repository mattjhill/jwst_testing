"""
py.test module for unit testing the dq_init step.
"""
from .. import core_utils

import pytest
from jwst.dq_init import DQInitStep
from jwst.datamodels import MaskModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def mask_model(request):
    ref_path = request.config.model.meta.ref_file.mask.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return MaskModel(ref_path)

@pytest.fixture(scope='module')
def mask_hdul(request):
    ref_path = request.config.model.meta.ref_file.mask.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_dq_init_step(request, input_model):
    request.config.model = DQInitStep.call(input_model)

def test_dq_flag_translation(mask_hdul, mask_model):
    expected_dq = core_utils.bitwise_propagate(mask_hdul)
    assert np.all(expected_dq == mask_model.dq)

def test_pixeldq_propagation(output_model, mask_model):
    if mask_model.meta.subarray.name == 'GENERIC':
        xsize = output_model.meta.subarray.xsize
        xstart = output_model.meta.subarray.xstart
        ysize = output_model.meta.subarray.ysize
        ystart = output_model.meta.subarray.ystart
        submask = mask_model.dq[ystart - 1:ysize + ystart - 1, xstart - 1:xstart + xsize - 1]
    else:
        submask = mask_model.dq

    assert np.all(submask == output_model.pixeldq)

def test_groupdq_initialization(output_model):
    assert np.all(output_model.groupdq == 0)

def test_err_initialization(output_model):
    assert np.all(output_model.err == 0)

def test_dq_def_initialization(output_model):
    assert hasattr(output_model, 'dq_def')