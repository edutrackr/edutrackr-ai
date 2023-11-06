import os
import sys

app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)

###

import unittest
from api.common.utils.runtime import has_arg


def suite():
    return unittest\
        .TestLoader()\
        .discover(
            start_dir="tests", 
            pattern="*_test.py"
        )

if __name__ == '__main__':
    verbose = has_arg("-v") or has_arg("--verbose")
    verbosity_level = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity_level)
    runner.run(suite())
