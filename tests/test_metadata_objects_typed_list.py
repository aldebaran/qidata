# -*- coding: utf-8 -*-

# Standard Library
import unittest

from qidata.metadata_objects import TypedList

class TypedListTest(unittest.TestCase):

    def setUp(self):
        self.typed_list = TypedList(str, args=["test"])
        self.alt_list_a = TypedList(int, args=[0])
        self.alt_list_b = TypedList(str, args=["test", "test"])
        self.alt_list_c = TypedList(str, args=["test0"])
        self.alt_list_d = TypedList(str, args=["test"])

    def test_list_functions(self):
        assert(self.typed_list.typename == str)
        assert(self.alt_list_a.typename == int)
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

    def test_list_equality(self):
        assert(self.typed_list != ["test"])
        assert(self.typed_list != self.alt_list_a)
        assert(self.typed_list != self.alt_list_b)
        assert(self.typed_list != self.alt_list_c)
        assert(self.typed_list == self.alt_list_d)
