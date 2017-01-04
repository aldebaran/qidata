# -*- coding: utf-8 -*-

# Standard Library
import unittest
# Qidata
from qidata.files.qidatafile import QiDataFile
from qidata.files.version import identifyFileAnnotationVersion
from qidata.files.conversion import *
import xmp
import fixtures
from qidata.metadata_objects import Person

class FileConversion(unittest.TestCase):
	def setUp(self):
		self.vN_path = fixtures.sandboxed(fixtures.JPG_PHOTO)
		self.v1_path = fixtures.sandboxed(fixtures.QIDATA_V1)
		self.v2_path = fixtures.sandboxed(fixtures.QIDATA_V2)
		self.v3_path = fixtures.sandboxed(fixtures.QIDATA_V3)

	def test_identify_version(self):
		assert(identifyFileAnnotationVersion(self.v1_path)=="0.1")
		assert(identifyFileAnnotationVersion(self.v2_path)=="0.2")
		assert(identifyFileAnnotationVersion(self.v3_path)=="1.0")
		assert(identifyFileAnnotationVersion(self.vN_path)==None)

	def test_conversion_from_unannotated(self):
		orig_sha1 = fixtures.sha1(self.vN_path)
		qidataFileConversionToCurrentVersion(self.vN_path, None)
		new_sha1 = fixtures.sha1(self.vN_path)
		assert(orig_sha1 == new_sha1)

	def test_conversion_from_v1(self):
		qidataFileConversionToCurrentVersion(self.v1_path, dict(annotator="sambrose"))
		qidata_file = QiDataFile(self.v1_path)
		fixtures.verifyAnnotations(qidata_file, "sambrose")
		assert(len(qidata_file.annotators)==1)

	def test_conversion_from_v1_with_missing_argument(self):
		with self.assertRaises(TypeError):
			qidataFileConversionToCurrentVersion(self.v1_path)

	def test_conversion_from_v1_with_bad_argument(self):
		with self.assertRaises(TypeError):
			qidataFileConversionToCurrentVersion(self.v1_path, dict(annotator=0))

	def test_conversion_from_v2(self):
		qidataFileConversionToCurrentVersion(self.v2_path)
		qidata_file = QiDataFile(self.v2_path)
		fixtures.verifyAnnotations(qidata_file, "sambrose")

	def test_conversion_from_v3(self):
		orig_sha1 = fixtures.sha1(self.v3_path)
		qidataFileConversionToCurrentVersion(self.v3_path)
		qidata_file = QiDataFile(self.v3_path)
		fixtures.verifyAnnotations(qidata_file, "sambrose")
		new_sha1 = fixtures.sha1(self.v3_path)
		assert(orig_sha1 == new_sha1)