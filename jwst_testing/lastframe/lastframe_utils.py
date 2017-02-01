"""
This file contains the functions which will be used to test the lastframe step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def lastframe_correction(input_hdul, reference_hdul, output_hdul):
    """
    Check that the values in the SCI extension of the last-frame reference file are 
    subtracted from the final frame of the science exposure.
    """
    expected = input_hdul['SCI'].data
    expected[:,-1,:,:] -= reference_hdul['SCI'].data
    result = np.allclose(expected, output_hdul['SCI'].data)
    return result