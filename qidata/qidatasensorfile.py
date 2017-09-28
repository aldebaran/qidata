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

# Third-party libraries
from xmp.xmp import XMPFile, registerNamespace

# Local modules
from qidata import DataType
from qidata.metadata_objects import Transform, TimeStamp
from qidata.qidatafile import QiDataFile, throwIfClosed
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
			setattr(_raw_metadata, "transform", self.transform)
			setattr(_raw_metadata, "timestamp", self.timestamp)

		super(QiDataSensorFile, self).close()

	# ───────────
	# Private API

	@throwIfClosed
	def _loadAnnotations(self):
		super(QiDataSensorFile, self)._loadAnnotations()

		# Load data type
		_raw_metadata = self._xmp_file.metadata[QIDATA_SENSOR_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			xmp_tools._removePrefixes(data)
			self._type = DataType[data["data_type"]]
			self._position = Transform(**data["transform"])
			self._timestamp = TimeStamp(**data["timestamp"])

	# ──────────────
	# Textualization

	def __unicode__(self):
		res_str = ""
		res_str += "File name: " + self.name + "\n"
		res_str += "Object type: " + unicode(self.type) + "\n"
		res_str += "Object timestamp: " + unicode(self.timestamp) + "\n"
		res_str += "Object transform: " + unicode(self.transform) + "\n"
		res_str += QiDataObject.__unicode__(self)
		return res_str