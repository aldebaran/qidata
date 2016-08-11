# -*- coding: utf-8 -*-

# Standard Library
import unittest

from qidata.metadata_objects import makeMetadataObject, MetadataObjectBase
from qidata.types import MetadataType

class MetadataObjects(unittest.TestCase):

    def test_make_non_existing_metadata_object(self):
        with self.assertRaises(TypeError):
            created_object = makeMetadataObject("")


class MetadataObjectsBase(unittest.TestCase):

    def test_attributes(self):
        metadata_base = MetadataObjectBase()
        with self.assertRaises(NotImplementedError):
            metadata_base.toDict()
        with self.assertRaises(NotImplementedError):
            MetadataObjectBase.fromDict()

        for metadata_type in list(MetadataType):
            created_object = makeMetadataObject(metadata_type)
            makeMetadataObject(metadata_type, created_object.toDict())
