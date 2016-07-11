# -*- coding: utf-8 -*-

# Standard Library
import unittest
# Qidata
from qidata_file.qidatafile import QiDataFile
import xmp
from . import fixtures

class File(unittest.TestCase):
	def setUp(self):
		self.jpg_path = fixtures.sandboxed(fixtures.JPG_PHOTO)

	def test_contextmanager_noop(self):
		with QiDataFile(self.jpg_path):
			pass

	def test_metadata_attribute(self):
		with QiDataFile(self.jpg_path) as datafile:
			datafile.metadata

	def test_annotations_attribute(self):
		with QiDataFile(self.jpg_path) as datafile:
			datafile.annotations

class Metadata(unittest.TestCase):
	def setUp(self):
		self.jpg_data_item = QiDataFile(fixtures.sandboxed(fixtures.QIDATA_TEST_FILE))
		self.jpg_metadata = self.jpg_data_item.metadata

	def tearDown(self):
		self.jpg_data_item.close()




