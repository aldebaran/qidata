# -*- coding: utf-8 -*-

"""
	``qidata`` package
	==================

	This package contains or will contain in the near future several tools designed to
	facilitate data annotation and datasets handling.

	It provides libraries desgined to easilly construct metadata objects depending on the concerned
	data type and is built on an external library (Adobe's XMP) to store those metadata with the
	concerned file.
	However, using those metadata is not restricted to a file, it could later be simply used to
	display specific information on an data stream for instance.

"""

# Standard libraries
import os as _os
import pkg_resources as _pkg
from types import ModuleType as _ModType
from enum import Enum as _Enum
import sys as _sys

# ––––––––––––––––––––––––––––
# Convenience version variable

VERSION = open(_os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "VERSION")).read().split()[0]

# –––––––––––––––––––––
# Load metadata plugins

# Dynamically create a module
_dyn_mod_name = "qidata.metadata_objects"
metadata_objects = _ModType(_dyn_mod_name)
metadata_objects.__path__ = []
metadata_objects.__doc__ = "Dynamic package to mount metadata plugins"
_sys.modules[_dyn_mod_name] = metadata_objects
_metadata_list = list()

# Load all plugins and mount them on our dynamic module
for _ep in _pkg.iter_entry_points(group="qidata.metadata.definition"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]

	# Add the class's name to metadata type list
	_metadata_list.append(_name)

	# Add the class to module's attributes
	setattr(metadata_objects, _name, _ep.load())

	# Reset the class module and name
	getattr(metadata_objects, _name).__module__ = _dyn_mod_name
	getattr(metadata_objects, _name).__name__ = _name

for _ep in _pkg.iter_entry_points(group="qidata.metadata.package"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]

	# Add the module to module's attributes
	setattr(metadata_objects, _name, _ep.load())

	# Add the module to global module cache
	getattr(metadata_objects, _name).__name__ = _dyn_mod_name+"."+_name
	_sys.modules[_dyn_mod_name+"."+_name] = getattr(metadata_objects, _name)


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
	AUDIO   = 0 #: For WAV files
	DATASET = 1 #: For folders containing several annotated files
	IMAGE   = 2 #: For PNG and JPG images

	def __str__(self):
		return self.name


# –––––––––––––––––––––––––––––––––
# Define supported metatadata types

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

	:param metadata_object_type: requested object to build's name (str)
	:param data: data to prefill to created object (dict)
	"""
	if isinstance(metadata_object_type, MetadataType)\
	  and hasattr(metadata_objects,metadata_object_type.name):
		class_ = getattr(metadata_objects,metadata_object_type.name)
		return class_() if data is None else class_.fromDict(data)
	else:
		raise TypeError("Requested metadata object (%s) does not exist"
		                % metadata_object_type)

# –––––––––––––
# Inner modules

from qidatafile import QiDataFile
from qidataset import QiDataSet

# –––––––––––––––
# Exported values

__all__ = ["metadata_objects",
           "makeMetadataObject",
           "DataType",
           "MetadataType"
           "QiDataFile",
           "QiDataSet"]

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
