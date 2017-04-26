import argparse
import os

import pytest

from jwst import datamodels

def collect_2A_steps(input):
    steps = []
    input = datamodels.open(input)
    if input.meta.instrument.name == 'MIRI':

        # process MIRI exposures;
        # the steps are in a different order than NIR

        steps.append("dq_init")
        steps.append("saturation")
        # steps.append("ipc")
        steps.append("linearity")
        steps.append("rscd")
        steps.append("lastframe")

        # calwebb_dark stops here
        if 'DARK' in input.meta.exposure.type:
            return steps

        steps.append("dark_current")
        steps.append("refpix")
        steps.append("persistence")

    else:

        # process Near-IR exposures

        steps.append("dq_init")
        steps.append("saturation")
    #     steps.append("ipc")
        steps.append("superbias")
        steps.append("refpix")
        steps.append("linearity")

        # calwebb_dark stops here
        if 'DARK' in input.meta.exposure.type:
            return steps

        steps.append("persistence")
        steps.append("dark_current")

    # apply the jump step
    steps.append("jump")

    # apply the ramp_fit step
    steps.append("ramp_fit")

    return steps

def collect_2B_steps(input):
    steps = []
    input = datamodels.open(input_file)
    exp_type = input.meta.exposure.type

    # Apply WCS info
    steps.append("assign_wcs")

    # Extract 2D sub-windows for NIRSpec slit and MSA
    if exp_type in ['NRS_FIXEDSLIT', 'NRS_BRIGHTOBJ', 'NRS_MSASPEC']:
        steps.append("extract_2d")

    # Apply flat-field correction
    steps.append("flat_field")

    # Apply the source type decision step
    steps.append("srctype")

    # Apply the straylight correction for MIRI MRS
    if exp_type == 'MIR_MRS':
        steps.append("straylight")

    # Apply the fringe correction for MIRI MRS
    if exp_type == 'MIR_MRS':
        steps.append("fringe")

    # Apply pathloss correction to NIRSpec exposures
    if exp_type in ['NRS_FIXEDSLIT', 'NRS_BRIGHTOBJ', 'NRS_MSASPEC',
                    'NRS_IFU']:
        steps.append("pathloss")

    # Apply flux calibration
    steps.append("photom")

    # Produce a resampled product, either via resample_spec for
    # "regular" spectra or cube_build for IFU data. No resampled
    # product is produced for time-series modes.
    if exp_type in ['NRS_FIXEDSLIT', 'NRS_BRIGHTOBJ',
                                    'NRS_MSASPEC', 'NIS_WFSS', 'NRC_GRISM']:
        # Call the resample_spec step
        steps.append("resample_spec")

    elif exp_type in ['MIR_MRS', 'NRS_IFU']:

        # Call the cube_build step for IFU data
        steps.append("cube_build")

    # Extract a 1D spectrum from the 2D/3D data
    steps.append("extract_1d")

    return steps

def run_pytest(filename, steps_only):

    pytest_args = ['-v']
    steps_2A = collect_2A_steps(filename)
    steps_2B = collect_2B_steps(filename)
    steps = steps_2A
    # steps += steps_2B
    test_files = [os.path.join(os.path.dirname(__file__), step, 'test_' + step + '.py') for step in steps]
    pytest_args += test_files
    pytest_args += ['--uncal', filename, '--html', filename.split('/')[-1].split('.')[0]+'.html']
    if steps_only:
        pytest_args += ['-m', 'step']

    result = pytest.main(pytest_args)

    return result

def run_tests_single():
    parser = argparse.ArgumentParser(description="run tests for a single FITS file")
    parser.add_argument('file', help='Level 1B FITS file')
    parser.add_argument('--steps_only', action='store_true',
                        help='Run only the pipeline steps, no extra validation tests')
    args = parser.parse_args()
    run_pytest(args.file, args.steps_only)


def run_tests_batch():
    pass