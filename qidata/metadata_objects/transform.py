# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard libraries
from distutils.version import StrictVersion

# Third-party libraries
from strong_typing.typed_parameters import (StructParameter as _Stru,
                                            FloatParameter as _Float)

# Local modules
from qidata.metadata_objects import MetadataObject

class Translation(MetadataObject):

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

class Rotation(MetadataObject):

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
	                           default=1),
	]
	__ATT_VERSIONS__ = [None]*4

	__VERSION__="0.1"
	__DESCRIPTION__="Describes a rotation by a quaternion"

class Transform(MetadataObject):

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
	__DESCRIPTION__="Describes the coordinates and orientation of a sensor"
