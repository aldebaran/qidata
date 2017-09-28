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

# Standard library
from distutils.version import StrictVersion

# Third-party libraries
from strong_typing.typed_parameters import (EnumParameter as _Enum,
                                            StructParameter as _Stru,
                                            StringParameter as _Str,
                                            FloatParameter as _Float,
                                            IntegerParameter as _Int,
                                            VectorParameter as _Vect)
# Local modules
from qidata.metadata_objects import MetadataObject
from qidata.metadata_objects import _QidataEnumMixin
import model_device as _md
DeviceModel = _md.generateEnum()
from countries import Country

class SpatialLocation(MetadataObject):

	__ATTRIBUTES__ = [
	                   _Enum(name="country",
	                   	    choices=Country,
	                        description="Continent and country where the data was recorded",
	                        default=Country.UNSPECIFIED),

	                   _Str(name="city",
	                          description="City where the data was recorded"),

	                   _Float(name="latitude",
	                         description="Recording's location's latitude",
	                         default=None,
	                         range=(-90, 90)),

	                   _Float(name="longitude",
	                         description="Recording's location's longitude",
	                         default=None,
	                         range=(-180, 180)),

	                   _Vect(name="tags",
	                          description="Add some tags to help sorting by location.\
	                          It can be a room name for instance",
	                          type=str)
	]
	__ATT_VERSIONS__ = [None]*5

	__VERSION__="0.1"
	__DESCRIPTION__="Contains details about the device used to produce the data"

class TimeLocation(MetadataObject):

	__ATTRIBUTES__ = [
	                   _Int(name="year",
	                           description="Year of the recording",
	                           default=None,
	                           range=(0, None)),

	                   _Int(name="month",
	                           description="Month of the recording",
	                           default=None,
	                           range=(1, 12)),

	                   _Int(name="day",
	                           description="Day of the recording",
	                           default=None,
	                           range=(1, 31)),

	                   _Int(name="hour",
	                           description="Hour of the recording",
	                           default=None,
	                           range=(0, 23)),

	                   _Float(name="starting_timestamp",
	                         description="Recording's starting timestamp",
	                         default=None,
	                         range=(0, None)),

	                   _Float(name="length",
	                         description="Recording's duration (in seconds)",
	                         default=None,
	                         range=(0, None))
	]
	__ATT_VERSIONS__ = [None]*6

	__VERSION__="0.1"
	__DESCRIPTION__="Contains information on the date and time of the data acquisition"

class RecordingDevice(MetadataObject):

	__ATTRIBUTES__ = [
	                   _Enum(name="device_model",
	                   	    choices=DeviceModel,
	                        description="Brand and model of the device used to record",
	                        default=DeviceModel.UNSPECIFIED),

	                   _Str(name="device_id",
	                         description="Unique ID of the device used to record"),

	                   _Str(name="sw_version",
	                         description="Version of the software embedded on the device\
	                         (or any relevant SW) used to perform the recording")
	]
	__ATT_VERSIONS__ = [None]*3

	__VERSION__="0.1"
	__DESCRIPTION__="Contains details about the device used to produce the data"

class EnvironmentalSoundConditions(MetadataObject):

	__slots__ = ["ambient_sound_reverberation",
	             "ambient_sound_level"]

	__ATTRIBUTES__ = [
	                   _Float(name="ambient_sound_reverberation",
	                        description="Recording area reverberation time in seconds (RT60)",
	                        default=None,
	                        range=(0.0, None)),

	                   _Float(name="ambient_sound_level",
	                         description="General sound level in the recording area in dB",
	                         default=None,
	                         range=(None, None))
	]
	__ATT_VERSIONS__ = [None]*2

	__VERSION__="0.1"
	__DESCRIPTION__="Contains details about the sound environment"

