"""
py.test module for unit testing the dark_current step.
"""

import pytest
from jwst.assign_wcs import AssignWcsStep
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

# @pytest.fixture(scope='module')
# def dark_model(request):
#     ref_path = request.config.model.meta.ref_file.dark.name
#     ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
#     if request.config.model.meta.instrument.name == 'MIRI':
#         return DarkMIRIModel(ref_path)
#     else:
#         return DarkModel(ref_path)
#
# @pytest.fixture(scope='module')
# def dark_hdul(request):
#     ref_path = request.config.model.meta.ref_file.dark.name
#     ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
#     return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_assign_wcs_step(request, input_model):
    request.config.model = AssignWcsStep.call(input_model)
