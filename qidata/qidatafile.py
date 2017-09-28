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
The ``qidata.qidatafile`` module provides the
:class:`qidata.qidatafile.QiDataFile` abstract class. It derives from
:class:`qidata.qidataobject.QiDataObject` and wraps the :mod:`xmp` package,
allowing to write in a file's metadata header if any. It also defines a
QiDataFile factory to easily open files as QiDataObjects.
"""

# Standard libraries
import abc
import copy
import os
import re
from collections import OrderedDict

# Third-party libraries
from xmp.xmp import XMPFile, registerNamespace

# Local modules
from qidata import DataType
from qidata.qidataobject import QiDataObject
import _mixin as xmp_tools

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

class QiDataFile(QiDataObject):

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
		if os.path.splitext(file_path)[1] == ".xmp":
			# If file is a .xmp, just read it normally
			# If the filename without xmp extension is an existing
			# file, then mark it as the real file opened
			xmp_path = file_path
			if os.path.exists(os.path.splitext(file_path)[0]):
				file_path = os.path.splitext(file_path)[0]

		elif os.path.exists(file_path + ".xmp"):
			# If there is an external annotation file, use it
			xmp_path = file_path + ".xmp"

		elif mode=="w":
			# If there is no external annotation file but we are in "w" mode
			# Copy the internal annotations in an external annotation file
			xmp_path = file_path + ".xmp"
			with XMPFile(file_path, rw=False) as _internal:
				with XMPFile(xmp_path, rw=True) as _external:
					_external.libxmp_metadata = _internal.libxmp_metadata
		else:
			# Open the internal annotations
			xmp_path = file_path


		# Store the file path
		self._file_path = file_path

		# And prepare the xmp file
		self._xmp_file = XMPFile(xmp_path, rw=(mode=="w"))
		self._is_closed = True
		self._open()

	# ──────────
	# Properties

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
			xmp_tools._save_annotations(self._xmp_file, self.annotations)
		self._xmp_file.close()
		self._is_closed = True

	@throwIfClosed
	def cancelChanges(self):
		"""
		Erase changes by reloading metadata from file
		"""
		# Re-load annotations
		self._loadAnnotations()

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
		self._loadAnnotations()
		return self

	@throwIfClosed
	def _loadAnnotations(self):
		"""
		Loads annotations
		"""
		# Load annotations
		self._annotations = xmp_tools._load_annotations(self._xmp_file)

	# ───────────────
	# Context Manager

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

	# ──────────────
	# Textualization

	def __unicode__(self):
		res_str = ""
		res_str += "File name: " + self.name + "\n"
		res_str += QiDataObject.__unicode__(self)
		return res_str
