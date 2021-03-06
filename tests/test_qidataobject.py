# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard Library
import os
import pytest

# Local modules
from qidata.qidataobject import QiDataObject, ReadOnlyException
from qidata import metadata_objects

def test_abstract():
	with pytest.raises(TypeError):
		qidata_object = QiDataObject()

class ObjectForTests(QiDataObject):
	@property
	def raw_data(self):
		return None

	@property
	def read_only(self):
		return False

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

class ReadOnlyObjectForTests(QiDataObject):
	@property
	def raw_data(self):
		return None

	@property
	def read_only(self):
		return True

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

class ReadOnlyObjectWithAnnotationsForTests(QiDataObject):

	def __init__(self):
		self._annotations = dict(
		  jdoe=dict(
		    Property=[
		      [metadata_objects.Property(key="prop", value="11"), 0]
		    ]
		  ),
		)

	@property
	def raw_data(self):
		return None

	@property
	def read_only(self):
		return True

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

class FakeAnnotation():
	pass

class AnotherFakeAnnotation(metadata_objects.MetadataObject):
	pass

class Property(object):
	pass

def test_qidata_object():
	qidata_object = ObjectForTests()

	# Annotations should be empty
	assert(dict() == qidata_object.annotations)

	# They should stay empty when modifying the returned dict
	annotations = qidata_object.annotations
	annotations["test"] = 0
	assert(dict() == qidata_object.annotations)

	# Annotation is not settable
	with pytest.raises(AttributeError):
		qidata_object.annotations = annotations

	# But it is still possible to add annotations
	qidata_object.addAnnotation(
	  "jdoe",
	  metadata_objects.Property(key="test", value="0"),
	  None
	)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[[metadata_objects.Property(key="test", value="0"), None]],
	    ),
	  ) == qidata_object.annotations
	)
	assert(["jdoe"] == qidata_object.annotators)

	# However, only real metadata can be passed
	with pytest.raises(TypeError):
		qidata_object.addAnnotation("jdoe", FakeAnnotation(), None)

	with pytest.raises(TypeError):
		qidata_object.addAnnotation("jdoe", Property(), None)

	with pytest.raises(TypeError):
		qidata_object.addAnnotation("jdoe", AnotherFakeAnnotation(), None)

	# Make sure Context, TimeStamp and Transform cannot be added, as they are
	# reserved for special purposes
	with pytest.raises(TypeError):
		qidata_object.addAnnotation("jdoe", metadata_objects.Context(), None)

	with pytest.raises(TypeError):
		qidata_object.addAnnotation("jdoe", metadata_objects.Transform(), None)

	with pytest.raises(TypeError):
		qidata_object.addAnnotation("jdoe", metadata_objects.TimeStamp(), None)

	# And the given location must be validated by our object
	with pytest.raises(Exception):
		qidata_object.addAnnotation(
		  "jdoe",
		  metadata_objects.Property(key="test", value="0"),
		  -1
		)

	# Once added, we can still modify an annotation by changing the one on our
	# side
	a=metadata_objects.Property(key="another_prop", value="10")
	qidata_object.addAnnotation("jdoe", a, None)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="test", value="0"), None],
	        [metadata_objects.Property(key="another_prop", value="10"), None]
	      ],
	    ),
	  ) == qidata_object.annotations
	)
	a.value = 11
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="test", value="0"), None],
	        [metadata_objects.Property(key="another_prop", value="11"), None]
	      ],
	    ),
	  ) == qidata_object.annotations
	)

	# And it can also be removed
	qidata_object.removeAnnotation("jdoe",a)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="test", value="0"), None],
	      ],
	    ),
	  ) == qidata_object.annotations
	)

	# Add the same annotation multiple times, at different locations
	qidata_object.addAnnotation("jdoe", a, 0)
	qidata_object.addAnnotation("jdoe", a, 1)
	qidata_object.addAnnotation("jdoe", a, 0)
	qidata_object.addAnnotation("jdoe", a, None)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="test", value="0"), None],
	        [metadata_objects.Property(key="another_prop", value="11"), 0],
	        [metadata_objects.Property(key="another_prop", value="11"), 1],
	        [metadata_objects.Property(key="another_prop", value="11"), 0],
	        [metadata_objects.Property(key="another_prop", value="11"), None],
	      ],
	    ),
	  ) == qidata_object.annotations
	)
	qidata_object.removeAnnotation("jdoe",a)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="test", value="0"), None],
	        [metadata_objects.Property(key="another_prop", value="11"), 0],
	        [metadata_objects.Property(key="another_prop", value="11"), 1],
	        [metadata_objects.Property(key="another_prop", value="11"), 0],
	      ],
	    ),
	  ) == qidata_object.annotations
	)
	qidata_object.removeAnnotation("jdoe",a)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="test", value="0"), None],
	        [metadata_objects.Property(key="another_prop", value="11"), 1],
	        [metadata_objects.Property(key="another_prop", value="11"), 0],
	      ],
	    ),
	  ) == qidata_object.annotations
	)

	# Trying to remove stuff at the wrong location raises
	with pytest.raises(ValueError):
		qidata_object.removeAnnotation(
		  "jdoe",
		  metadata_objects.Property(key="test", value="0"),
		  0
		)
	with pytest.raises(ValueError):
		qidata_object.removeAnnotation("jdoe",a,2)

	# Trying to remove other things raises exceptions
	with pytest.raises(TypeError):
		qidata_object.removeAnnotation("jdoe",FakeAnnotation())

	with pytest.raises(TypeError):
		qidata_object.removeAnnotation("jdoe",Property())

	with pytest.raises(ValueError):
		qidata_object.removeAnnotation("jsmith",a)

	# When the last object is removed, empty sections are removed
	qidata_object.removeAnnotation("jdoe",a)
	qidata_object.removeAnnotation(
	  "jdoe",
	  metadata_objects.Property(key="test", value="0")
	)
	qidata_object.removeAnnotation("jdoe",a)
	assert(
	  dict() == qidata_object.annotations
	)
	qidata_object.addAnnotation("jdoe", a, 0)
	qidata_object.removeAnnotation("jdoe", a, 0)
	assert(
	  dict() == qidata_object.annotations
	)

	b=metadata_objects.Object("qrcode", "10", 1)
	qidata_object.addAnnotation("jdoe", b, 0)
	with pytest.raises(ValueError):
		qidata_object.removeAnnotation("jdoe", a, 0)
	qidata_object.addAnnotation("jdoe", a, 0)

	assert(
	  dict(
	    jdoe=dict(
	      Object=[
	        [b, 0],
	      ],
	      Property=[
	        [a, 0]
	      ]
	    ),
	  ) == qidata_object.annotations
	)

	assert([] == qidata_object.getAnnotations("jsmith"))
	assert([] == qidata_object.getAnnotations("jdoe", "Face"))

	with pytest.raises(TypeError):
		qidata_object.getAnnotations("jdoe", "Toto")

	jdoe_annotations = qidata_object.getAnnotations("jdoe")
	assert(2 == len(jdoe_annotations))
	jdoe_annotations = qidata_object.getAnnotations("jdoe", "Property")
	assert(1 == len(jdoe_annotations))
	jdoe_prop = jdoe_annotations[0][0]
	jdoe_prop.key = "better_key"
	print qidata_object
	assert(
	  dict(
	    jdoe=dict(
	      Object=[
	        [b, 0],
	      ],
	      Property=[
	        [metadata_objects.Property(key="better_key", value="11"), 0]
	      ]
	    ),
	  ) == qidata_object.annotations
	)

