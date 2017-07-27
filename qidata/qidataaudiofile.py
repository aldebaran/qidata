# -*- coding: utf-8 -*-
"""
QiDataSensorFile specialization for audio files
"""

# Local modules
from qidata import DataType
from qidata.qidatasensorfile import QiDataSensorFile

class QiDataAudioFile(QiDataSensorFile):
	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		QiDataSensorFile.__init__(self, file_path, mode)

	# ──────────
	# Properties

	@property
	def type(self):
		_t = QiDataSensorFile.type.fget(self)
		return _t if _t else DataType.AUDIO

	@type.setter
	def type(self, new_type):
		if not str(new_type).startswith("AUDIO"):
			raise TypeError("Cannot convert %s to %s"%(self.type, new_type))
		QiDataSensorFile.type.fset(self, new_type)

	@property
	def raw_data(self):
		"""
		Returns the raw data of audio file

		:raise: NotImplementedError
		"""
		raise NotImplementedError

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