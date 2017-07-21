# -*- coding: utf-8 -*-

# Third-party libraries
from strong_typing.typed_parameters import StringParameter as _String

# Local modules
from qidata.metadata_objects import MetadataObject

class Property(MetadataObject):

	__ATTRIBUTES__ = [
	                   _String(name="key",
	                           description="Property name",
	                           default=None),
	                   _String(name="value",
	                           description="Property value",
	                           default=""),
	]
	__ATT_VERSIONS__ = [None]*2

	__VERSION__="0.1"
	__DESCRIPTION__="Contains a property in the form of a key and a value"
