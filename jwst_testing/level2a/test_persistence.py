"""
py.test module for unit testing the persistence step.
"""

import pytest
from jwst.persistence import PersistenceStep
# from jwst.datamodels import
from astropy.io import fits
import numpy as np

# Set up the fixtures needed for all of the tests

# @pytest.fixture(scope='module')
# def persistence_model(request):
#     ref_path = request.config.model.meta.ref_file.persistence.name
#     ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
#     return RSCDModel(ref_path)
#
# @pytest.fixture(scope='module')
# def persistence_hdul(request):
#     ref_path = request.config.model.meta.ref_file.persistence.name
#     ref_path = ref_path.replace('crds://', '/grp/crds/cache/references/jwst/')
#     return fits.open(ref_path)

# Unit Tests

@pytest.mark.step
def test_persistence_step(request, input_model):
    request.config.model = PersistenceStep.call(input_model)
