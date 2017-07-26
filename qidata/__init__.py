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

# Local modules
from metadata_objects import __all__

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
	# IMG_STEREO = 5 #: For stereo images

	def __str__(self):
		return self.name

# –––––––––––––––––––––––––––––––––
# Define supported metatadata types

_metadata_list = __all__

# Make sure there is at least one definition
if len(_metadata_list) == 0:
	_msg = "No metadata definition could be found."
	_msg += "Please try to re-install to fix the problem."
	raise ImportError(_msg)

# Create MetadataType enum
MetadataType = _BaseEnum("MetadataType", _metadata_list)
MetadataType.__doc__ = "Metadata object types provided by qidata"

def makeMetadataObject(metadata_object_type, data=None):
	"""
	MetadataObjects factory
	This is the prefered way to create MetadataObjects. Objects that
	can be created by this method are the ones in `qidata.MetadataType`

	:param metadata_object_type: requested object to build's name
	:type metadata_object_type: str
	:param data: data to prefill to created object
	:type data: dict
	"""
	if isinstance(metadata_object_type, MetadataType)\
	  and hasattr(metadata_objects,metadata_object_type.name):
		class_ = getattr(metadata_objects,metadata_object_type.name)
		return class_() if data is None else class_.fromDict(data)
	else:
		raise TypeError("Requested metadata object (%s) does not exist"
		                % metadata_object_type)

# Import submodules import definitions
from qidatafile import QiDataFile, ClosedFileException
from qidataset import QiDataSet, isDataset