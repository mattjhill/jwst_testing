"""
This file contains the functions which will be used to test the dq_init step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def pixeldq_ext_exists(output_hdul):
    """
    Check that the PIXELDQ extension has been added to the output hdulList.
    """
    result = "PIXELDQ" in output_hdul
    return result

def groupdq_ext_exists(output_hdul):
    """
    Check that the GROUPDQ extension has been added to the output HDUList.
    """
    result = "GROUPDQ" in output_file
    return result

def groupdq_vals_all_zero(output_hdul):
    """
    Check that the GROUPDQ array values are all initialized to zero.
    """
    result = (np.all(output_hdul["GROUPDQ"].data == 0))
    return result

def err_ext_exists(output_hdul):
    """
    Check that the ERR extension has been added to the output HDUList.
    """

    result = "ERR" in output_hdul
    return result

def err_vals_all_zero(output_hdul):
    """
    Check that the ERR array values are all initialized to zero.
    """

    result = np.all(output_hdul["ERR"].data == 0)
    return result

def pixeldq_propagation(output_hdul, reference_hdul):
    """
    Check that all DQ flags are propagated from the reference file (header keyword 
    R_MASK) to the output PIXELDQ array.

    .. table:: Expected Flags

        +-----+-------+---------------+---------------------------------------------+
        | Bit | Value | Name          | Description                                 |
        +=====+=======+===============+=============================================+
        | 0   | 1     | DO_NOT_USE    | Bad pixel.                                  |
        +-----+-------+---------------+---------------------------------------------+
        | 1   | 2     | NON_SCIENCE   | Pixel not on science portion of detector    |
        +-----+-------+---------------+---------------------------------------------+
        | 2   | 4     | DEAD          | Dead pixel                                  |
        +-----+-------+---------------+---------------------------------------------+
        | 3   | 8     | LOW_QE        | Low quantum efficiency                      |
        +-----+-------+---------------+---------------------------------------------+
        | 4   | 16    | NO_GAIN_VALUE | Gain cannot be measured                     |
        +-----+-------+---------------+---------------------------------------------+
        | 5   | 32    | OPEN          | open Pixel (counts move to adjacent pixels) |
        +-----+-------+---------------+---------------------------------------------+
        | 6   | 64    | ADJ_OPEN      | Adjacent to open pixel                      |
        +-----+-------+---------------+---------------------------------------------+

    """
    input_dq = np.zeros_like(output_hdul['PIXELDQ'].data)
    result = np.all(core_utils.bitwise_propagate(reference_hdul, input_dq) == output_hdul['PIXELDQ'].data)
    return result
