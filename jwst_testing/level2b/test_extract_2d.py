"""
py.test module for unit testing the extract_2d step.
"""

import pytest
from jwst.extract_2d import Extract2dStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_extract_2d_step(request, input_model):
    request.config.model = Extract2dStep.call(input_model)
