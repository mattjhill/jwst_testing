"""
This module contains the validation testing for the JWST Calibration
Pipeline.
"""

__docformat__ = 'reStructuredText'

from astropy.io import fits
import numpy as np
import unittest
import sys
import pytest
dq_init = pytest.mark.dq_init
slow = pytest.mark.slow


@dq_init
class Test_dq_init(unittest.TestCase):
	"""
	The base class for testing the dq_init step.
	"""
	# from jwst_pipeline.dq_init import DQInitStep

	# dq_init = DQInitStep.call(
	# 	"data/jw00017001001_01101_00001_NRCA1_uncal.fits", 
	# 	config_file="data/cfgs/dq_init.cfg")	

	if hasattr(sys, '_called_from_test'):
		# called from within a test run
		dq_init = fits.open(
		"data/jw00017001001_01101_00001_NRCA1_uncal_dq_init.fits")

	else:
		pass
	# called "normally"


	def test_groupdq_exists(self):
		"""
		Checks that the groupdq has been set.
		"""
		# if using object from pipeline
		# assert(hasattr(self.dq_init., 'groupdq'))

		# if using fits file generated by strun
		assert("GROUPDQ" in self.dq_init)

	def test_groupdq_vals(self):
		"""
		Checks that the groupdq extension 
		values are all zero after dq_init.
		"""
		# if using object from pipeline
		# assert(np.all(self.dq_init.groupdq == 0))

		# if using fits file generated by strun
		assert(np.all(self.dq_init["GROUPDQ"].data == p))


	def test_err_exists(self):
		"""
		Check that all err extension values are all zero.
		"""

		# if using object from pipeline
		# assert(hasattr(self.dq_init, 'err'))
		# if using fits file generated by strun
		assert("ERR" in self.dq_init)

	def test_err_vals(self):
		"""
		Check that all err extension values are all zero.
		"""

		# if using object from pipeline
		# assert(np.all(self.dq_init.pixeldq == 0))

		# if using fits file generated by strun
		assert(np.all(self.dq_init["ERR"].data == 0))


class TestClassExample:
	"""
	a test class
	"""
	@slow
	def test_foo(self):
		assert(True)

	def test_bar(self):
		assert(True)

