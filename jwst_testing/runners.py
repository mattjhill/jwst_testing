import argparse
from datetime import datetime
import multiprocessing
import os

from astropy.io import fits
import pytest
from py.xml import html, raw
import pkg_resources
import pytest_html

from jwst import datamodels

image2 = ['NRC_IMAGE', 'NRC_TACQ', 'NRC_CORON', 'NRC_FOCUS', 'NRC_WFSS',
          'NRC_TACONFIRM', 'NRC_TSIMAGE', 'NRS_BOTA', 'NRS_CONFIRM', 'NRS_IMAGE',
          'NRS_MIMF', 'NRS_TACONFIRM', 'NRS_TACQ', 'NRS_TASLIT', 'NIS_AMI', 'NIS_IMAGE',
          'NIS_TACQ', 'NIS_TACONFIRM', 'MIR_IMAGE', 'MIR_TACQ', 'MIR_LYOT', 'MIR_4QPM',
          'MIR_CORONCAL', 'FGS_IMAGE']

spec2 = ['NRC_GRISM', 'NRC_TSGRISM', 'NRS_BRIGHTOBJ', 'NRS_FIXEDSLIT', 'NRS_IFU',
         'NRS_LAMP', 'NRS_MSASPEC', 'NIS_SOSS', 'NIS_WFSS','MIR_LRS-FIXEDSLIT',
         'MIR_LRS-SLITLESS', 'MIR_MRS']

def collect_2A_steps(header):
    steps = []
    if header['INSTRUME'] == 'MIRI':

        # process MIRI exposures;
        # the steps are in a different order than NIR

        steps.append("dq_init")
        steps.append("saturation")
        # steps.append("ipc")
        steps.append("linearity")
        steps.append("rscd")
        steps.append("lastframe")

        # # calwebb_dark stops here
        # if 'DARK' in input.meta.exposure.type:
        #     return steps
        #
        # steps.append("dark_current")
        # steps.append("refpix")
        # steps.append("persistence")

    else:

        # process Near-IR exposures

        steps.append("dq_init")
        steps.append("saturation")
    #     steps.append("ipc")
        steps.append("superbias")
        steps.append("refpix")
        steps.append("linearity")

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

def collect_spec2B_steps(header):
    steps = []
    exp_type = header['EXP_TYPE']

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

def collect_image2B_steps(header):
    return ["assign_wcs", "flat_field", "photom"]

def run_pytest(filename, steps_only=True):

    pytest_args = ['-v']
    header = fits.getheader(filename)
    steps = collect_2A_steps(header)

    # if header['EXP_TYPE'] in image2:
    #     steps += collect_image2B_steps(header)
    # if header['EXP_TYPE'] in spec2:
    #     steps += collect_spec2B_steps(header)

    test_files = [os.path.join(os.path.dirname(__file__), step, 'test_' + step + '.py') for step in steps]
    pytest_args += test_files
    pytest_args += ['--uncal', filename, '--html',
                    filename.split('/')[-1].replace('fits', 'html'),
                    '--self-contained-html']
    if steps_only:
        pytest_args += ['-m', 'step']

    result = pytest.main(pytest_args)
    return filename, result

def run_tests_single():
    parser = argparse.ArgumentParser(description="run tests for a single FITS file")
    parser.add_argument('file', help='Level 1B FITS file')
    parser.add_argument('--steps_only', action='store_true',
                        help='Run only the pipeline steps, no extra validation tests')
    args = parser.parse_args()
    run_pytest(args.file, args.steps_only)


