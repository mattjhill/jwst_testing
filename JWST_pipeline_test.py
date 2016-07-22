import sys
from PIL import Image
import glob
from astropy.io import fits
import pytest

def get_file_names(arguments):
    """
    Takes arguments from the command line in order of <input> <expected output>
    and returns the names of both files; to be called by the testing suite file
    """
    if (len(arguments) == 1):
        #raw_input should be input in Python 3
        input_file = input("Enter the name of the input file: ")
        expected_output_file = input("Enter the name of the expected output file: ")
        print ("Running tests now...")
        return (input_file, expected_output_file)
    elif (len(arguments) == 3):
        input_file = arguments[1]
        expected_output_file = arguments[2]
        print ("Running tests now...")
        return (input_file, expected_output_file)
    else:
        print ("Please have the command line arguments organized as:\n"
        + "\tpython JWST_pipeline_test <input_file> <expected_output_file>")

def start_tests():
    pytest.main()


(input_file, expected_output_file) = get_file_names(sys.argv)
start_tests()
#start_tests(input_file, expected_output_file)
print (input_file, expected_output_file)
