from setuptools import setup, find_packages

try:
    import relic.release
except ImportError:
    print('This package requires RELIC ("Release I Control"):')
    print('  pip install relic')
    exit(1)

version = relic.release.get_info()
relic.release.write_template(version, 'jwst_testing')

setup(
    name = "jwst_testing",
    version=version.pep386,
    packages = find_packages(),
    entry_points = {
        'console_scripts' : [
            'test_jwst_single = jwst_testing.runners:run_tests_single',
            'test_jwst_batch = jwst_testing.runners:run_tests_batch'
        ]
    },
    install_requires = ['relic', 'pytest-html'],
    zip_safe = False,
    )