def test_qidata_object_extra():
	qidata_object = ObjectForTests()

	# If we start by adding an annotation, everything should be fine
	qidata_object.addAnnotation("jdoe", metadata_objects.Property(key="test", value="0"), None)
	assert(
	  dict(
	    jdoe=dict(
	      Property=[[metadata_objects.Property(key="test", value="0"), None]],
	    ),
	  ) == qidata_object.annotations
	)

def test_read_only_qidata_object():
	qidata_object = ReadOnlyObjectForTests()

	# Make sure "add" and "remove" cannot be used
	a=metadata_objects.Property(key="another_prop", value="10")
	with pytest.raises(ReadOnlyException):
		qidata_object.addAnnotation("jdoe", a, None)
	with pytest.raises(ReadOnlyException):
		qidata_object.removeAnnotation("jdoe", a, None)

def test_read_only_cannot_be_modified():
	qidata_object = ReadOnlyObjectWithAnnotationsForTests()

	jdoe_annotations = qidata_object.getAnnotations("jdoe", "Property")
	assert(1 == len(jdoe_annotations))
	jdoe_prop = jdoe_annotations[0][0]
	jdoe_prop.key = "better_key"
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="prop", value="11"), 0]
	      ]
	    ),
	  ) == qidata_object.annotations
	)