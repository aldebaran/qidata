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

"""
QiDataSensorFile specialization for image files
"""

# Standard libraries


# Third-party libraries
import cv2
from image import Image

# Local modules
from qidata import DataType
from qidata.qidatasensorfile import QiDataSensorFile

class QiDataImageFile(QiDataSensorFile):
	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		self._raw_data = Image(file_path)
		QiDataSensorFile.__init__(self, file_path, mode)

	# ──────────
	# Properties

	@property
	def type(self):
		_t = QiDataSensorFile.type.fget(self)
		return _t if _t else DataType.IMAGE

	@type.setter
	def type(self, new_type):
		if not str(new_type).startswith("IMAGE"):
			raise TypeError("Cannot convert %s to %s"%(self.type, new_type))
		QiDataSensorFile.type.fset(self, new_type)

	@property
	def raw_data(self):
		"""
		Returns the image opened with OpenCV
		"""
		return self._raw_data

	def _isLocationValid(self, location):
		"""
		Checks if a location given with an annotation is correct

		:param location: The location to evaluate
		:type location: list or None

		.. note::
			The location is expected to be of the form [[0,0],[100,100]]. It
			represents a rectangle, by the coordinates of its upper left and
			lower right corners.
		"""
		if location is None: return True
		try:
			return (
			  isinstance(location[0][0],int)\
			    and isinstance(location[0][1],int)\
			    and isinstance(location[1][0],int)\
			    and isinstance(location[1][1],int)
			)
		except Exception:
			return False

	# ──────────────
	# Textualization

	def __unicode__(self):
		res_str = QiDataSensorFile.__unicode__(self)
		res_str += "Image shape: " + str(self.raw_data.numpy_image.shape) + "\n"
		return res_str