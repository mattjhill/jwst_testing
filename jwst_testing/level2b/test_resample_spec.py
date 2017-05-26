"""
py.test module for unit testing the resample_spec step.
"""

import pytest
from jwst.resample import ResampleSpecStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_resample_spec_step(request, input_model):
    request.config.model = ResampleSpecStep.call(input_model)
