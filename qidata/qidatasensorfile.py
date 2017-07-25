# -*- coding: utf-8 -*-

# Third-party libraries
from xmp.xmp import XMPFile, registerNamespace

# Local modules
from qidata import DataType
from qidata.metadata_objects import Transform, TimeStamp
from qidata.qidatafile import QiDataFile
from qidata.qidataobject import QiDataObject
from qidata.qidatasensorobject import QiDataSensorObject
import _mixin as xmp_tools

QIDATA_SENSOR_NS=u"http://softbank-robotics.com/qidatasensor/1"
registerNamespace(QIDATA_SENSOR_NS, "qidatasensor")

class QiDataSensorFile(QiDataSensorObject, QiDataFile):

	# ──────────
	# Public API

	def close(self):
		"""
		Closes the file after writing the metadata
		"""
		if self.mode != "r":
			_raw_metadata = self._xmp_file.metadata[QIDATA_SENSOR_NS]
			setattr(_raw_metadata, "data_type", self.type)
			setattr(_raw_metadata, "position", self.position)
			setattr(_raw_metadata, "timestamp", self.timestamp)

		super(QiDataSensorFile, self).close()

	def reloadMetadata(self):
		super(QiDataSensorFile, self).reloadMetadata()

		# Load data type
		_raw_metadata = self._xmp_file.metadata[QIDATA_SENSOR_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			xmp_tools._removePrefixes(data)
			self._type = DataType[data["data_type"]]
			self._position = Transform(**data["position"])
			self._timestamp = TimeStamp(**data["timestamp"])

	# ──────────────
	# Textualization

	def __unicode__(self):
		res_str = ""
		res_str += "File name: " + self.name + "\n"
		res_str += "Object type: " + unicode(self.type) + "\n"
		res_str += "Object timestamp: " + unicode(self.timestamp) + "\n"
		res_str += "Object transform: " + unicode(self.position) + "\n"
		res_str += QiDataObject.__unicode__(self)
		return res_str