# -*- coding: utf-8 -*-
"""
The ``qidata.qidatafile`` module provides the
:class:`qidata.qidatafile.QiDataFile` abstract class. It derives from
:class:`qidata.qidataobject.QiDataObject` and wraps the :mod:`xmp` package,
allowing to write in a file's metadata header if any. It also defines a
QiDataFile factory to easily open files as QiDataObjects.
"""

# Standard libraries
import abc
import copy
import re
from collections import OrderedDict

# Third-party libraries
from xmp.xmp import XMPFile

# Local modules
from qidata.qidataobject import QiDataObject
from ._mixin import XMPHandlerMixin

class ClosedFileException(Exception):pass

def throwIfClosed(f):
	def wraps(*args):
		self=args[0]
		if self.closed:
			raise ClosedFileException("Trying to read/write on a closed file")
		return f(*args)
	return wraps

# def getFileDataType(path):
# 	"""
# 	Return type of data stored in given file

# 	:param path: Path of the file to test
# 	:type path: str
# 	:return: Type of the file
# 	:rtype: ``qidata.DataType``
# 	"""
# 	for pattern in LOOKUP_ITEM_MODEL:
# 		if pattern.match(path):
# 			return LOOKUP_ITEM_MODEL[pattern]
# 	raise TypeError("Data type not supported by QiDataFile")

class QiDataFile(QiDataObject, XMPHandlerMixin):

	# ───────────
	# Constructor

	def __init__(self, file_path, mode = "r"):
		"""
		Create and open a QiDataFile.
		QiDataFile wraps the xmp library specifically to store QiDataObjects under the
		QiData namespace.

		:param file_path: path to the file to open
		:type file_path: str
		:param mode: opening mode, "r" for reading, "w" for writing
		:param mode: str

		.. warnings::
			The mode behavior is different from the regular Python file mode.
			The file is NEVER created if it does not exist. Besides, opening
			an existing file in "w" mode does not overwrite it.
		"""
		self._file_path = file_path
		self._xmp_file = XMPFile(file_path, rw=(mode=="w"))
		self._is_closed = True
		self._open()

	# ──────────
	# Properties

	@abc.abstractproperty
	def type(self):
		"""
		Specify the type of data in the file

		:return: The type of this file
		:rtype: qidata.DataType
		"""

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
	def read_only(self):
		return ("r" == self.mode)

	@property
	def name(self):
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
			self._save_annotations(self._xmp_file, self.annotations)
		self._xmp_file.close()
		self._is_closed = True

	@throwIfClosed
	def reloadMetadata(self):
		"""
		Erase metadata changes by reloading saved metadata
		"""
		self._annotations = self._load_annotations(self._xmp_file)

	@throwIfClosed
	def addAnnotation(self, annotator, annotation, location=None):
		QiDataObject.addAnnotation(self, annotator, annotation, location)

	@throwIfClosed
	def removeAnnotation(self, annotator, annotation, location=None):
		QiDataObject.removeAnnotation(self, annotator, annotation, location)

	# ───────────
	# Private API

	def _open(self):
		"""
		Open the file
		"""
		# file.__init__(self, self._file_path, "r")
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


# ─────────────────
# Specialized files

from qidata.qidataimagefile import QiDataImageFile
from qidata.qidataaudiofile import QiDataAudioFile

LOOKUP_ITEM_MODEL = {
    re.compile(".*\.png"): QiDataImageFile,
    re.compile(".*\.jpg"): QiDataImageFile,
    re.compile(".*\.wav"): QiDataAudioFile,
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
	for pattern in LOOKUP_ITEM_MODEL:
		if pattern.match(file_path):
			return LOOKUP_ITEM_MODEL[pattern](file_path, mode)
	raise TypeError("Data type not supported by QiDataFile")

# __all__=["open", "QiDataFile"]