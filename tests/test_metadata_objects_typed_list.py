# -*- coding: utf-8 -*-

# Standard Library
import unittest

from qidata.metadata_objects import TypedList

class TypedListTest(unittest.TestCase):

    def setUp(self):
        self.typed_list = TypedList(str, args=["test"])

    def test_list_functions(self):
        assert(len(self.typed_list) == 1)
        assert(self.typed_list.pop() == "test")
        assert(len(self.typed_list) == 0)

    def test_list_append_element(self):
        self.typed_list.appendDefault()
        assert(len(self.typed_list) == 2)

        self.typed_list.append("test2")
        assert(len(self.typed_list) == 3)

        with self.assertRaises(TypeError):
            self.typed_list.append(0)
        assert(len(self.typed_list) == 3)
