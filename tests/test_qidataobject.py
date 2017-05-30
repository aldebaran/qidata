# -*- coding: utf-8 -*-

# Standard Library
import unittest

from qidata.qidataobject import QiDataObject
from qidata import qidatafile
import utilities

class QidataObjectTest(unittest.TestCase):
    def test_attributes(self):
        qidata_object = QiDataObject()
        with self.assertRaises(NotImplementedError):
            qidata_object.raw_data
        assert(qidata_object.metadata == dict())
        with self.assertRaises(NotImplementedError):
            qidata_object.type

class QiDataObjectImplem:
    def test_attributes(self):
        self.qidata_object.raw_data
        self.qidata_object.metadata
        self.qidata_object.type

class QiDataFileAsObject(unittest.TestCase, QiDataObjectImplem):

    def setUp(self):
        self.jpg_path = utilities.sandboxed(utilities.JPG_PHOTO)
        self.qidata_object = qidatafile.open(self.jpg_path)

    def tearDown(self):
        self.qidata_object.close()
