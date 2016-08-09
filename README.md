# ST_Validate
JWST Pipeline Validation

To run this application:
  - Go into set_values.cfg
  - Find the test(s) you want to run, it will be inside brackets
  - Below the brackets, set the {}_file equal to the input file you want to be tested
    - this will look like: dq_init_file = jw00036001001_01101_00001_NRCA1_uncal_DQInitStep.fits
  - If you would like to run multiple files for the same step of the pipeline:
    - For each file you want to test, create a new copy of set_values.cfg and change it accordingly
    - If you will not run a certain step, leave the _file = None
  - When you have initiated the steps you want tested, run:
    - python st_validate.py {your_config_here}
