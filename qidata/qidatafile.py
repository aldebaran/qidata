# -*- coding: utf-8 -*-

"""
The ``qidata.qidatafile`` module provides the ``QiDataFile`` class which is a ``QiDataObject``
wrapping the ``:mod:xmp`` package. It provides the access to a file's metadata through the
QiDataObject's interface.
"""

from xmp.xmp import XMPFile
from qidata import DataType
from qidata.qidataobject import QiDataObject
from collections import OrderedDict
import copy
import re
from _mixin import XMPHandlerMixin

# ──────────
# Data Items

LOOKUP_ITEM_MODEL = {
    re.compile(".*\.png"): DataType.IMAGE,
    re.compile(".*\.jpg"): DataType.IMAGE,
    re.compile(".*\.wav"): DataType.AUDIO
}

def isSupported(dataPath):
	"""
	Return True if file extension can be opened as QiDataFile

	:param path: Path of the file to test
	:type path: str
	:return: True if file is supported by qidata
	:rtype: bool
	"""
	for pattern in LOOKUP_ITEM_MODEL:
		if pattern.match(dataPath):
			return True
	return False

def getFileDataType(path):
	"""
	Return type of data stored in given file

	:param path: Path of the file to test
	:type path: str
	:return: Type of the file
	:rtype: ``qidata.DataType``
	"""
	for pattern in LOOKUP_ITEM_MODEL:
		if pattern.match(path):
			return LOOKUP_ITEM_MODEL[pattern]
	raise TypeError("Data type not supported")

def open(file_path, mode="r"):
	"""
	Open a file as a QiDataFile.
	This is the preferred way to open a QiDatafile.

	:param file_path: Path to the file to open
	:param mode: Mode of opening ("r" for reading, "w" for writing)
	:rtype: ``qidata.QiDataFile``
	:Example:
		>>> from qidata import qidatafile
		>>> myFile = qidatafile.open("path/to/file")

	.. warning::

		The mode behavior is different from the regular Python file mode.
		The file is NEVER created if it does not exist. Besides, opening
		an existing file in "w" mode does not overwrite it.
	"""
	return QiDataFile(file_path, mode)

class QiDataFile(QiDataObject, file, XMPHandlerMixin):

	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		"""
		Create and open a QiDataFile.
		QiDataFile wraps the xmp library specifically to store QiDataObjects under the
		QiData namespace.

		:param file_path: path to the file to open (str)
		:param mode: opening mode, "r" for reading, "w" for writing (str)

		.. warnings::
			The mode behavior is different from the regular Python file mode.
			The file is NEVER created if it does not exist. Besides, opening
			an existing file in "w" mode does not overwrite it.
		"""

		self._type = getFileDataType(file_path)
		self._file_path = file_path
		self._xmp_file = XMPFile(file_path, rw=(mode=="w"))
		# self._annotations = None
		self._is_closed = True
		self._open()

	# ──────────
	# Properties

	@property
	def raw_data(self):
		"""
		Return the content of the file as a string

		.. note::

			The content of the file is read-only and can only return the file as a string.
			To open it differently or to modify the content, use your regular methods/modules.
		"""
		raw_data = self.read()
		self.seek(0)
		return raw_data

	@property
	def type(self):
		"""
		Specify the type of data in the file

		Return :class:`qidata.DataType`
		"""
		return self._type

	@property
	def closed(self):
		"""
		True if the file is closed
		"""
		return self._is_closed

	@property
	def mode(self):
		"""
		Specify the file mode

		"r" => read-only mode
		"w" => read/write mode
		"""
		return "w" if self._xmp_file.rw else "r"

	@property
	def path(self):
		"""
		Give the file path
		"""
		return self._file_path

	# ──────────
	# Public API

	def close(self):
		"""
		Closes the file after writing the metadata
		"""
		if self.mode != "r":
			self._save(self._xmp_file, self.metadata)
		self._xmp_file.close()
		file.close(self)
		self._is_closed = True

	def reloadMetadata(self):
		"""
		Erase metadata changes by reloading saved metadata
		"""
		self.metadata = self._load(self._xmp_file)

	# ───────────
	# Private API

	def _open(self):
		"""
		Open the file
		"""
		file.__init__(self, self._file_path, "r")
		self._xmp_file.__enter__()
		self._is_closed = False
		self.reloadMetadata()
		return self

	# ───────────────
	# Context Manager

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

__all__=["open", "QiDataFile"]