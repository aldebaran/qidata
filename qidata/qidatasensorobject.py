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
from collections import OrderedDict
import copy
import abc

# Local modules
from qidata import DataType
from qidata.qidataobject import QiDataObject,ReadOnlyException,throwIfReadOnly
from qidata.metadata_objects import TimeStamp, Transform
from textualize import textualize_metadata

class QiDataSensorObject(QiDataObject):
	"""
	Abstract class describing a piece of data created by a sensor.
	"""
	# ──────────
	# Properties

	@abc.abstractproperty
	def type(self):
		"""
		Specify the type of data in the object

		:return: The type of this object
		:rtype: qidata.DataType
		"""
		return getattr(self, "_type", None)

	@type.setter
	@throwIfReadOnly
	def type(self, new_type):
		"""
		Changes the type of the object

		:param data_type: New data type
		:type data_type: qidata.DataType

		.. note::
			A given type cannot be changed to any other type, they have to be
			related
		"""
		# Check given type
		try:
			self._type = DataType[new_type]
		except KeyError:
			try:
				self._type = DataType(new_type)
			except ValueError:
				raise TypeError("%s is not a valid DataType"%new_type)

	@property
	def transform(self):
		"""
		Returns the position of the sensor which created the current data
		in a global frame.

		:rtype: qidata.metadata_objects.Transform
		"""
		if not hasattr(self, "_position"):
			self._position = Transform()
		return self._position

	@transform.setter
	@throwIfReadOnly
	def transform(self, new_tf):
		if isinstance(new_tf, Transform):
			self._position = new_tf
		else:
			raise TypeError("Wrong type given to update transform property")

	@property
	def timestamp(self):
		"""
		Returns the timestamp at which the current data was created.

		:rtype: qidata.metadata_objects.TimeStamp
		"""
		if not hasattr(self, "_timestamp"):
			self._timestamp = TimeStamp(0,0)
		return self._timestamp

	@timestamp.setter
	@throwIfReadOnly
	def timestamp(self, new_ts):
		if isinstance(new_ts, TimeStamp):
			self._timestamp = new_ts
		else:
			raise TypeError("Wrong type given to update timestamp property")

	# ──────────────
	# Textualization

	def __unicode__(self):
		res_str = ""
		res_str += "Object type: " + unicode(self.type) + "\n"
		res_str += "Object timestamp: " + unicode(self.timestamp) + "\n"
		res_str += "Object transform: " + unicode(self.position) + "\n"
		res_str += QiDataObject.__unicode__(self)
		return res_str