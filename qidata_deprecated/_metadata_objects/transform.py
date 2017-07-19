# -*- coding: utf-8 -*-

# Standard library
from distutils.version import StrictVersion

# strong_typing
from strong_typing import VersionedStruct as _VS
from strong_typing.typed_parameters import (EnumParameter as _Enum,
                                            StructParameter as _Stru,
                                            StringParameter as _Str,
                                            FloatParameter as _Float,
                                            IntegerParameter as _Int,
                                            VectorParameter as _Vect)

class Translation(_VS):

	__ATTRIBUTES__ = [
	                   _Float(name="x",
	                           description="Translation vector's X coordinate",
	                           default=0),

	                   _Float(name="y",
	                           description="Translation vector's Y coordinate",
	                           default=0),

	                   _Float(name="z",
	                           description="Translation vector's Z coordinate",
	                           default=0)
	]
	__ATT_VERSIONS__ = [None]*3

	__VERSION__="0.1"
	__DESCRIPTION__="Describes a translation by a size 3 vector"

class Rotation(_VS):

	__ATTRIBUTES__ = [
	                   _Float(name="x",
	                           description="Rotation quaternion's X coordinate",
	                           default=0),

	                   _Float(name="y",
	                           description="Rotation quaternion's Y coordinate",
	                           default=0),

	                   _Float(name="z",
	                           description="Rotation quaternion's Z coordinate",
	                           default=0),

	                   _Float(name="w",
	                           description="Rotation quaternion's W coordinate",
	                           default=0),
	]
	__ATT_VERSIONS__ = [None]*4

	__VERSION__="0.1"
	__DESCRIPTION__="Describes a rotation by a quaternion"

class Transform(_VS):

	__ATTRIBUTES__ = [
	    _Stru(name="translation",
	                          description="Location where the data was recorded",
	                          type=Translation),
	    _Stru(name="rotation",
	                          description="Location where the data was recorded",
	                          type=Rotation),
	]
	__ATT_VERSIONS__ = [None]*2

	__VERSION__="0.1"
	__DESCRIPTION__="Describes the coordinates and orientation of a piece of data"
