"""
py.test module for unit testing the cube_build step.
"""

import pytest
from jwst.cube_build import CubeBuildStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_cube_build_step(request, input_model):
    request.config.model = CubeBuildStep.call(input_model)
