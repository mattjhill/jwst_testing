"""
py.test module for unit testing the fringe step.
"""

import pytest
from jwst.fringe import FringeStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_fringe_step(request, input_model):
    request.config.model = FringeStep.call(input_model)
