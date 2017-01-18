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
import sys as _sys

# ––––––––––––––––––––––––––––
# Convenience version variable

VERSION = open(_os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "VERSION")).read().split()[0]

# –––––––––––––––––––––
# Load metadata plugins

# Dynamically create a module
metadata_objects = _ModType("metadata_objects")
_sys.modules["qidata.metadata_objects"] = metadata_objects
_metadata_list = list()

# Load all plugins and mount them on our dynamic module
for _ep in _pkg.iter_entry_points(group="qidata.metadata.definition"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]
	# Add the class's name to metadata type list
	_metadata_list.append(_name)
	# Add the class to module's attributes
	setattr(metadata_objects, _name, _ep.load())

for _ep in _pkg.iter_entry_points(group="qidata.metadata.package"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]
	# Add the module to module's attributes
	setattr(metadata_objects, _name, _ep.load())
	# Add the module to global module cache
	_sys.modules["qidata.metadata_objects."+_name] = getattr(metadata_objects, _name)



#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
