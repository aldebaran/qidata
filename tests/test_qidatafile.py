# -*- coding: utf-8 -*-

# Standard Library
import unittest
# Qidata
from qidata.files import qidatafile
import qidata.files
import fixtures

class FileTools(unittest.TestCase):
	def test_support(self):
		assert(qidata.files.isSupported("./toto.png"))
		assert(not qidata.files.isSupported(""))

class File(unittest.TestCase):
	def setUp(self):
		self.jpg_path = fixtures.sandboxed(fixtures.JPG_PHOTO)

	def test_contextmanager_noop(self):
		with qidatafile.open(self.jpg_path):
			pass

	def test_metadata_attribute(self):
		with qidatafile.open(self.jpg_path) as datafile:
			datafile.raw_metadata

	def test_annotations_attribute(self):
		with qidatafile.open(self.jpg_path) as datafile:
			datafile.metadata

	def test_annotators_attribute(self):
		with qidatafile.open(self.jpg_path) as datafile:
			datafile.annotators

class MetadataReading(unittest.TestCase):
	def setUp(self):
		self.jpg_data_path = fixtures.sandboxed(fixtures.QIDATA_TEST_FILE)
		self.jpg_data_item = qidatafile.open(self.jpg_data_path)
		self.jpg_metadata = self.jpg_data_item.raw_metadata

	def tearDown(self):
		self.jpg_data_item.close()

	def test_annotations(self):
		fixtures.verifyAnnotations(self.jpg_data_item, "sambrose")

	def test_annotators(self):
		annotators = self.jpg_data_item.annotators
		assert(annotators == ["sambrose"])

	def test_modification_readonly(self):
		from qidata.metadata_objects import Person
		annotations = self.jpg_data_item.metadata
		test_person = [Person("name", 1), [[1.0, 2.0],[20.0, 25.0]]]
		annotations["jdoe"]=dict()
		annotations["jdoe"]["Person"]=[test_person]
		self.jpg_data_item.save()
		self.jpg_data_item.close()
		self.jpg_data_item = qidatafile.open(self.jpg_data_path)

		fixtures.verifyAnnotations(self.jpg_data_item, "sambrose")

class MetadataWriting(unittest.TestCase):
	def setUp(self):
		self.jpg_data_path = fixtures.sandboxed(fixtures.QIDATA_TEST_FILE)
		self.jpg_data_item = qidatafile.open(self.jpg_data_path, "w")
		self.jpg_metadata = self.jpg_data_item.raw_metadata

	def test_modification(self):
		from qidata.metadata_objects import Person
		annotations = self.jpg_data_item.metadata
		test_person = [Person("name", 1), [[1.0, 2.0],[20.0, 25.0]]]
		annotations["jdoe"]=dict()
		annotations["jdoe"]["Person"]=[test_person]
		self.jpg_data_item.save()
		self.jpg_data_item.close()
		self.jpg_data_item = qidatafile.open(self.jpg_data_path)

		annotations = self.jpg_data_item.metadata
		assert(annotations.has_key("jdoe"))
		assert(annotations["jdoe"].has_key("Person"))
		assert(len(annotations["jdoe"]["Person"][0])==2)
		assert(isinstance(annotations["jdoe"]["Person"][0][0], Person))
		person = annotations["jdoe"]["Person"][0][0]
		location = annotations["jdoe"]["Person"][0][1]
		assert(person.id == 1)
		assert(person.name == "name")
		assert(location == [[1.0, 2.0],[20.0, 25.0]])

	def test_deletion(self):
		annotations = self.jpg_data_item.metadata
		for annotator in annotations.keys():
			annotations.pop(annotator)
		self.jpg_data_item.save()
		self.jpg_data_item.close()
		self.jpg_data_item = qidatafile.open(self.jpg_data_path)

		annotations = self.jpg_data_item.metadata
		assert(not annotations.has_key("sambrose"))

	def test_reload(self):
		from qidata.metadata_objects import Person
		annotations = self.jpg_data_item.metadata
		test_person = [Person("name", 1), [[1.0, 2.0],[20.0, 25.0]]]
		annotations["jdoe"]=dict()
		annotations["jdoe"]["Person"]=[test_person]
		assert(self.jpg_data_item.metadata.has_key("jdoe"))
		self.jpg_data_item.load()
		assert(not self.jpg_data_item.metadata.has_key("jdoe"))

class MetadataTestCases(unittest.TestCase):
	def setUp(self):
		self.jpg_data_path = fixtures.sandboxed(fixtures.QIDATA_TEST_FILE)
		self.jpg_data_item = qidatafile.open(self.jpg_data_path, "w")
		self.jpg_metadata = self.jpg_data_item.raw_metadata

	def test_general_annotation(self):
		"""
		This test checks if it is possible to add an annotation without
		specific location (annotation to the whole file)
		"""
		from qidata.metadata_objects import Person
		annotations = self.jpg_data_item.metadata
		test_person = [Person("name", 1), None]
		annotations["jdoe"]=dict()
		annotations["jdoe"]["Person"]=[test_person]
		self.jpg_data_item.save()
		self.jpg_data_item.close()
		self.jpg_data_item = qidatafile.open(self.jpg_data_path)

		annotations = self.jpg_data_item.metadata
		assert(annotations.has_key("jdoe"))
		assert(annotations["jdoe"].has_key("Person"))
		assert(len(annotations["jdoe"]["Person"][0])==2)
		assert(isinstance(annotations["jdoe"]["Person"][0][0], Person))
		person = annotations["jdoe"]["Person"][0][0]
		location = annotations["jdoe"]["Person"][0][1]
		assert(person.id == 1)
		assert(person.name == "name")
		assert(location == None)
