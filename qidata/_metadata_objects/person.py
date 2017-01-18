# -*- coding: utf-8 -*-

# Standard library
from distutils.version import StrictVersion

# strong_typing
from strong_typing import VersionedStruct
from strong_typing.typed_parameters import (IntegerParameter,
                                            StringParameter)

class Person(VersionedStruct):

	__ATTRIBUTES__ = [
	                   StringParameter(name="name",
	                          description="Name of the person represented",
	                          default="")
	]
	__ATT_VERSIONS__ = [None]

	__VERSION__="0.2"
	__DESCRIPTION__="Contains annotation details for a person"

	__DEPRECATED_ATT_N_VERSIONS__ = [
	                                  (IntegerParameter(name="id",
	                                           description="A unique id given to this person through all relevant data",
	                                           default=0), None, "0.2")
	]


	# ───────────────────
	# Retro-compatibility

	@classmethod
	def _fromOldDict(cls, data, version):
		if version == StrictVersion("0.1"):
			data.pop("id")
		return cls(**data)
