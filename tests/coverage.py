"""
Script to evaluate test coverage

`pip install coverage`
`coverage run coverage.py`
`coverage report`
"""

import unittest
from test_qidatafile import *
from test_qidatafile_conversion import *

if __name__ == "__main__":
	unittest.main()
