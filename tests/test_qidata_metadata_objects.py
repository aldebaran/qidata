# -*- coding: utf-8 -*-

# Standard Library
import unittest

from qidata import makeMetadataObject, MetadataType
from qidata.metadata_objects import *

class MetadataObjects(unittest.TestCase):

    def test_make_non_existing_metadata_object(self):
        with self.assertRaises(TypeError):
            created_object = makeMetadataObject("")


class MetadataObjectsBase(unittest.TestCase):

    def test_attributes(self):
        for metadata_type in list(MetadataType):
            created_object = makeMetadataObject(metadata_type)
            copied_object = makeMetadataObject(metadata_type, created_object)
            assert(created_object == copied_object)

            # Check it is accessible and does not raise
            created_object.version

class MetadataObjectBaseImplemented():
    def test_make_default_object(self):
        def_object = self.type()

    def test_copy_object(self):
        copy = self.type(self.instance)
        assert(copy == self.instance)

    def test_too_many_arguments(self):
        args = []
        for attrib in self.type.__ATTRIBUTES__:
            args.append(getattr(self.instance, attrib.id))
        args.append(0)
        with self.assertRaises(TypeError):
            self.type(*args)

    def test_wrong_keys(self):
        with self.assertRaises(TypeError):
            self.type(aspcfgbenrgahreb=0)

    def test_import_from_old_versions(self):
        for input_dict, gnd in zip(self.inputs, self.outputs):
            output_object = self.type.fromDict(input_dict)
            assert(output_object == gnd)

class PersonTest(unittest.TestCase, MetadataObjectBaseImplemented):
    def setUp(self):
        self.type=Person
        self.instance = Person("Pepper")
        self.inputs = [{"name":"Pepper", "id":10, "version":"0.1"}]
        self.outputs = [Person("Pepper")]

class SpeechTest(unittest.TestCase, MetadataObjectBaseImplemented):
    def setUp(self):
        self.type=Speech
        self.instance = Speech("Pepper", "Hello, I'm Pepper")
        self.inputs = [{"name":"Pepper", "sentence":"Hello world", "id":10, "version":"0.1"}]
        self.outputs = [Speech("Pepper", "Hello world")]

class ObjectTest(unittest.TestCase, MetadataObjectBaseImplemented):
    def setUp(self):
        self.type=Object
        self.instance = Object("qrcode", "10", 1)
        self.inputs = [{"type":"qrcode", "value":"Hello!", "id":10, "version":"0.1"}]
        self.outputs = [Object("qrcode", "Hello!", 10)]

class FaceTest(unittest.TestCase, MetadataObjectBaseImplemented):

    def setUp(self):
        from qidata.metadata_objects.face import FacialPart
        self.type=Face
        self.instance = Face("Pepper", 12)
        self.inputs = [
            {
                "name":"Pepper",
                "id":10,
                "version":"0.1"},
            {
                "name":"gszwarc",
                "fid":0,
                "age":27,
                "expression":[0.140624997439,
                              0.223124995478,
                              0.0318749987055,
                              0.247499989579,
                              0.356874989346],
                "facial_parts":[
                                [[98, 53], 0.175687507952],
                                [[130, 60], 0.0129375002653],
                                [[124, 106], 0.0884375025926],
                                [[105, 58], 0.175687507952],
                                [[89, 54], 0.175687507952],
                                [[123, 61], 0.0129375002653],
                                [[134, 62], 0.0129375002653],
                                [[100, 105], 0.0884375025926],
                                [[131, 109], 0.0884375025926],
                                [[114, 83], 0.242000014216],
                                [[128, 85], 0.242000014216],
                                [[125, 96], 0.0884375025926]
                               ],
                "gender":"male",
                "smile":[0.394999994896,0.0751250039757],
                "version":"0.2"
            }
        ]
        self.outputs = [
            Face("Pepper", 0),
            Face("gszwarc",27,
                expression=[0.140624997439,
                              0.223124995478,
                              0.0318749987055,
                              0.247499989579,
                              0.356874989346],
                facial_parts=[
                                FacialPart([98, 53], 0.175687507952),
                                FacialPart([130, 60], 0.0129375002653),
                                FacialPart([124, 106], 0.0884375025926),
                                FacialPart([105, 58], 0.175687507952),
                                FacialPart([89, 54], 0.175687507952),
                                FacialPart([123, 61], 0.0129375002653),
                                FacialPart([134, 62], 0.0129375002653),
                                FacialPart([100, 105], 0.0884375025926),
                                FacialPart([131, 109], 0.0884375025926),
                                FacialPart([114, 83], 0.242000014216),
                                FacialPart([128, 85], 0.242000014216),
                                FacialPart([125, 96], 0.0884375025926)
                              ],
                gender="male",
                smile=[0.394999994896,0.0751250039757],
            )
        ]

class ContextTest(unittest.TestCase, MetadataObjectBaseImplemented):
    def setUp(self):
        self.type=Context
        self.instance = Context()
        self.inputs = [dict()]
        self.outputs = [Context()]