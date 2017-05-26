"""
py.test module for unit testing the srctype step.
"""

import pytest
from jwst.srctype import SourceTypeStep
from astropy.io import fits
import numpy as np

# Unit Tests

@pytest.mark.step
def test_srctype_step(request, input_model):
    request.config.model = SourceTypeStep.call(input_model)
