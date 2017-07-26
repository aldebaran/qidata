# -*- coding: utf-8 -*-

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
