"""
py.test module for unit testing the pathloss step.
"""

import pytest
from jwst.pathloss import PathLossStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_pathloss_step(request, input_model):
    request.config.model = PathLossStep.call(input_model)
