# -*- coding: utf-8 -*-

"""
The ``qidata.qidatafile`` module provides the ``QiDataFile`` class which is a ``QiDataObject``
wrapping the :mod:`xmp` package. It provides the access to a file's metadata through the
QiDataObject's interface.
"""

from xmp.xmp import XMPFile, registerNamespace
from qidata import DataType
import glob
from qidata.qidatafile import QiDataFile
from collections import OrderedDict
import copy
import re
import os
import uuid
import _mixin as xmp_tools

QIDATA_FRAME_NS=u"http://softbank-robotics.com/qidataframe/1"
registerNamespace(QIDATA_FRAME_NS, "qidataframe")

class FrameIsInvalid(Exception):pass

def throwIfInvalid(f):
	def wraps(*args, **kwargs):
		self = args[0]
		if self._is_valid:
			return f(*args, **kwargs)
		raise FrameIsInvalid
	return wraps

class QiDataFrame(QiDataFile):

	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r", files=[]):
		"""
		Create and open a QiDataFrame.

		:param file_path: path of the file to open
		:type file_path: str
		:param mode: opening mode, "r" for reading, "w" for writing
		:type mode: str
		:param files: list of files that composes the frame
		:type files: list
		:raises: TypeError if less than 2 files are given
		"""
		self._files = set(files)
		self._is_valid = True
		QiDataFile.__init__(self, file_path, mode)

	@staticmethod
	def create(files, parent_corpus_path):
		"""
		Factory to create QiDataFrame.

		:param files: list of files that composes the frame
		:type files: list
		:param parent_corpus_path: path to the corpus containing the frame
		:type parent_corpus_path: str
		:raises: TypeError if less than 2 files are given
		"""
		frame_name = os.path.join(parent_corpus_path,str(uuid.uuid4())+".frame.xmp")
		frame = QiDataFrame(frame_name, "w", files)
		return frame

	# ──────────
	# Properties

	@property
	def raw_data(self):
		"""
		Same as `files` property
		"""
		return self.files

	@property
	@throwIfInvalid
	def files(self):
		"""
		Return the set of files composing this frame
		"""
		return copy.copy(self._files)

	@property
	@throwIfInvalid
	def mode(self):
		return QiDataFile.mode.__get__(self)

	@property
	@throwIfInvalid
	def annotations(self):
		return QiDataFile.annotations.__get__(self)

	# ──────────
	# Public API

	def close(self):
		"""
		Closes the file frame after writing the metadata
		"""
		if self.mode != "r":
			# Erase current frame content's metadata
			_raw_metadata = self._xmp_file.metadata[QIDATA_FRAME_NS]
			setattr(_raw_metadata, "files", list(self._files))

		QiDataFile.close(self)

	# ───────────
	# Private API

	def _isLocationValid(self, location):
		"""
		Checks if a location given with an annotation is correct

		:param location: The location to evaluate
		:type location: list or None

		.. note::
			The location is expected to be a 3D bounding box, respecting the
			form [[0.0,0.0,0.0],[100.0,100.0,100.0]]. It represents a cuboid, by
			the coordinates of two opposite corner (and assuming all coordinates
			of the first corner are lower than the ones of the second corner)
		"""
		if location is None: return True
		try:
			return (
			  isinstance(location[0][0],float)\
			    and isinstance(location[0][1],float)\
			    and isinstance(location[0][2],float)\
			    and isinstance(location[1][0],float)\
			    and isinstance(location[1][1],float)\
			    and isinstance(location[1][2],float)\
			    and location[0][0] < location[1][0]\
			    and location[0][1] < location[1][1]\
			    and location[0][2] < location[1][2]
			)
		except Exception:
			return False

	@throwIfInvalid
	def _open(self):
		"""
		Open the file
		"""
		QiDataFile._open(self)

		# Load content info stored in metadata
		_raw_metadata = self._xmp_file.metadata[QIDATA_FRAME_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			xmp_tools._removePrefixes(data)
			self._files = set(data["files"])
		return self
