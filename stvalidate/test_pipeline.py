from astropy.io import fits
import numpy as np
import unittest
import pytest
import os
from .chapters import ReportChapter

dq_dict = {
'DO_NOT_USE' : 0,
'SATURATED' : 1,
'JUMP_DET' : 2,
'DROPOUT' : 3,
'RESERVED' : 4,     
'RESERVED' : 5,     
'RESERVED' : 6,     
'RESERVED' : 7,     
'UNRELIABLE_ERROR' : 8,
'NON_SCIENCE' : 9,
'DEAD' : 10,
'HOT' : 11,
'WARM' : 12,
'LOW_QE' : 13,
'RC' : 14,
'TELEGRAPH' : 15,
'NONLINEAR' : 16,
'BAD_REF_PIXEL' : 17,
'NO_FLAT_FIELD' : 18,
'NO_GAIN_VALUE' : 19,
'NO_LIN_CORR' : 20,
'NO_SAT_CHECK' : 21,
'UNRELIABLE_BIAS' : 22,
'UNRELIABLE_DARK' : 23,
'UNRELIABLE_SLOPE' : 24,
'UNRELIABLE_FLAT' : 25,
'OPEN' : 26,
'ADJ_OPEN' : 27,
'UNRELIABLE_RESET' : 28,
'MSA_FAILED_OPEN' : 29,
'OTHER_BAD_PIXEL' : 30,
}

def get_pixeldq_bit(name):
    if name in dq_dict:
        return dq_dict[name]
    else:
        return 'N/A'

def bitwise_propagate(refhdu, pixeldq):
    for row in refhdu['DQ_DEF'].data:
        try:
            # find which pixels have the bit set
            flagged = (np.bitwise_and(1, np.right_shift(refhdu['DQ'].data.astype(np.uint32), row['BIT'])))
            # shift them to the correct bit for PIXELDQ
            flagged = np.left_shift(flagged, dq_dict[row['NAME']])
            # propagate into the PIXELDQ extension
            pixeldq = np.bitwise_or(pixeldq, flagged)
        except KeyError:
            print("No DQ mnemonic "+row['NAME'])
    return pixeldq

