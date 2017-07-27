# -*- coding: utf-8 -*-
"""
QiDataSensorFile specialization for image files
"""

# Standard libraries


# Third-party libraries
import cv2

# Local modules
from qidata import DataType
from qidata.qidatasensorfile import QiDataSensorFile

class QiDataImageFile(QiDataSensorFile):
	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		self._raw_data = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
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
		res_str += "Image shape: " + str(self.raw_data.shape) + "\n"
		return res_str