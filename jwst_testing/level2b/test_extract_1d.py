"""
py.test module for unit testing the extract_1d step.
"""

import pytest
from jwst.extract_1d import Extract1dStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_extract_1d_step(request, input_model):
    request.config.model = Extract1dStep.call(input_model)
