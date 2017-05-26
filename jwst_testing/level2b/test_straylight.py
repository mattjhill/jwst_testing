"""
py.test module for unit testing the straylight step.
"""

import pytest
from jwst.straylight import StraylightStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_straylight_step(request, input_model):
    request.config.model = StraylightStep.call(input_model)
