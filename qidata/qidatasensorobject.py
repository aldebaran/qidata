# -*- coding: utf-8 -*-

# Standard libraries
from collections import OrderedDict
import copy
import abc

# Local modules
from qidata import DataType
from qidata.qidataobject import QiDataObject,ReadOnlyException,throwIfReadOnly
from qidata.metadata_objects import TimeStamp
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
		return self._position

	@property
	def timestamp(self):
		return getattr(self,"_timestamp", TimeStamp(0,0))

	@timestamp.setter
	@throwIfReadOnly
	def timestamp(self, new_ts):
		self._timestamp = new_ts
