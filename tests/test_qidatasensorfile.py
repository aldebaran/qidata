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

# Third-party libraries
import pytest

# Local modules
from qidata.qidatasensorfile import QiDataSensorFile
from qidata import metadata_objects,DataType, qidatafile
from qidata import QiDataFile, ClosedFileException

# Test
# import conftest

def test_abstract():
	with pytest.raises(TypeError):
		qidata_object = QiDataSensorFile()

class SensorFileForTests(QiDataSensorFile):
	@property
	def type(self):
		return QiDataSensorFile.type.fget(self)

	@type.setter
	def type(self, new_type):
		QiDataSensorFile.type.fset(self, new_type)

	@property
	def raw_data(self):
		return None

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

def test_qidata_sensor_file(jpg_file_path):
	# Open file in "w" mode and add annotation
	ts=metadata_objects.TimeStamp(1000, 2)
	p=metadata_objects.Transform(
	                             translation=dict(x=10,y=15,z=-2),
	                             rotation=dict(x=0,y=0,z=0,w=1)
	                            )
	with SensorFileForTests(jpg_file_path, "w") as f:
		f.timestamp = ts
		f.transform = p
		f.type = DataType.AUDIO

	with SensorFileForTests(jpg_file_path, "r") as f:
		assert(ts == f.timestamp)
		assert(p == f.transform)
		assert(DataType.AUDIO == f.type)
