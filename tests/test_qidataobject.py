# -*- coding: utf-8 -*-

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

	b=metadata_objects.TimeStamp(seconds=0, nanoseconds=1)
	qidata_object.addAnnotation("jdoe", b, 0)
	with pytest.raises(ValueError):
		qidata_object.removeAnnotation("jdoe", a, 0)

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