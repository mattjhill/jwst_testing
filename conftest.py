"""
Configuration file for py.test
"""

import pytest

def pytest_addoption(parser):
	parser.addoption("--skip_dq_init", action="store_true", 
		help="skip the dq_init step tests")
	parser.addoption("--runslow", action="store_true",
		help="run slow tests")

def pytest_runtest_setup(item):
	if 'dq_init' in item.keywords and item.config.getvalue("--skip_dq_init"):
		pytest.skip("skipping dq_init tests")
	if 'slow' in item.keywords and not item.config.getvalue("runslow"):
		pytest.skip("need --runslow option to run")

def pytest_configure(config):
    import sys
    sys._called_from_test = True

def pytest_unconfigure(config):
    import sys  # This was missing from the manual
    del sys._called_from_test
