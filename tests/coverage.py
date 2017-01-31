"""
Script to evaluate test coverage

`pip install coverage`
`coverage run coverage.py`
`coverage report`
"""

import unittest
from test_qidataset import *
from test_qidatafile import *
from test_qidatafile_conversion import *
from test_qidata_metadata_objects import *
from test_qidataobject import *

if __name__ == "__main__":
	fixtures.cleanData() # Remove traces of previous tests if they exist
	unittest.main(catchbreak=True)
