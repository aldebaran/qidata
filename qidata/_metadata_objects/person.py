# -*- coding: utf-8 -*-

# Standard libraries
from distutils.version import StrictVersion

# Third-party libraries
from strong_typing.typed_parameters import (IntegerParameter as _Int,
                                            StringParameter as _Str)

# Local modules
from qidata.metadata_objects import MetadataObject

class Person(MetadataObject):

	__ATTRIBUTES__ = [
	                   _Str(name="name",
	                        description="Name of the person represented",
	                        default="")
	]
	__ATT_VERSIONS__ = [None]

	__VERSION__="0.2"
	__DESCRIPTION__="Contains annotation details for a person"

	__DEPRECATED_ATT_N_VERSIONS__ = [
	  (
	    _Int(
	      name="id",
	      description="A unique id given to this person through all relevant data",
	      default=0
	    ),
		None,
		"0.2"
	  )
	]

	# ───────────────────
	# Retro-compatibility

	@classmethod
	def _fromOldDict(cls, data, version):
		if version == StrictVersion("0.1"):
			data.pop("id")
		return cls(**data)
