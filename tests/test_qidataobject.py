# -*- coding: utf-8 -*-

# Standard Library
import unittest
import os

from qidata.qidataobject import QiDataObject
from qidata import qidatafile, qidataframe
import utilities

class QidataObjectTest(unittest.TestCase):
    def test_attributes(self):
        qidata_object = QiDataObject()
        with self.assertRaises(NotImplementedError):
            qidata_object.raw_data
        assert(qidata_object.metadata == dict())
        with self.assertRaises(NotImplementedError):
            qidata_object.type
        with self.assertRaises(NotImplementedError):
            qidata_object.read_only

class QiDataObjectImplem:
    def test_attributes(self):
        self.qidata_object.raw_data
        self.qidata_object.metadata
        self.qidata_object.type
        self.qidata_object.read_only

class QiDataFileAsObject(unittest.TestCase, QiDataObjectImplem):

    def setUp(self):
        self.jpg_path = utilities.sandboxed(utilities.JPG_PHOTO)
        self.qidata_object = qidatafile.open(self.jpg_path)

    def tearDown(self):
        self.qidata_object.close()

class QiDataFrameAsObject(unittest.TestCase, QiDataObjectImplem):

    def setUp(self):
        self.qidata_object = qidataframe.QiDataFrame.create(["a", "b"],".")

    def tearDown(self):
        self.qidata_object.close()
        os.remove(self.qidata_object._file_path)
