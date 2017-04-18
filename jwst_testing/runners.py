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
        # steps.append("linearity")
        # steps.append("rscd")
        # steps.append("lastframe")
        #
        # # calwebb_dark stops here
        # if 'DARK' in input.meta.exposure.type:
        #     return steps
        #
        # steps.append("dark_current")
        # steps.append("refpix")
        # steps.append("persistence")

    else:

        # process Near-IR exposures
        log.debug('Processing a Near-IR exposure')

        steps.append("dq_init")
        steps.append("saturation")
    #     steps.append("ipc")
    #     steps.append("superbias")
    #     steps.append("refpix")
    #     steps.append("linearity")
    #
    #     # calwebb_dark stops here
    #     if 'DARK' in input.meta.exposure.type:
    #         return steps
    #
    #     steps.append("persistence")
    #     steps.append("dark_current")
    #
    # # apply the jump step
    # steps.append("jump")
    #
    # # apply the ramp_fit step
    # steps.append("ramp_fit")

    return steps

def collect_2B_steps(input):

    return []

def run_tests_single():
    parser = argparse.ArgumentParser(description="run tests for a single FITS file")
    parser.add_argument('file', help='Level 1B FITS file')
    parser.add_argument('--steps_only', action='store_true',
                        help='Run only the pipeline steps, no extra validation tests')
    args = parser.parse_args()

    pytest_args = ['-v']
    steps_2A = collect_2A_steps(args.file)
    steps_2B = collect_2B_steps(args.file)
    steps = steps_2A + steps_2B
    test_files = [os.path.join(os.path.dirname(__file__), step, 'test_' + step + '.py') for step in steps]
    pytest_args += test_files
    pytest_args += ['--uncal', args.file, '--html', args.file.split('/')[-1].split('.')[0]+'.html']
    if args.steps_only:
        pytest_args += ['-m', 'step']
    pytest.main(pytest_args)

def run_tests_batch():
    pass