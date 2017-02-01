"""
This file contains the functions which will be used to test the dark_current step
of the JWST Calibration Pipeline
"""

from .. import core_utils

import numpy as np

def dark_current_subtraction(output_hdul, reference_hdul, input_hdul):
    """
    The Dark Current step can use reference files with one of two formats:  If the reference 
    file contains a ramp with NFRAMES=1 and GROUPGAP=0, then the program averages and skips dark 
    frames to match the NFRAMES and GROUPGAP values of the science data, before performing a 
    group-by-group subtraction of the dark-reference ramp from the science data.  To speed 
    processing, if the reference file has NFRAMES and GROUPGAP values that match those of the 
    data file, then the ramp will be subtracted as is, without additional averaging.  If the 
    dark ramp has more groups than the science image, the extra dark groups are ignored.  If 
    the dark ramp has fewer groups than the science image, the Dark Current step will issue a 
    warning and return the science image unchanged.
    """

    nframes = output_hdul[0].header['NFRAMES']
    groupgap = output_hdul[0].header['GROUPGAP']
    nints, ngroups, nx, ny = output_hdul['SCI'].shape
    nframes_tot = (nframes+groupgap)*ngroups
    if nframes_tot > reference_hdul['SCI'].data.shape[0]:
        # data should remain unchanged if there are more frames in the 
        # science data than the reference file
        result = np.all(input_hdul['SCI'].data == output_hdul['SCI'].data)
        return result
    else:
        dark_correct = np.zeros((nframes, ngroups, nx, ny))
        data = reference_hdul['SCI'].data[:nframes_tot, :, :]
        for i in range(nframes):
            dark_correct[i] = data[i::(nframes+groupgap),:,:]

        dark_correct = np.average(dark_correct, axis=0)
        result = input_hdul['SCI'].data - dark_correct
        result = np.allclose(result, output_hdul['SCI'].data)
        return result

def pixeldq_propagation(output_hdul, reference_hdul, input_hdul):
    """
    Check that all DQ flags are propagated from the reference file (header keyword 
    R_DARK) to the output PIXELDQ array.

    .. table:: Supported Flags

        +-----+-------+------------------+----------------------+
        | Bit | Value | Name             | Description          |
        +=====+=======+==================+======================+
        | 0   | 1     | DO_NOT_USE       | Bad pixel.           |
        +-----+-------+------------------+----------------------+
        | 1   | 2     | HOT              | Hot Pixel.           |
        +-----+-------+------------------+----------------------+
        | 2   | 4     | WARM             | Warm pixel           |
        +-----+-------+------------------+----------------------+
        | 3   | 8     | UNRELIABLE_DARK  | Dark variance large  |
        +-----+-------+------------------+----------------------+
        | 4   | 16    | UNRELIABLE_SLOPE | Slope variance large |
        +-----+-------+------------------+----------------------+
    """
    nframes = output_hdul[0].header['NFRAMES']
    groupgap = output_hdul[0].header['GROUPGAP']
    nints, ngroups, nx, ny = output_hdul['SCI'].shape
    nframes_tot = (nframes+groupgap)*ngroups
    if nframes_tot > reference_hdul['SCI'].data.shape[0]:
        result = np.all(input_hdul['PIXELDQ'].data == output_hdul['PIXELDQ'].data)
        return result

    else:
        result = np.all(core_utils.bitwise_propagate(reference_hdul, input_hdul['PIXELDQ'].data) == output_hdul['PIXELDQ'].data)
        return result
