# -*- coding: utf-8 -*-

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
	def position(self):
		"""
		Returns the position of the sensor which created the current data
		in a global frame.

		:rtype: qidata.metadata_objects.Transform
		"""
		return getattr(self,
		               "_position",
		               Transform(translation=dict(x=0,y=0,z=0),
		                         rotation=dict(x=0,y=0,z=0,w=1))
		              )

	@position.setter
	@throwIfReadOnly
	def position(self, new_pos):
		if isinstance(new_pos, Transform):
			self._position = new_pos
		else:
			raise TypeError("Wrong type given to update position property")

	@property
	def timestamp(self):
		"""
		Returns the timestamp at which the current data was created.

		:rtype: qidata.metadata_objects.TimeStamp
		"""
		return getattr(self, "_timestamp", TimeStamp(0,0))

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