@pytest.fixture(scope="module")
def toctree(request):
    index = ReportChapter("JWST Calibration Pipeline Validation Testing Report")
    index.add_text(".. toctree::"+'\n\t'+":maxdepth: 2")
    def cleanup():
        if pytest.config.getoption("--gen_report"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            index.write("source/index.rst")
            os.chdir(curdir)

    request.addfinalizer(cleanup)
    return index

class TestDQInitStep:
    """
    The base class for testing the Data Quality Initialization.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("dq_init", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("dq_init", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs dq_init input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("dq_init", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("dq_init", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs dq_init output_file")

    @pytest.fixture(scope="class")
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_MASK'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Data Quality Initialization")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/dq_init.rst")
                toctree.add_text('\t'+"dq_init", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_pixeldq_ext_exists(self, output_file, chapter, request):
        """
        Check that the PIXELDQ extension has been added to the output HDUList.
        """
        result = "PIXELDQ" in output_file
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_pixeldq_propagation(self, output_file, refhdu, chapter, request):
        """
        Check that all DQ flags are propagated from the reference file (header keyword 
        R_MASK) to the output PIXELDQ array.

        .. table:: Supported Flags

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
        input_dq = np.zeros_like(output_file['PIXELDQ'].data)
        result = np.all(bitwise_propagate(refhdu, input_dq) == output_file['PIXELDQ'].data)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_groupdq_ext_exists(self, output_file, chapter, request):
        """
        Check that the GROUPDQ extension has been added to the output HDUList.
        """
        result = "GROUPDQ" in output_file
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_groupdq_vals_all_zero(self, output_file, chapter, request):
        """
        Check that the GROUPDQ array values are all initialized to zero.
        """
        result = (np.all(output_file["GROUPDQ"].data == 0))

        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result


    def test_err_ext_exists(self, output_file, chapter, request):
        """
        Check that the ERR extension has been added to the output HDUList.
        """

        result = ("ERR" in output_file)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_err_vals_all_zero(self, output_file, chapter, request):
        """
        Check that the ERR array values are all initialized to zero.
        """

        result = (np.all(output_file["ERR"].data == 0))
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

class TestSaturationStep:
    """
    The base class for testing Saturation Check.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("saturation", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("saturation", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs saturation input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("saturation", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("saturation", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs saturation output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_SATURA'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Saturation")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/saturation.rst")
                toctree.add_text('\t'+"saturation", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_saturation_groupdq_set(self, output_file, refhdu, chapter, request):
        """
        Check that for each group in the science data file, if the pixel exceeds the 
        saturation level, then the SATURATED flag is set for that pixel in the
        corresponding plane of the GROUPDQ array - and in all subsequent planes. 
        """
        if 'DQ' in refhdu:
            flag = np.logical_and(output_file['SCI'].data >= refhdu['SCI'].data, 
                refhdu['DQ'].data != 2)
        else: 
            flag = output_file['SCI'].data >= refhdu['SCI'].data

        expected_groupdq = np.zeros_like(output_file['GROUPDQ'].data)
        expected_groupdq[flag] = 2
        
        #now make sure that pixels in groups after a flagged pixel are also flagged
        flag = (np.cumsum(expected_groupdq == 2, axis=1) > 0)
        expected_groupdq[flag] = 2 

        result = np.all(output_file['GROUPDQ'].data == expected_groupdq)
        #if pytest.config.getoption("--gen_report"):
            # chapter.add_subsection("Saturation Flag Check")

            # description = "If the pixel value is higher than the saturation level determined by the reference file it should have its GROUPDQ value changed to 2 along with all subsequent pixels in the integration, unless it's PIXELDQ is flagged as NO_SAT_CHECK or it has a value of NaN.  We check that these flags are correctly set."
            # chapter.add_text(description)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    @pytest.mark.dq_init
    def test_saturation_pixeldq_propagation(self, output_file, refhdu, input_file, request, chapter):
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
        try:
            result = np.all(bitwise_propagate(refhdu, input_file['PIXELDQ'].data) == output_file['PIXELDQ'].data)
        except Exception as err:
            result = False
            if pytest.config.getoption("--gen_report"):
                chapter.add_text(":py:meth:`"+request.function.__name__+"` ERROR")
                chapter.add_text("Failed due to Error: "+err.args[0])
                chapter.add_text(request.function.__doc__)
                assert result, "Failed due to Error: "+err.args[0]


        #if pytest.config.getoption("--gen_report"):
            # dq_def = list(refhdu['DQ_DEF'].data)
            # dq_def.insert(0, refhdu['DQ_DEF'].data.columns.names)
            # dq_def = [list(row) for row in dq_def]
            # dq_def[0].insert(1, "PIXELDQ BIT")
            # [row.insert(1, get_pixeldq_bit(row[2])) for row in dq_def[1:]]
            # chapter.add_subsection("Data Quality Flag Propagation")

            # description = "The reference file for this step has a DQ_DEF extension which describes the format of DQ extension, which contains various pixel quality flags.  We must ensure that the pipeline supported flags are properly tranlated into the PIXELDQ extension of the step output."
            # chapter.add_text(description)
            # chapter.add_table("Reference File DQ_DEF", dq_def)

        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

class TestIPCStep:
    """
    The base class for testing IPC Deconvolution.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("ipc", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("ipc", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs ipc input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("ipc", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("ipc", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs ipc output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_IPC'][7:]
        return fits.open(ref_file)

class TestSuperbiasStep:
    """
    The base class for testing Superbias Subtraction.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("superbias", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("superbias", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs superbias input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("superbias", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("superbias", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs superbias output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_SUPERB'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Superbias Subtraction")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/superbias.rst")
                toctree.add_text('\t'+"superbias", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_superbias_subtraction(self, output_file, refhdu, input_file, request, chapter):
        """
        Check that superbias is subtracted from each group in the image array, including 
        reference pixels.  
        """
        check = np.logical_or(refhdu['DQ'].data == 0, np.zeros_like(output_file['SCI'].data))
        result = np.allclose((input_file['SCI'].data - refhdu['SCI'].data)[check], output_file['SCI'].data[check])
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_superbias_pixeldq_propagation(self, output_file, refhdu, input_file, request, chapter):
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
        result = np.all(bitwise_propagate(refhdu, input_file['PIXELDQ'].data) == output_file['PIXELDQ'].data)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

class TestRefpixStep:
    """
    The base class for testing Reference-Pixel Correction.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("refpix", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("refpix", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs refpix input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("refpix", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("refpix", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs refpix output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        if 'R_REFPIX' in output_file[0].header:
            CRDS = '/grp/crds/cache/references/jwst/'
            ref_file = CRDS+output_file[0].header['R_REFPIX'][7:]
            return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Reference Pixel Correction")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/refpix.rst")
                toctree.add_text('\t'+"refpix", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

class TestResetStep:
    """
    The base class for testing the Reset-Anomaly Correction.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("reset", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("reset", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs reset input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("reset", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("reset", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs reset output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_RESET'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Reset Anomaly Correction")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/reset.rst")
                toctree.add_text('\t'+"reset", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_reset_correction(self, input_file, refhdu, output_file, request, chapter):
        """
        Check that for each integration in the input science data, the 
        reset corrections are subtracted, group by group, integration 
        by integration. If the input science data contains more groups 
        than the reset correction, then the correction for subsequent 
        groups is zero. If the input science data contains more 
        integrations than the reset correction, then the correction 
        corresponding to the final integration in the reset file is used. 
        Only performed for MIRI data.
        """
        nints, ngroups, nx, ny = output_file['SCI'].data.shape
        print(nints, ngroups)
        results = []
        for i in range(nints):
            for g in range(ngroups-1):
                if i >= refhdu['SCI'].data.shape[0]:
                    results.append(np.allclose(input_file['SCI'].data[i,g,:,:] - refhdu['SCI'].data[-1,g,:,:], output_file['SCI'].data[i,g,:,:]))
                elif g >= refhdu['SCI'].data.shape[1]:
                    results.append(np.allclose(input_file['SCI'].data[i,g,:,:], output_file['SCI'].data[i,g,:,:]))
                else:
                    results.append(np.allclose(input_file['SCI'].data[i,g,:,:] - refhdu['SCI'].data[i,g,:,:], output_file['SCI'].data[i,g,:,:]))
        result = np.all(results)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_reset_pixeldq_propagation(self, input_file, refhdu, output_file, request, chapter):
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
        result = np.all(bitwise_propagate(refhdu, input_file['PIXELDQ'].data) == output_file['PIXELDQ'].data)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

class TestLastframeStep:
    """
    The base class for testing Last-Frame Correction.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("lastframe", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("lastframe", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs lastframe input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("lastframe", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("lastframe", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs lastframe output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        if output_file[0].header['INSTRUME'] != 'MIRI':
            pytest.skip()

        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_LASTFR'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Lastframe Correction")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/lastframe.rst")
                toctree.add_text('\t'+"lastframe", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_lastframe_correction(self, input_file, refhdu, output_file, request, chapter):
        """
        Check that the values in the SCI extension of the last-frame reference file are 
        subtracted from the final frame of the science exposure.
        """
        expected = input_file['SCI'].data
        expected[:,-1,:,:] -= refhdu['SCI'].data
        result = np.allclose(expected, output_file['SCI'].data)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

class TestLinearityStep:
    """
    The base class for testing the Linearity.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("linearity", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("linearity", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs linearity input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("linearity", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("linearity", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs linearity output_file")

    @pytest.fixture(scope="class")
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_LINEAR'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Linearity Correction")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/linearity.rst")
                toctree.add_text('\t'+"linearity", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_linearity_correction(self, output_file, refhdu, input_file, request, chapter):
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
        corrected = np.logical_and(input_file['GROUPDQ'].data != 2, refhdu['DQ'].data != 2)
        
        linearity_applied = np.allclose(
            np.polyval(refhdu['COEFFS'].data[::-1], input_file['SCI'].data)[corrected], 
            output_file['SCI'].data[corrected])

        linearity_ignored = np.allclose(input_file['SCI'].data[~corrected], 
            output_file['SCI'].data[~corrected])

        # make sure that the values linearity correction is properly applied to relevant pixels
        # and ignored elsewhere
        result = linearity_applied and linearity_ignored
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    @pytest.fixture(scope="class")
    def _percent_rms(self, output_file):
        """
        Calculate the percent rms after fitting a line to the linearity corrected
        ramps.
        """
        nints, ngroups, nx, ny = output_file['SCI'].data.shape
        pixeldq = output_file['PIXELDQ'].data
        rms = np.zeros((nints, nx, ny))
        for i in range(nints):
            data = output_file['SCI'].data[i]
            groupdq = output_file['GROUPDQ'].data[i]
            groups = np.arange(data.shape[0])
            for (x,y), val in np.ndenumerate(data[0]):
                if x % 500 == 0 and y == 0:
                    print(x,y)
                usable = groupdq[:,x,y] == 0
                residuals = np.zeros(groupdq[0].shape)
                if usable.sum() > 4 and pixeldq[x,y] == 0: # make sure there are atleast 4 unsaturated groups
                    p = np.polyfit(groups[usable], data[:,x,y][usable], 1)
                    res = np.polyval(p, groups[usable]) - data[:,x,y][usable]
                    #residuals[usable] = res
                    rms[i, x,y] = np.std(res) / np.max(data[:,x,y][usable]) * 100

        return rms

    def test_linearity_median_residuals_rms_lt_1percent(self, _percent_rms, request, chapter):
        """
        Check that after the linearity correction the ramps agree with a linear 
        fit to an percent RMS of less than 1%.
        Where
        
        .. math::
            \%RMS = \\frac{F - F_c}{\max{F_c}} * 100
        
        """
        good = _percent_rms != 0
        result = np.median(_percent_rms[good]) < 1.
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    def test_linearity_99percent_of_residuals_rms_lt1percent(self, _percent_rms, request, chapter):
        """
        Check that more than 99% of pixels' residuals have percent RMS < 1%.
        """
        good = np.logical_and(_percent_rms != 0, ~np.isnan(_percent_rms))
        result = float(np.sum(_percent_rms[good] < 1.))/len(_percent_rms[good]) < 99.
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

    @pytest.mark.lastframe
    def test_linearity_pixeldq_propagation(self, output_file, refhdu, input_file, request, chapter):
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
        result =  np.all(bitwise_propagate(refhdu, input_file['PIXELDQ'].data) == output_file['PIXELDQ'].data)
        if pytest.config.getoption("--gen_report"):
            if result:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                chapter.add_text(request.function.__doc__)
            else:
                chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                chapter.add_text(request.function.__doc__)                

        assert result

class TestDarkCurrentStep:
    """
    The base class for testing the Dark Current Subtraction.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("dark_current", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("dark_current", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs dark_current input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("dark_current", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("dark_current", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs dark_current output_file")

    @pytest.fixture
    def refhdu(self, output_file):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+output_file[0].header['R_DARK'][7:]
        return fits.open(ref_file)

    @pytest.fixture(scope="class")
    def chapter(self, request, toctree):
        chapter = ReportChapter("Dark Current Correction")

        def cleanup():
            if pytest.config.getoption("--gen_report"):
                curdir = os.getcwd()
                config_dir = os.path.dirname(request.config.getoption("--config_file"))
                os.chdir(config_dir)
                chapter.write("source/dark_current.rst")
                toctree.add_text('\t'+"dark_current", extra_newline=False)
                os.chdir(curdir)

        request.addfinalizer(cleanup)
        return chapter

    def test_dark_current_subtraction(self, output_file, refhdu, input_file, request, chapter):
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

        nframes = output_file[0].header['NFRAMES']
        groupgap = output_file[0].header['GROUPGAP']
        nints, ngroups, nx, ny = output_file['SCI'].shape
        nframes_tot = (nframes+groupgap)*ngroups
        if nframes_tot > refhdu['SCI'].data.shape[0]:
            # data should remain unchanged if there are more frames in the 
            # science data than the reference file
            result = np.all(input_file['SCI'].data == output_file['SCI'].data)
            if pytest.config.getoption("--gen_report"):
                if result:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                    chapter.add_text(request.function.__doc__)
                else:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                    chapter.add_text(request.function.__doc__)                

            assert result
        else:
            dark_correct = np.zeros((nframes, ngroups, nx, ny))
            data = refhdu['SCI'].data[:nframes_tot, :, :]
            for i in range(nframes):
                dark_correct[i] = data[i::(nframes+groupgap),:,:]

            dark_correct = np.average(dark_correct, axis=0)
            result = input_file['SCI'].data - dark_correct
            result = np.allclose(result, output_file['SCI'].data)
            if pytest.config.getoption("--gen_report"):
                if result:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                    chapter.add_text(request.function.__doc__)
                else:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                    chapter.add_text(request.function.__doc__)                

            assert result

    def test_dark_current_pixeldq_propagation(self, output_file, refhdu, input_file, request, chapter):
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
        nframes = output_file[0].header['NFRAMES']
        groupgap = output_file[0].header['GROUPGAP']
        nints, ngroups, nx, ny = output_file['SCI'].shape
        nframes_tot = (nframes+groupgap)*ngroups
        if nframes_tot > refhdu['SCI'].data.shape[0]:
            result = np.all(input_file['PIXELDQ'].data == output_file['PIXELDQ'].data)
            if pytest.config.getoption("--gen_report"):
                if result:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                    chapter.add_text(request.function.__doc__)
                else:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                    chapter.add_text(request.function.__doc__)                

            assert result
        else:
            result = np.all(bitwise_propagate(refhdu, input_file['PIXELDQ'].data) == output_file['PIXELDQ'].data)
            if pytest.config.getoption("--gen_report"):
                if result:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` PASSED")
                    chapter.add_text(request.function.__doc__)
                else:
                    chapter.add_text(":py:meth:`"+request.function.__name__+"` FAILED")
                    chapter.add_text(request.function.__doc__)                

            assert result
            
class TestJumpStep:
    """
    The base class for testing Jump Detection.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("jump", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("jump", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs jump input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("jump", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("jump", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs jump output_file")


class TestRampFitStep:
    """
    The base class for testing Ramp Fitting.
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("ramp_fit", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("ramp_fit", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs ramp_fit input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("ramp_fit", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("ramp_fit", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs ramp_fit output_file")

# ##############################################################################
# ################################# 2B steps ###################################
# ##############################################################################

@pytest.mark.assign_wcs
class TestAssignWCSStep:
    """
    The base class for testing the assign_wcs step
    """

@pytest.mark.flat_field
class TestFlatFieldStep:
    """
    The base class for testing the flat_field step
    """
    @pytest.fixture(scope="class")
    def input_file(self, request, config):
        if  config.has_option("flat_field", "input_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("flat_field", "input_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs flat_field input_file")

    @pytest.fixture(scope="class")
    def output_file(self, request, config):
        if  config.has_option("flat_field", "output_file"):
            curdir = os.getcwd()
            config_dir = os.path.dirname(request.config.getoption("--config_file"))
            os.chdir(config_dir)
            hdu = fits.open(config.get("flat_field", "output_file"))
            os.chdir(curdir)
            return hdu
        else:
            pytest.skip("needs flat_field output_file")

    @pytest.fixture
    def refhdu(self, flat_field_hdu):
        CRDS = '/grp/crds/cache/references/jwst/'
        ref_file = CRDS+flat_field_hdu[0].header['R_FLAT'][7:]
        return fits.open(ref_file)

    def test_flat_field_correction(self, input_file, refhdu, output_file):
        """
        Check that the flat field correction is applied properly to the input file.
        The flat correction should divide the input data by the matching pixel values in the 
        reference file unless they are flagged in reference file DQ extension.
        """
        correct = refhdu['DQ'].data == 0
        expected_flat = input_file['SCI'].data
        expected_flat[correct] = input_file['SCI'].data[correct]/refhdu['SCI'].data[correct]
        assert np.all(output_file['SCI'].data  == expected_flat)

    def test_flat_field_dq(self, input_file, refhdu, output_file):
        """
        check that proper Data quality flags are added according to the reference file.

        NOTE: This fails in build 6.
        """
        assert np.all(bitwise_propagate(refhdu, input_file['DQ'].data) == output_file['DQ'].data)


@pytest.mark.persistence
class TestPersistenceStep:
    """
    The base class for testing the persistence step
    """

@pytest.mark.emission
class TestEmissionStep:
    """
    The base class for testing the emission step
    """

@pytest.mark.photom
class TestPhotomStep:
    """
    The base class for testing the photom step
    """
