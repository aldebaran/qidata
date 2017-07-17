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
from qidata.qidataobject import QiDataObject
from collections import OrderedDict
import copy
import re
import os
import uuid
from _mixin import XMPHandlerMixin

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

class QiDataFrame(QiDataObject, XMPHandlerMixin):

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
		self._file_path = file_path
		self._files = set(files)
		self._xmp_file = XMPFile(self._file_path, rw=(mode=="w"))
		self._is_closed = True
		self._is_valid = True
		self._open()

	@staticmethod
	def create(files, parent_corpus_path, mode):
		frame_name = os.path.join(parent_corpus_path,str(uuid.uuid4())+".frame.xmp")
		frame = QiDataFrame(frame_name, mode, files)
		return frame

	# ──────────
	# Properties

	@property
	@throwIfInvalid
	def raw_data(self):
		"""
		Return a list with the data set's children and content
		"""
		return copy.copy(self._files)

	@property
	@throwIfInvalid
	def files(self):
		"""
		Return the set of files composing this frame
		"""
		return copy.copy(self._files)

	@property
	@throwIfInvalid
	def type(self):
		"""
		Returns ``qidata.DataType.DATASET``
		"""
		return DataType.FRAME

	@property
	@throwIfInvalid
	def mode(self):
		"""
		Specify the opening mode

		"r" => read-only mode
		"w" => read/write mode
		"""
		return "w" if self._xmp_file.rw else "r"

	@property
	@throwIfInvalid
	def metadata(self):
		return QiDataObject.metadata.__get__(self)

	@metadata.setter
	@throwIfInvalid
	def metadata(self, new_metadata):
		QiDataObject.metadata.__set__(self, new_metadata)

	# ──────────
	# Public API

	def close(self):
		"""
		Closes the file frame after writing the metadata
		"""
		if self._is_closed:
			return
		if self.mode != "r":
			# Save annotations' metadata
			self._save(self._xmp_file, self._annotations)

			# Erase current frame content's metadata
			_raw_metadata = self._xmp_file.metadata[QIDATA_FRAME_NS]
			setattr(_raw_metadata, "files", list(self._files))

		self._xmp_file.close()
		self._is_closed = True

	def reloadMetadata(self):
		"""
		Erase metadata changes by reloading saved metadata
		"""
		self.metadata = self._load(self._xmp_file)

	# ───────────
	# Private API

	@throwIfInvalid
	def _open(self):
		"""
		Open the file
		"""
		self._is_closed = False
		self._xmp_file.__enter__()
		self.reloadMetadata()

		# Load content info stored in metadata
		_raw_metadata = self._xmp_file.metadata[QIDATA_FRAME_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			XMPHandlerMixin._removePrefix(data)
			self._files = set(data["files"])
		return self
