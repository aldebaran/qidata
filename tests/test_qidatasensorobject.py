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
	pos = qidata_object.transform
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
		ro_qidata_object.transform = Transform()

	with pytest.raises(ReadOnlyException):
		ro_qidata_object.type = DataType.AUDIO

	assert(None == qidata_object.type)
	qidata_object.type = DataType.IMAGE_2D
	assert(DataType.IMAGE_2D == qidata_object.type)
	qidata_object.type = "IMAGE_2D"
	assert(DataType.IMAGE_2D == qidata_object.type)
	with pytest.raises(TypeError):
		qidata_object.type = "BLABLABLA"