class EnvironmentalLightConditions(MetadataObject):
	class FromOutdoor(_QidataEnumMixin):
		NO_OUTDOOR_LIGHT = 0
		NIGHT_LIGHT = 1
		STREET_LIGHT_AT_NIGHT = 2
		CLOUDY_DAY_LIGHT = 3
		SUNNY_DAY_LIGHT = 4
		UNSPECIFIED = 99

	class FromIndoor(_QidataEnumMixin):
		NO_INDOOR_LIGHT = 0
		CANDLE_LIGHT = 1
		DIM_LIGHT = 2
		BRIGHT_LIGHT = 3
		FLASH_LIGHT = 4
		UNSPECIFIED = 99

	__ATTRIBUTES__ = [
	                   _Enum(name="outdoor_light",
	                   	    choices=FromOutdoor,
	                        description="Type of light coming from the outside enlighting the scene",
	                        default=FromOutdoor.UNSPECIFIED),

	                   _Enum(name="indoor_light",
	                        choices=FromIndoor,
	                        description="Type of light coming from the inside enlighting the scene",
	                        default=FromIndoor.UNSPECIFIED),

	                   _Float(name="ambient_luminosity",
	                         description="Ambient luminosity of the scene (lux)",
	                         default=None,
	                         range=(0, None))
	]
	__ATT_VERSIONS__ = [None]*3

	__VERSION__="0.1"
	__DESCRIPTION__="Contains details about how the environment is enlightened"

class EnvironmentalDescription(MetadataObject):
	class Category(_QidataEnumMixin):
		INDOOR_BAR = 0
		INDOOR_HOUSE = 1
		INDOOR_OFFICE = 2
		INDOOR_RESTAURANT = 3
		INDOOR_SHOP = 4
		INDOOR_UNSPECIFIED = 99

		OUTDOOR_FOREST = 100
		OUTDOOR_MOUNTAIN = 101
		OUTDOOR_SKY = 102
		OUTDOOR_STREET = 103
		OUTDOOR_UNSPECIFIED = 199

		TRANSPORT_BOAT = 201
		TRANSPORT_BUS = 202
		TRANSPORT_CAR = 203
		TRANSPORT_PLANE = 204
		TRANSPORT_SUBWAY = 205
		TRANSPORT_TRAIN = 206
		TRANSPORT_UNSPECIFIED = 299

		UNSPECIFIED = 9999

	__ATTRIBUTES__ = [
	                   _Enum(name="category",
	                   	    choices=Category,
	                        description="Type of environment",
	                        default=Category.UNSPECIFIED),

	                   _Stru(name="light_conditions",
	                          description="Description of lighting conditions of the scene",
	                          type=EnvironmentalLightConditions),

	                   _Stru(name="sound_conditions",
	                          description="Description of audio conditions of the scene",
	                          type=EnvironmentalSoundConditions)
	]
	__ATT_VERSIONS__ = [None]*3

	__VERSION__="0.1"
	__DESCRIPTION__="Contains details about the environment"

class Context(MetadataObject):
	__ATTRIBUTES__ = [
	                   _Stru(name="recording_location",
	                          description="Location where the data was recorded",
	                          type=SpatialLocation),

	                   _Stru(name="recording_datetime",
	                          description="Datetime when the data was recorded",
	                          type=TimeLocation),

	                   _Stru(name="recording_device",
	                          description="Details on the device used to record",
	                          type=RecordingDevice),

	                   _Vect(name="recorder_names",
	                          description="Name of the persons handling the recording",
	                          type=str),

	                   _Stru(name="environmental_description",
	                          description="Description of the conditions of the recording",
	                          type=EnvironmentalDescription),

	                   _Vect(name="tags",
	                          description="Add some tags to describe your dataset.\
	                          This could be used to sort datasets and also to organize\
	                          test results. It is however always preferable to use the\
	                          defined sections. Tags is only here to add information that\
	                          does not fit in other attributes.",
	                          type=str)
	]
	__ATT_VERSIONS__ = [None]*6

	__VERSION__="0.1"
	__DESCRIPTION__="Contains contextual details on the recording"
