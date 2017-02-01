"""
This file contains the functions which will be used to test the superbias step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def superbias_subtraction(output_hdul, reference_hdul, input_hdul):
    """
    Check that superbias is subtracted from each group in the image array, including 
    reference pixels.  
    """
    check = np.logical_or(reference_hdul['DQ'].data == 0, np.zeros_like(output_hdul['SCI'].data))
    result = np.allclose((input_hdul['SCI'].data - reference_hdul['SCI'].data)[check], output_hdul['SCI'].data[check])
    return result

def pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    """
    Check that all DQ flags are propagated from the reference file 
    (header keyword R_SUPERB) to the output PIXELDQ array.

    .. table:: Supported Flags

        +-----+-------+-----------------+---------------------+
        | Bit | Value | Name            | Description         |
        +=====+=======+=================+=====================+
        | 0   | 1     | DO_NOT_USE      | Bad pixel.          |
        +-----+-------+-----------------+---------------------+
        | 1   | 2     | UNRELIABLE_BIAS | Bias variance large |
        +-----+-------+-----------------+---------------------+

    """
    result = np.all(bitwise_propagate(reference_hdul, input_hdul['PIXELDQ'].data) == output_hdul['PIXELDQ'].data)               
    return result
