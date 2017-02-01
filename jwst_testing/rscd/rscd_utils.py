"""
This file contains the functions which will be used to test the rscd step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def rscd_correction(input_hdul, reference_hdul, output_hdul):
    """
    Check that for each integration in the input science data, the 
    reset corrections are subtracted, group by group, integration 
    by integration. If the input science data contains more groups 
    than the reset correction, then the correction for subsequent 
    groups is zero. If the input science data contains more 
    integrations than the reset correction, then the correction 
    corresponding to the final integration in the reset file is used. 
    Only performed for MIRI data.

    WARNING: Possibly depreceated in B7 switched to RSCD correction
    """
    nints, ngroups, nx, ny = output_hdul['SCI'].data.shape
    results = []
    for i in range(nints):
        for g in range(ngroups-1):
            if i >= reference_hdul['SCI'].data.shape[0]:
                results.append(np.allclose(input_hdul['SCI'].data[i,g,:,:] - reference_hdul['SCI'].data[-1,g,:,:], output_hdul['SCI'].data[i,g,:,:]))
            elif g >= reference_hdul['SCI'].data.shape[1]:
                results.append(np.allclose(input_hdul['SCI'].data[i,g,:,:], output_hdul['SCI'].data[i,g,:,:]))
            else:
                results.append(np.allclose(input_hdul['SCI'].data[i,g,:,:] - reference_hdul['SCI'].data[i,g,:,:], output_hdul['SCI'].data[i,g,:,:]))
    result = np.all(results)
    return result

def pixeldq_propagation(input_hdul, reference_hdul, output_hdul):
    """
    Check that all DQ flags are propagated from the reference file (header keyword 
    R_RESET) to the output PIXELDQ array.

    .. table:: Supported Flags

        +-----+-------+------------------+----------------------------+
        | Bit | Value | Name             | Description                |
        +=====+=======+==================+============================+
        | 0   | 1     | DO_NOT_USE       | Bad pixel.                 |
        +-----+-------+------------------+----------------------------+
        | 1   | 2     | UNRELIABLE_RESET | Sensitive to reset anomaly |
        +-----+-------+------------------+----------------------------+

    """
    result = np.all(core_utils.bitwise_propagate(reference_hdul, input_hdul['PIXELDQ'].data) == output_hdul['PIXELDQ'].data)
    return result
