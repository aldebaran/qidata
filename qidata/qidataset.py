# -*- coding: utf-8 -*-

# Standard Library
import __builtin__
import os
import copy

# xmp
from xmp.xmp import XMPFile, registerNamespace

# qidata
from qidata import DataType, qidatafile
from qidata.qidataobject import QiDataObject
from _mixin import XMPHandlerMixin

QIDATA_CONTENT_NS=u"http://softbank-robotics.com/qidataset/1"
registerNamespace(QIDATA_CONTENT_NS, "qidataset")

METADATA_FILENAME = "metadata.xmp" # Place-holder

def isDataset(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, METADATA_FILENAME))

def isMetadataFile(path):
    return  os.path.isfile(path) and os.path.basename(path) == METADATA_FILENAME

class QiDataSetContent:
	"""
	Describes the content of a dataset

	It contains information about:
	 - the available types of data
	 - the annotators
	 - the type of metadata contained
	 - the "status" of the metadata

	.. note::
		"status" can be "partial" (``False``) or "total" (``True``).
		It represents the completeness of a certain metadata.
		For instance, if the "Face" metadata of "jdoe" is
		"total", it means that all files have been annotated. This
		is a very valuable information.

		Imagine a file in the data set has no "Face" metadata. Does it
		mean that there is no face visible in the file, or that the
		annotator did not annotate that specific file ? When the
		metadata is registered as "total", it means that every file
		without a "Face" metadata has actually no face in it.

	.. warning::
		Because of what was just said, metadata CANNOT and MUST NOT
		be declared "Total" automatically. The value of such a statement
		can only be guaranteed if it emanates from a human.
	"""

	def __init__(self, files_info, metadata_info=dict(), **kwargs):
		"""
		:param files_info: Contains the number of files of each type
		:type files_info: dict
		:param metadata_info: Status of the different metadatas
		:type metadata_info: dict

		Other keywords arguments are ignored

		.. note::
			metadata_info contains a 2-layer dict to describe the status
			of all metadata types per annotator.

		:Example:
			>>> metadata_info["jdoe"]["Face"]
			False # regarding Face metadata, jdoe did not totally annotate the dataset
		"""
		# Create data
		self._data = dict()
		for annotator, subdict in metadata_info.iteritems():
			for annotation_type, status in subdict.iteritems():
				self._data[(annotator, annotation_type)] = True if status =="True" else False

		self._type_content = dict(files_info) #: list of data types with number of file

		# _content is a list of triplet whose each is
		# (annotator_name, annotation_type, annotation_is_total)

	def toDict(self):
		out = dict(metadata_info=dict(), files_info=self._type_content)
		for k,v in self._data.iteritems():
			if not out["metadata_info"].has_key(k[0]):
				out["metadata_info"][k[0]] = dict()
			out["metadata_info"][k[0]][k[1]] = v
		return out

	@property
	def annotators(self):
		"""
		Returns the list of annotators that made at least one total
		annotation
		"""
		return list(set([k[0] for k,v in self._data.iteritems() if v]))

	@property
	def annotation_types(self):
		"""
		Returns the list of annotations type that are totally annotated by at
		least one annotator
		"""
		return list(set([k[1] for k,v in self._data.iteritems() if v]))

	@property
	def file_types(self):
		"""
		Returns the list of file types present in the dataset
		"""
		# dict values are the number of files for each type
		# it will help to track dataset changes
		return self._type_content.keys()

	@property
	def partial_annotations(self):
		"""
		Returns a list of tuple containing all non-total annotations
		"""
		return [k for k,v in self._data.iteritems() if not v]

	def setMetadataTotalityStatus(self, annotator_name, metadata_type, is_total):
		"""
		Set an annotation's totality status over the dataset

		.. warning:: This should always come from a human decision

		:param annotator_name: The annotator who made the full annotation
		:param metadata_type: The annotation type that was fully annotated
		:param is_total: True if the annotation is covering the whole dataset
		"""
		self._data[(annotator_name,metadata_type)] = is_total

