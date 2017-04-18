"""
py.test module for unit testing the saturation step.
"""

from .. import core_utils

import pytest
from jwst.saturation import SaturationStep
from jwst.datamodels import SaturationModel
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

@pytest.fixture(scope='module')
def saturation_model(request):
    ref_path = request.config.model.meta.ref_file.saturation.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return SaturationModel(ref_path)

@pytest.fixture(scope='module')
def saturation_hdul(request):
    ref_path = request.config.model.meta.ref_file.saturation.name
    ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
    return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_saturation_step(request, input_model):
    request.config.model = SaturationStep.call(input_model)

def test_groupdq_flagging(output_model, saturation_model):

    # extract subarray
    if saturation_model.meta.subarray.name == 'GENERIC':
        xsize = output_model.meta.subarray.xsize
        xstart = output_model.meta.subarray.xstart
        ysize = output_model.meta.subarray.ysize
        ystart = output_model.meta.subarray.ystart
        satmask = saturation_model.data[ystart - 1:ysize + ystart - 1, xstart - 1:xstart + xsize - 1]

    else:
        satmask = saturation_model.data

    # flag pixels greater than saturation threshold
    expected_groupdq = np.zeros_like(output_model.groupdq)
    flagged = output_model.data >= satmask
    expected_groupdq[flagged] = 2

    # make sure that pixels in groups after a flagged pixel are also flagged
    flagged = np.cumsum(expected_groupdq == 2, axis=1) > 0
    expected_groupdq[flagged] = 2

    assert np.all(output_model.groupdq == expected_groupdq)

def test_dq_flag_translation(saturation_hdul, saturation_model):
    expected_dq = core_utils.bitwise_propagate(saturation_hdul)
    assert np.all(expected_dq == saturation_model.dq)

def test_pixeldq_propagation(output_model, saturation_model, input_model):

    if saturation_model.meta.subarray.name == 'GENERIC':
        xsize = output_model.meta.subarray.xsize
        xstart = output_model.meta.subarray.xstart
        ysize = output_model.meta.subarray.ysize
        ystart = output_model.meta.subarray.ystart
        submask = saturation_model.dq[ystart - 1:ysize + ystart - 1, xstart - 1:xstart + xsize - 1]

    else:
        submask = saturation_model.dq

    assert np.all(output_model.pixeldq == np.bitwise_or(submask, input_model.pixeldq))
