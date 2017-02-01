"""
This file contains the functions which will be used to test the linearity step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def linearity_correction(output_hdul, reference_hdul, input_hdul):
    """
    Check that the linearity correction is properly applied to all relevant pixels. The algorithm 
    uses a polynomial of the form

    .. math::

        F_c = \sum_{i=0}^N C_i F^i
    
    where :math:`F_c` is the corrected counts, :math:`C` are the correction coefficients, and :math:`F` 
    is the uncorrected counts.  The coefficients of the polynomial at each pixel are given by the 
    reference file.        
    """

    # ignore pixels which are saturated (GROUPDQ = 2) or NO_LIN_CORR (DQ = 2)
    corrected = np.logical_and(input_hdul['GROUPDQ'].data != 2, reference_hdul['DQ'].data != 2)
    
    linearity_applied = np.allclose(
        np.polyval(reference_hdul['COEFFS'].data[::-1], input_hdul['SCI'].data)[corrected], 
        output_hdul['SCI'].data[corrected])

    linearity_ignored = np.allclose(input_hdul['SCI'].data[~corrected], 
        output_hdul['SCI'].data[~corrected])

    # make sure that the values linearity correction is properly applied to relevant pixels
    # and ignored elsewhere
    result = linearity_applied and linearity_ignored
    return result

def pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    """
    Check that all DQ flags are propagated from the reference file (header keyword 
    R_LINEAR) to the output PIXELDQ array.

    .. table:: Supported Flags

        +-----+-------+------------------+-----------------------------------------+
        | Bit | Value | Name             | Description                             |
        +=====+=======+==================+=========================================+
        | 0   | 1     | DO_NOT_USE       | Bad pixel.                              |
        +-----+-------+------------------+-----------------------------------------+
        | 1   | 2     | NONLINEAR        | Pixel highly nonlinear.                 |
        +-----+-------+------------------+-----------------------------------------+
        | 2   | 4     | NO_LIN_CORR      | Linearity correction not available.     |
        +-----+-------+------------------+-----------------------------------------+

    """
    result =  np.all(core_utils.bitwise_propagate(reference_hdul, input_hdul['PIXELDQ'].data) == output_hdul['PIXELDQ'].data)
    return result
