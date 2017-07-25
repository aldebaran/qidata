# -*- coding: utf-8 -*-

# Standard Library
import os
import pytest

# Local modules
from qidata import DataType
from qidata.qidatasensorobject import QiDataSensorObject
from qidata.qidataobject import ReadOnlyException
from qidata.metadata_objects import TimeStamp, Transform

def test_abstract():
	with pytest.raises(TypeError):
		qidata_object = QiDataSensorObject()

class SensorObjectForTests(QiDataSensorObject):
	@property
	def raw_data(self):
		return None

	@property
	def read_only(self):
		return False

	@property
	def type(self):
		return QiDataSensorObject.type.fget(self)

	@type.setter
	def type(self, new_type):
		QiDataSensorObject.type.fset(self, new_type)

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

class ReadOnlySensorObjectForTests(QiDataSensorObject):
	@property
	def raw_data(self):
		return None

	@property
	def read_only(self):
		return True

	@property
	def type(self):
		return QiDataSensorObject.type.fget(self)

	@type.setter
	def type(self, new_type):
		QiDataSensorObject.type.fset(self, new_type)

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

def test_qidata_sensor_object():
	qidata_object = SensorObjectForTests()
	ro_qidata_object = ReadOnlySensorObjectForTests()

	# Make sure there is a default timestamp
	assert(TimeStamp(0,0) == qidata_object.timestamp)
	pos = qidata_object.position
	assert(0 == pos.translation.x)
	assert(0 == pos.translation.y)
	assert(0 == pos.translation.z)
	assert(0 == pos.rotation.x)
	assert(0 == pos.rotation.y)
	assert(0 == pos.rotation.z)
	assert(1 == pos.rotation.w)

	# Make sure timestamp can be set
	qidata_object.timestamp = TimeStamp(10,0)
	assert(TimeStamp(10,0) == qidata_object.timestamp)

	with pytest.raises(TypeError):
		qidata_object.timestamp = (15,)

	# But not in read-only
	with pytest.raises(ReadOnlyException):
		ro_qidata_object.timestamp = TimeStamp(10,0)

	with pytest.raises(ReadOnlyException):
		ro_qidata_object.position = Transform()

	with pytest.raises(ReadOnlyException):
		ro_qidata_object.type = DataType.AUDIO

	assert(None == qidata_object.type)
	qidata_object.type = DataType.IMAGE_2D
	assert(DataType.IMAGE_2D == qidata_object.type)
	qidata_object.type = "IMAGE_2D"
	assert(DataType.IMAGE_2D == qidata_object.type)
	with pytest.raises(TypeError):
		qidata_object.type = "BLABLABLA"