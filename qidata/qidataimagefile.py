# -*- coding: utf-8 -*-
"""
QiDataFile specialization for image files
"""

# Standard libraries


# Third-party libraries
import cv2

# Local modules
from qidata import DataType
from qidata.qidatafile import QiDataFile

class QiDataImageFile(QiDataFile):
	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		self._raw_data = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
		QiDataFile.__init__(self, file_path, mode)

	# ──────────
	# Properties

	@property
	def type(self):
		return DataType.IMAGE

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