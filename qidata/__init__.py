# -*- coding: utf-8 -*-

"""
	``qidata`` package
	==================

	This package contains or will contain in the near future several tools
	designed to facilitate data annotation and datasets handling.

	It provides libraries designed to easilly construct metadata objects
	depending on the concerned data type and is built on an external library
	(Adobe's XMP) to store those metadata with the concerned file.
	However, using those metadata is not restricted to a file, it could later be
	simply used to display specific information on an data stream for instance.
"""

# Standard libraries
from enum import Enum as _Enum
import os as _os
import pkg_resources as _pkg
import re as _re

# Local modules
import metadata_objects

# ––––––––––––––––––––––––––––
# Convenience version variable

VERSION = open(_os.path.join(_os.path.dirname(_os.path.realpath(__file__)),
                             "VERSION")).read().split()[0]

# ––––––––––––––––––––––
# Define convenient enum

class _BaseEnum(_Enum):
	def __str__(self):
		return self.name

# –––––––––––––––––––––––––––
# Define supported data types

class DataType(_BaseEnum):
	"""
	Types of objects known by qidata
	"""
	AUDIO      = 0 #: For WAV files
	# DATASET    = 1 #: For folders containing several annotated files
	# FRAME      = 6 #: Special file describing an "atomic" piece of data
	IMAGE      = 2 #: For all images (used for PNG and JPG extensions)
	IMAGE_2D   = 3 #: For 2D images
	IMAGE_3D     = 4 #: For 3D images
	IMAGE_IR     = 5 #: For IR images
	IMAGE_STEREO = 6 #: For stereo images

	def __str__(self):
		return self.name

# –––––––––––––––––––––––––––––––––
# Define supported metatadata types

_metadata_list = metadata_objects.__all__

# Load all plugins and mount them on metadata_objects module
for _ep in _pkg.iter_entry_points(group="qidata.metadata.definition"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]

	# Add the class's name to metadata type list
	_metadata_list.append(_name)

	# Add the class to module's attributes
	setattr(metadata_objects, _name, _ep.load())

	# Reset the class module and name
	getattr(metadata_objects, _name).__module__ = "qidata.metadata_objects"
	getattr(metadata_objects, _name).__name__ = _name

for _ep in _pkg.iter_entry_points(group="qidata.metadata.package"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]

	# Add the module to module's attributes
	setattr(metadata_objects, _name, _ep.load())

	# Add the module to global module cache
	getattr(metadata_objects, _name).__name__ = "qidata.metadata_objects."+_name
	_sys.modules["qidata.metadata_objects."+_name] = getattr(metadata_objects,
	                                                         _name)


# Make sure there is at least one definition
if len(_metadata_list) == 0:
	_msg = "No metadata definition could be found."
	_msg += "Please try to re-install to fix the problem."
	raise ImportError(_msg)

# Create MetadataType enum
MetadataType = _BaseEnum("MetadataType", _metadata_list)
MetadataType.__doc__ = "Metadata object types provided by qidata"

# ––––––––––––––––––––––––––––––
# Define metadata object factory

def makeMetadataObject(metadata_object_type, data=None):
	"""
	MetadataObjects factory
	This is the prefered way to create MetadataObjects. Objects that
	can be created by this method are the ones in `qidata.MetadataType`

	:param metadata_object_type: requested object to build's name
	:type metadata_object_type: str or qidata.MetadataType
	:param data: data to prefill to created object
	:type data: dict
	"""
	try:
		metadata_object_type = MetadataType[metadata_object_type]
	except KeyError:
		try:
			metadata_object_type = MetadataType(metadata_object_type)
		except ValueError:
			raise TypeError(
			          "%s is not a valid MetadataType"%metadata_object_type
			      )
	if isinstance(metadata_object_type, MetadataType)\
	  and hasattr(metadata_objects,metadata_object_type.name):
		class_ = getattr(metadata_objects,metadata_object_type.name)
		return class_() if data is None else class_.fromDict(data)
	else:
		raise TypeError("Requested metadata object (%s) does not exist"
		                % metadata_object_type)

# Make some submodules stuff directly accessible from qidata package
from qidataobject import ReadOnlyException
from qidatafile import QiDataFile, ClosedFileException
from qidataset import QiDataSet, isDataset

# ────────────────────
# File opening factory

from qidata import qidatasensorfile
from qidata import qidataimagefile
from qidata import qidataaudiofile

_LOOKUP_ITEM_MODEL = {
    _re.compile(".*\.png$"): qidataimagefile.QiDataImageFile,
    _re.compile(".*\.jpg$"): qidataimagefile.QiDataImageFile,
    _re.compile(".*\.wav$"): qidataaudiofile.QiDataAudioFile,
}

def isSupportedDataFile(file_path):
	"""
	Return True if path is a data file and can be opened as a QiDataFile

	:param file_path: Path of the file to test
	:type file_path: str
	:return: True if file can be opened as a QiDataFile
	:rtype: bool
	"""
	for pattern in _LOOKUP_ITEM_MODEL:
		if pattern.match(file_path):
			return True
	return False

def isSupported(data_path):
	"""
	Return True if path can be opened by qidata

	:param data_path: Path to test
	:type data_path: str
	:return: True if path is supported by qidata
	:rtype: bool
	"""
	return isSupportedDataFile(data_path)\
	       or _os.path.isdir(data_path)\
	       or _os.path.splitext(data_path)[1] == ".xmp"

def open(file_path, mode="r"):
	"""
	Open a file with qidata
	This is the preferred way to open a QiDatafile or a QiDataSet.

	:param file_path: Path to the file or folder to open
	:param mode: Mode of opening ("r" for reading, "w" for writing)
	:rtype: qidata.QiDataFile or qidata.QiDataSet
	:Example:
		>>> import qidata
		>>> myFile = qidata.open("path/to/file")

	.. warning::

		The mode behavior is different from the regular Python file mode.
		The file is NEVER created if it does not exist. Besides, opening
		an existing file in "w" mode does not overwrite it.
	"""
	path_splitted = _os.path.splitext(file_path)
	if path_splitted[1] == ".xmp":
		file_path = path_splitted[0]

	for pattern in _LOOKUP_ITEM_MODEL:
		if pattern.match(file_path):
			return _LOOKUP_ITEM_MODEL[pattern](file_path, mode)

	raise TypeError("Data type not supported by QiDataFile")