def run_tests_batch():
    parser = argparse.ArgumentParser(description="run tests for a number of FITS file")
    parser.add_argument('file', help='list of files')
    parser.add_argument('-n', help='number of processes to run in parallel', type=int)
    parser.add_argument('--steps_only', action='store_true',
                        help='Run only the pipeline steps, no extra validation tests')
    args = parser.parse_args()

    file_list = os.path.abspath(args.file)
    time = datetime.utcnow().isoformat()
    os.mkdir(time)
    os.chdir(time)

    rows = []
    file_list = open(file_list).read().split()
    if args.n is not None:
        p = multiprocessing.Pool(args.n)
    else:
        p = multiprocessing.Pool()

    for result in p.imap(run_pytest, file_list):
        f = result[0]

        header = fits.getheader(f)
        body = html.body()

        cells = [
            html.th('Filename',
                    class_='sortable intial-sort',
                    col='result'),
            html.th('Result', class_='sortable', col='result'),
            html.th('Instrument', class_='sortable', col='name'),
            html.th('Detector', class_='sortable', col='detector'),
            html.th('Filter', class_='sortable', col='filter'),
            html.th('Pupil', class_='sortable', col='pupil'),
            html.th('Grating', class_='sortable', col='grating'),
            html.th('Channel', class_='sortable', col='channel'),
            html.th('Band', class_='sortable', col='band'),
            html.th('Exposure Type', class_='sortable', col='exp_type'),
            html.th('Read Pattern', class_='sortable', col='readpatt'),
            html.th('Nints', class_='sortable numeric', col='nints'),
            html.th('Ngroups', class_='sortable numeric', col='ngroups'),
            html.th('Subarray', class_='sortable', col='subarray'),
            html.th('X Start', class_='sortable numeric', col='xstart'),
            html.th('X Size', class_='sortable numeric', col='xsize'),
            html.th('Y Start', class_='sortable numeric', col='ystart'),
            html.th('Y Size', class_='sortable numeric', col='ysize')]

        if result[1]:
            rows.append([
                html.td(html.a(f.split('/')[-1], href=f.split('/')[-1].replace('fits', 'html'))),
                failed('Failed'),
                html.td(get_keyword(header, 'INSTRUME')),
                html.td(get_keyword(header, 'DETECTOR')),
                html.td(get_keyword(header, 'FILTER')),
                html.td(get_keyword(header, 'PUPIL')),
                html.td(get_keyword(header, 'GRATING')),
                html.td(get_keyword(header, 'CHANNEL')),
                html.td(get_keyword(header, 'BAND')),
                html.td(get_keyword(header, 'EXP_TYPE')),
                html.td(get_keyword(header, 'READPATT')),
                html.td(get_keyword(header, 'NINTS')),
                html.td(get_keyword(header, 'NGROUPS')),
                html.td(get_keyword(header, 'SUBARRAY')),
                html.td(get_keyword(header, 'SUBSTRT1')),
                html.td(get_keyword(header, 'SUBSIZE1')),
                html.td(get_keyword(header, 'SUBSTRT2')),
                html.td(get_keyword(header, 'SUBSIZE2'))])

        else:
            rows.append([
                html.td(html.a(f.split('/')[-1], href=f.split('/')[-1].replace('fits', 'html'))),
                passed('Passed'),
                html.td(get_keyword(header, 'INSTRUME')),
                html.td(get_keyword(header, 'DETECTOR')),
                html.td(get_keyword(header, 'FILTER')),
                html.td(get_keyword(header, 'PUPIL')),
                html.td(get_keyword(header, 'GRATING')),
                html.td(get_keyword(header, 'CHANNEL')),
                html.td(get_keyword(header, 'BAND')),
                html.td(get_keyword(header, 'EXP_TYPE')),
                html.td(get_keyword(header, 'READPATT')),
                html.td(get_keyword(header, 'NINTS')),
                html.td(get_keyword(header, 'NGROUPS')),
                html.td(get_keyword(header, 'SUBARRAY')),
                html.td(get_keyword(header, 'SUBSTRT1')),
                html.td(get_keyword(header, 'SUBSIZE1')),
                html.td(get_keyword(header, 'SUBSTRT2')),
                html.td(get_keyword(header, 'SUBSIZE2'))])

        table_rows = [html.tr(row) for row in rows]
        table = [html.h2('Results'), html.table([html.thead(html.tr(cells),
                                                            id='results-table-head')] + table_rows,
                                                id='results-table')]
        body.extend(table)

        style_css = pkg_resources.resource_string(
            pytest_html.__name__, os.path.join('resources', 'style.css'))
        # css_href = '{0}/{1}'.format('assets', 'style.css')
        # html_css = html.link(href=css_href, rel='stylesheet',
        #                      type='text/css')
        html_css = html.style(raw(style_css))
        head = html.head(
            html.meta(charset='utf-8'),
            html.title('Test Report'),
            html_css)

        doc = html.html(head, body)
        report = open('results.html', 'w')
        report.write(doc.unicode(indent=2))
        report.close()

    os.chdir('..')

def get_keyword(header, keyword):
    if keyword in header:
        return header[keyword]
    else:
        return ''

class passed(html.td):
    style = html.Style(color = 'green')

class inprogress(html.td):
    style = html.Style(color = 'orange')

class failed(html.td):
    style = html.Style(color = 'red')

