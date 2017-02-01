"""
This file contains the functions which will be used to test the saturation step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def groupdq_flagging(output_hdul, reference_hdul):
    """
    Check that for each group in the science data file, if the pixel exceeds the 
    saturation level, then the SATURATED flag is set for that pixel in the
    corresponding plane of the GROUPDQ array - and in all subsequent planes. 
    """
    if 'DQ' in reference_hdul:
        flag = np.logical_and(output_hdul['SCI'].data >= reference_hdul['SCI'].data, 
            reference_hdul['DQ'].data != 2)
    else: 
        flag = output_hdul['SCI'].data >= reference_hdul['SCI'].data

    expected_groupdq = np.zeros_like(output_hdul['GROUPDQ'].data)
    expected_groupdq[flag] = 2
    
    # now make sure that pixels in groups after a flagged pixel are also flagged
    flag = (np.cumsum(expected_groupdq == 2, axis=1) > 0)
    expected_groupdq[flag] = 2 

    result = np.all(output_hdul['GROUPDQ'].data == expected_groupdq)              
    return result

def pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    """
    Check that all DQ flags are propagated from the reference file 
    (header keyword R_SATURA) to the output PIXELDQ array.

    .. table:: Supported Flags

        +-----+-------+---------------+--------------------------------+
        | Bit | Value | Name          | Description                    |
        +=====+=======+===============+================================+
        | 0   | 1     | DO_NOT_USE    | Bad pixel.                     |
        +-----+-------+---------------+--------------------------------+
        | 1   | 2     | NO_SAT_CHECK  | Saturation check not available |
        +-----+-------+---------------+--------------------------------+

    """

    result = np.all(core_utils.bitwise_propagate(reference_hdul, input_hdul['PIXELDQ'].data) == output_hdul['PIXELDQ'].data)
    return result