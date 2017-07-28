# -*- coding: utf-8 -*-

# Standard libraries
import os

# Third-party libraries
import pytest

# Local modules
from qidata import metadata_objects,DataType, qidatafile
from qidata import QiDataFile, ClosedFileException
from qidata.qidataimagefile import QiDataImageFile
from qidata.qidataaudiofile import QiDataAudioFile

# Test
import conftest

def test_abstract():
	with pytest.raises(TypeError):
		qidata_object = QiDataFile()

class FileForTests(QiDataFile):
	@property
	def type(self): return DataType.AUDIO

	@type.setter
	def type(self, new_type): return

	@property
	def raw_data(self):
		return None

	def _isLocationValid(self, location):
		return (location is None or location >= 0)

def test_file_read_and_write(jpg_with_external_annotations,
                             jpg_with_internal_annotations):
	with FileForTests(jpg_with_external_annotations, "r") as f:
		assert(
		  {
		    "sambrose":{
		      "Property":[
		        [metadata_objects.Property("key", "value"), None]
		      ]
		    }
		  } == f.annotations
		)

	with FileForTests(jpg_with_internal_annotations, "r") as f:
		assert(
		  {
		    "sambrose":{
		      "Property":[
		        [metadata_objects.Property("key", "value"), None]
		      ]
		    }
		  } == f.annotations
		)

	assert(not os.path.exists(jpg_with_internal_annotations+".xmp"))

	with FileForTests(jpg_with_internal_annotations, "w") as f:
		assert(
		  {
		    "sambrose":{
		      "Property":[
		        [metadata_objects.Property("key", "value"), None]
		      ]
		    }
		  } == f.annotations
		)

	assert(os.path.exists(jpg_with_internal_annotations+".xmp"))

def test_qidata_file(jpg_file_path):
	# Open file in "w" mode and add annotation
	a=metadata_objects.Property(key="prop", value="10")
	f = FileForTests(jpg_file_path, "w")
	f.addAnnotation("jdoe", a, None)
	f.addAnnotation("jdoe", a, 1)
	f.close()

	# Make sure that once the file is closed, we can't do any special operation
	with pytest.raises(ClosedFileException):
		f.reloadMetadata()

	with pytest.raises(ClosedFileException):
		f.addAnnotation("jdoe", a, 1)

	# Open file with context manager in "r" mode and check annotation is there
	with FileForTests(jpg_file_path, "r") as f:
		assert(
		  dict(
		    jdoe=dict(
		      Property=[
		        [metadata_objects.Property(key="prop", value="10"), None],
		        [metadata_objects.Property(key="prop", value="10"), 1],
		      ],
		    ),
		  ) == f.annotations
		)

	# Remove all annotations, but then cancel everythin by reloading
	f = FileForTests(jpg_file_path, "w")
	f.removeAnnotation("jdoe", a, None)
	f.removeAnnotation("jdoe", a, 1)
	f.reloadMetadata()
	assert(
	  dict(
	    jdoe=dict(
	      Property=[
	        [metadata_objects.Property(key="prop", value="10"), None],
	        [metadata_objects.Property(key="prop", value="10"), 1],
	      ],
	    ),
	  ) == f.annotations
	)
	f.close()

	# Test properties
	f = FileForTests(jpg_file_path, "r")
	assert(jpg_file_path == f.name)
	assert(not f.closed)
	f.close()
	assert(f.closed)

@pytest.mark.parametrize("file_name,class_,datatype,valid_locs,invalid_locs",
	[
		(
			conftest.JPG_PHOTO,
			QiDataImageFile,
			DataType.IMAGE,
			[
			  [[0,0],[10,80]],
			],
			[
			  0,
			  [0],
			  [[0]],
			]
		),
		(
			conftest.WAV_SOUND,
			QiDataAudioFile,
			DataType.AUDIO,
			[
			  [10,80],
			],
			[
			  0,
			  [0],
			  [[0]],
			  [[0,0],[10,80]],
			]
		),
	]
)
def test_specialized_qidatafile(file_name, class_, datatype,valid_locs,invalid_locs):
	with qidatafile.open(conftest.sandboxed(file_name), "r") as _f:
		assert(isinstance(_f,class_))
		assert(datatype == _f.type)

	with qidatafile.open(conftest.sandboxed(file_name), "w") as _f:
		a=metadata_objects.Property(key="prop", value="10")
		_f.addAnnotation("jdoe", a, None)
		for invalid_loc in invalid_locs:
			with pytest.raises(Exception) as e:
				_f.addAnnotation("jdoe", a, invalid_loc)
			assert ('Location is invalid' == e.value.message)

		for valid_loc in valid_locs:
			_f.addAnnotation("jdoe", a, valid_loc)

def test_specify_type(jpg_file_path):
	with qidatafile.open(jpg_file_path, "w") as f:
		assert(DataType.IMAGE == f.type)
		f.type = DataType.IMAGE_2D
		assert(DataType.IMAGE_2D == f.type)
		f.type = "IMAGE_2D"
		assert(DataType.IMAGE_2D == f.type)
		with pytest.raises(TypeError):
			f.type = DataType.AUDIO

	with qidatafile.open(jpg_file_path, "r") as f:
		assert(DataType.IMAGE_2D == f.type)