class QiDataSet(QiDataObject, XMPHandlerMixin):

	# ───────────
	# Constructor

	def __init__(self, folder_path, mode="r"):
		"""
		Open a QiDataSet.

		:param folder_path: path to the data set to open (str)
		:param mode: opening mode, "r" for reading, "w" for writing (str)

		.. warnings::

			The folder must exist and cannot be created if it does not.

		.. note::

			"r" mode means the folder is expected to contain a file named
			"metadata.xmp". If it does not (if it is a regular folder) opening
			will fail).
			In "w" mode, any folder can be opened. If no "metadata.xmp" file is
			present, one will be created. If there is one, it WILL NOT BE TRUNCATED
			(unlike the regular "w" mode of file opening).
		"""

		metadata_path = os.path.join(folder_path, "metadata.xmp")
		if not os.path.isdir(folder_path):
			raise IOError("%s is not a valid folder"%folder_path)
		self._folder_path = folder_path
		if not isDataset(folder_path):
			if mode == "r" :
				# This is not an existing qidata dataset and we are not allowed to create it
				raise IOError("Given path is not a QiData dataset: metadata.xmp does not exist")
			elif mode=="w":
				# Folder is not a data set but we can turn it into one

				# We need XMP to create an empty metadata.xmp
				# Open it with xmp so that metadata.xmp is created
				with XMPFile(os.path.join(folder_path, "metadata.xmp"), rw=True):
					pass

		self._xmp_file = XMPFile(metadata_path, rw=(mode=="w"))
		self._is_closed = True
		self._streams = dict()
		self._open()

	# def __del__(self):
	# 	if not self.closed:
	# 		self.close()

	# ──────────
	# Properties

	@property
	def raw_data(self):
		"""
		Return a list with the data set's children and content
		"""
		return (self.children, self.content)

	@property
	def type(self):
		"""
		Returns ``qidata.DataType.DATASET``
		"""
		return DataType.DATASET

	@property
	def closed(self):
		"""
		True if the data set is closed
		"""
		return self._is_closed

	@property
	def mode(self):
		"""
		Specify the opening mode

		"r" => read-only mode
		"w" => read/write mode
		"""
		return "w" if self._xmp_file.rw else "r"

	@property
	def read_only(self):
		"""
		States if the object is protected against modification
		"""
		return ("r" == self.mode)

	@property
	def path(self):
		"""
		Give the folder path
		"""
		return self._folder_path

	@property
	def children(self):
		"""
		Return the list of supported files and data sets contained
		by the data set.
		"""
		ret = [fn
		           for fn in os.listdir(self.path)
		               if (qidatafile.isSupported(fn) or isDataset(fn))
		      ]
		ret.sort()
		return ret

	@property
	def content(self):
		"""
		Return all information given or infered from the contained files
		metadata

		:rtype: ``qidata.qidataset.QiDataSetContent``

		.. note::
			This is especially useful to discriminate which data sets to use.
			It is for instance possible to quickly find which data sets contains
			"Face" annotations.
		"""
		return self._content

	# ──────────
	# Public API

	def openChild(self, name, mode):
		"""
		Open QiDataFile or QiDataSet contained here

		:param name: Name of the file or folder to open
		:param mode: Opening mode (see ``qidata.QiDataFile`` and ``qidata.QiDataSet``)

		.. note::
			Opening the dataset in "r" mode does not prevent from opening its files in
			"w" mode
		"""
		path = os.path.join(self._folder_path, name)
		if not name in self.children:
			raise IOError("%s is not a child of the current dataset"%name)
		if os.path.isfile(path):
			return qidatafile.open(path, mode)
		elif os.path.isdir(path):
			return QiDataSet(path, mode)
		else:
			raise IOError("%s is neither a file nor a folder"%name)

	def close(self):
		"""
		Closes the dataset after writing the metadata
		"""
		if self.mode != "r":
			# Save annotations' metadata
			self._save(self._xmp_file, self._annotations)

			# Erase current dataset content's metadata
			_raw_metadata = self._xmp_file.metadata[QIDATA_CONTENT_NS]
			for key in _raw_metadata.attributes():
				del _raw_metadata[key]

			# Save new dataset content's metadata
			content_dict = self._content.toDict()
			for key in content_dict:
				setattr(_raw_metadata, key, content_dict[key])

			# Save data streams (they need to be a little be reworked to fit
			# XMP base rules, namely numbers cannot be keys so we add the
			# letter "t" in front of the timestamps)
			tmp_streams = dict()
			for stream_name, stream in self._streams.iteritems():
				tmp_streams[stream_name] = (stream[0],dict())
				for (timestamp,filename) in stream[1].iteritems():
					tmp_streams[stream_name][1]["t"+str(timestamp)] = filename

			setattr(_raw_metadata, "streams", tmp_streams)

		self._xmp_file.close()
		self._is_closed = True

	def getAllFilesOfType(self, type_name):
		"""
		Returns all the file names of a specific type

		:param type_name: Requested type
		:type type_name: ``qidata.DataType`` or str
		:return: List of filenames
		"""
		return self._content._type_content.get(str(type_name), [])

	def reloadMetadata(self):
		"""
		Erase metadata changes by reloading saved metadata
		"""
		self.metadata = self._load(self._xmp_file)

	def examineContent(self):
		"""
		Examine all dataset's files to infer content information.

		This will update the ``content`` property
		"""
		files_info = dict()
		annotations_info = dict()

		supported_subpaths = self.children
		for path in supported_subpaths:
			if isDataset(path):
				# Avoid it for the moment
				# But later we will have to handle sub-datasets
				continue
			file_type = qidatafile.getFileDataType(path)
			if not files_info.has_key(str(file_type)):
				files_info[str(file_type)] = []
			files_info[str(file_type)].append(path)
			with self.openChild(path, "r") as _child:
				for child_annotator in _child.metadata.keys():
					if not annotations_info.has_key(child_annotator):
						annotations_info[child_annotator] = dict()
					for metadata_type in _child.metadata[child_annotator]:
						annotations_info[child_annotator][metadata_type] = False

		# Create empty content if one is not already created
		if not hasattr(self, "_content"):
			self._content = QiDataSetContent(files_info, annotations_info)
		else:
			# Save the previous annotation status
			# files don't need to be saved as only the new list matters
			old_content = self._content._data

			# Create a new content from what was discovered
			self._content = QiDataSetContent(files_info, annotations_info)

			# For each TOTAL status, update the new content
			# Indeed, a TOTAL status is an input from a human
			# and therefore must not be erased by the program
			# Any PARTIAL status present before and not in the new
			# content would mean that NO file was found with this
			# annotation from this person => annotations were probably
			# removed => no need to re-add the information.
			for key, value in old_content.iteritems():
				if value == True:
					self._content._data[key] = True

	def setTypeOfFile(self, filename, data_type):
		"""
		Changes the registered type of a file

		:param filename: Name of the file whose type will change
		:param data_type: New data type
		:type data_type: ``qidata.DataType`` or str
		"""
		# Check given type
		try:
			_ = DataType[data_type]
		except KeyError:
			try:
				_ = DataType(data_type)
			except ValueError:
				raise TypeError("%s is not a valid DataType"%data_type)

		# Search for file in current type mapping
		for old_data_type in self._content.file_types:
			try:
				self._content._type_content[old_data_type].remove(filename)
			except ValueError:
				continue
			if len(self._content._type_content[old_data_type]) == 0:
				self._content._type_content.pop(old_data_type)
			break
		else:
			# If not found check if the file is actually in the dataset
			if not filename in self.children:
				raise ValueError("%s is not part of this QiDataSet"%filename)

		# Add the file in the type mapping
		if not self._content._type_content.has_key(str(data_type)):
			self._content._type_content[str(data_type)] = []
		self._content._type_content[str(data_type)].append(filename)

	def createNewStream(self, data_type, name, file_timestamp_pairs):
		"""
		Creates a new set of files which should be considered as part
		of the same data stream

		:param data_type: Type of the created data stream
		:type data_type: ``qidata.DataType``
		:param name: Name given to the stream
		:type name: str
		:param file_timestamp_pairs: List of pairs of filename and timestamp
		:type file_timestamp_pairs: list
		"""
		self._streams[name] = (data_type, dict(file_timestamp_pairs))

	def getAllStreams(self):
		"""
		Returns all declared streams

		:return: Every stream known by the data set
		:rtype: dict
		"""
		return copy.deepcopy(
			dict(
				(name, data[1]) for (name, data) in self._streams.iteritems()
			)
		)

	def getStreamsOfType(self, data_type):
		"""
		Returns all streams of a specific type

		:param data_type: Requested data type
		:type data_type: ``qidata.DataType``
		:return: Every stream of the requested type known by the data set
		:rtype: dict
		"""
		return copy.deepcopy(
			dict(
				(name, data[1]) for (name, data) in self._streams.iteritems() if data[0]==data_type
			)
		)

	def getStream(self, stream_name):
		"""
		Returns the requested stream

		:param stream_name: Requested data stream
		:type stream_name: str
		:return: The requested stream
		:rtype: dict
		"""
		return copy.deepcopy(self._streams[stream_name][1])

	def getStreamType(self, stream_name):
		"""
		Returns the type of a specific stream

		:param stream_name: Data stream of interest
		:type stream_name: str
		:return: The requested stream's data type
		:rtype: ``qidata.DataType``
		"""
		return self._streams[stream_name][0]

	def addToStream(self, stream_name, file_timestamp_pair_to_add):
		"""
		Add a pair (timestamp, file name) to a data stream

		:param stream_name: Name of the stream to modify
		:type stream_name: str
		:param file_timestamp_pair_to_add: Pair of filename and timestamp
		:type file_timestamp_pair_to_add: tuple
		"""
		_tmp=file_timestamp_pair_to_add
		self._streams[stream_name][1][_tmp[0]]=_tmp[1]

	def removeFromStream(self, stream_name, file_to_remove):
		"""
		Remove a file from a data stream

		:param stream_name: Name of the stream to modify
		:type stream_name: str
		:param file_to_remove: Name of the file to remove
		:type file_to_remove: str
		"""
		for (ts, filename) in self._streams[stream_name][1].iteritems():
			if filename == file_to_remove:
				self._streams[stream_name][1].pop(ts)
				break
			# si le stream devient vide, on devrait le supprimer

	@staticmethod
	def contentFromPath(folder_path):
		"""
		Returns the content of a dataset at the given path

		:param folder_path: Path from where to retrieve data set content

		.. note::
			This is especially useful for filtering the datasets over one condition
		"""
		with QiDataSet(folder_path) as _tmp:
			return _tmp.content

	# ───────────
	# Private API

	def _open(self):
		"""
		Open the data set
		"""
		self._xmp_file.__enter__()
		self._is_closed = False
		self.reloadMetadata()

		# Load content info stored in metadata
		_raw_metadata = self._xmp_file.metadata[QIDATA_CONTENT_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			XMPHandlerMixin._removePrefix(data)
			self._content = QiDataSetContent(**data)

			if len(data["files_info"])>0\
			   and isinstance(data["files_info"].values()[0], basestring):
				# Current file info is wrong
				# Examine content to get proper file info
				files_info = dict()
				supported_subpaths = self.children
				for path in supported_subpaths:
					if isDataset(path):
						# Avoid it for the moment
						# But later we will have to handle sub-datasets
						continue
					file_type = qidatafile.getFileDataType(path)
					if not files_info.has_key(str(file_type)):
						files_info[str(file_type)] = []
					files_info[str(file_type)].append(path)
				self._content._type_content = dict(files_info)
			# If streams are defined, load them. We have to go through the
			# whole structure to make sure that timestamps are properly
			# converted to float (after removal of the appended prefix letter
			# and filenames must be converted to string, as this is the type we
			# use, but they are saved as unicode)
			if data.has_key("streams") and len(data["streams"])>0:
				for stream_name, stream in data["streams"].iteritems():
					self._streams[stream_name] = [DataType[stream[0]],dict()]
					for (timestamp,filename) in stream[1].iteritems():
						self._streams[stream_name][1][float(timestamp[1:])] = str(filename)

		else:
			# if no content info was stored, infere it from the files
			self.examineContent()
		return self

	# ───────────────
	# Context Manager

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()
