# -*- coding: utf-8 -*-
"""
QiDataFile specialization for audio files
"""

# Standard libraries


# Third-party libraries

# Local modules
from qidata import DataType
from qidata.qidatafile import QiDataFile

class QiDataAudioFile(QiDataFile):
	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		QiDataFile.__init__(self, file_path, mode)

	# ──────────
	# Properties

	@property
	def type(self):
		return DataType.AUDIO

	@property
	def raw_data(self):
		"""
		Returns the image opened with OpenCV
		"""
		return None

	def _isLocationValid(self, location):
		"""
		Checks if a location given with an annotation is correct

		:param location: The location to evaluate
		:type location: list or None

		.. note::
			The location is expected to be of the form [0,0]. It represents a
			subset of samples, from the first, included, to the last, excluded.
		"""
		if location is None: return True
		try:
			return (
				isinstance(location, list)\
				 and len(location) == 2\
				 and isinstance(location[0],int)\
				 and isinstance(location[1],int)
			)
		except Exception:
			return False