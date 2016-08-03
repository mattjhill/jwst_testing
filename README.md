# ST_Validate
JWST Pipeline Validation

To run this application:
  - go into set_valies.cfg
  - find the test(s) you want to run, it will be inside brackets
  - below the brackets, set the {}_file equal to the input file you want to be tested
    - this will look like: dq_init_file = jw00036001001_01101_00001_NRCA1_uncal_DQInitStep.fits
  - when you have initiated the steps you want tested, run:
    - python JWST_pipeline_test.py
