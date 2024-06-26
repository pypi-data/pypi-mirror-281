from test_extract_assembly import *
from test_atp import *
from test_generation import *
from test_reader import *
import unittest
import warnings

def run_all():
    unittest.main()

def clear_tests():
    os.system("rm -rf test/asm/test/generation/*") # clear files

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_all()