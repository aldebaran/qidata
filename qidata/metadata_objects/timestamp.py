# -*- coding: utf-8 -*-

# Standard library
from distutils.version import StrictVersion

# Third-party libraries
from strong_typing.typed_parameters import IntegerParameter as _Int

# Local modules
from qidata.metadata_objects import MetadataObject

class TimeStamp(MetadataObject):

	__ATTRIBUTES__ = [
		_Int(name="seconds",
		      description="Number of seconds since Epoch",
		      default=0),
		_Int(name="nanoseconds",
		      description="Number of nanoseconds after the current second",
		      range=(0, 1000000000),
		      default=0)
	]
	__ATT_VERSIONS__ = [None]*2

	__VERSION__="0.1"
	__DESCRIPTION__="Timestamp at which the data was created"
