# -*- coding: utf-8 -*-

# Standard libraries
from collections import OrderedDict
import copy
import glob
import os

# Third-party libraries
from xmp.xmp import XMPFile, registerNamespace
from strong_typing._textualize import textualize_sequence, textualize_mapping

# Local modules
import qidata
from qidata import qidataframe, DataType, _BaseEnum
from qidata.metadata_objects import Context
from qidata.qidataobject import QiDataObject, throwIfReadOnly
import _mixin as xmp_tools

QIDATA_CONTENT_NS=u"http://softbank-robotics.com/qidataset/1"
registerNamespace(QIDATA_CONTENT_NS, "qidataset")

METADATA_FILENAME = "metadata.xmp" # Place-holder

def isDataset(path):
    return os.path.isdir(path)\
             and os.path.isfile(os.path.join(path, METADATA_FILENAME))

class QiDataSet(object):

	class AnnotationStatus(_BaseEnum):
		"""
		AnnotationStatus represents the completeness of an annotation.
		For instance, if the "Face" metadata of "jdoe" is TOTAL, it means that
		all files have been annotated. This is a very valuable information.

		:Example:
			Imagine a file in the dataset has no "Face" annotation. Does it
			mean that there is no face visible in the file, or that the
			annotator forgot to annotate that specific file ? When the
			annotation is registered as TOTAL, it means that every file
			without a "Face" annotation has actually no face in it.
		"""
		PARTIAL = 0
		TOTAL = 1

	# ───────────
	# Constructor

	def __init__(self, folder_path, mode="r"):
		"""
		Open a QiDataSet.

		:param folder_path: path to the data set to open
		:type folder_path: str
		:param mode: opening mode, "r" for reading, "w" for writing
		:type mode: str

		.. warnings::

			The folder must exist and cannot be created if it does not.

		.. note::

			"r" mode means the folder is expected to contain a file named
			"metadata.xmp" of a certain form (an empty file is not enough).
			Otherwise, opening will fail.
			In "w" mode, any folder can be opened. If no "metadata.xmp" file is
			present, one will be created. If there is one, it WILL NOT BE TRUNCATED
			(unlike the regular "w" mode of file opening).
		"""
		if not os.path.isdir(folder_path):
			raise IOError("%s is not a valid folder"%folder_path)

		self._folder_path = folder_path
		metadata_path = os.path.join(folder_path, METADATA_FILENAME)
		if not isDataset(folder_path):
			if mode == "r" :
				# This is not an existing qidata dataset and we are not allowed
				# to create it
				raise IOError(
				  "Given path is not a QiData dataset: %s does not exist"%(
				  	METADATA_FILENAME
				  )
				)
			elif mode=="w":
				# Folder is not a data set but we can turn it into one

				# We need XMP to create an empty metadata.xmp
				# Open it with xmp so that metadata.xmp is created
				with XMPFile(metadata_path, rw=True):
					pass

		self._annotation_content = dict()
		self._files_type = dict()
		self._xmp_file = XMPFile(metadata_path, rw=(mode=="w"))
		self._is_closed = True
		self._streams = dict()
		self._frames = list()
		self._open()

	# ──────────
	# Properties

	@property
	def annotations_available(self):
		"""
		Returns a list of all annotations references that are present at least
		once in the dataset, with their status

		:Example:
			>>> with QiDataSet("dummy/dataset", "r") as d:
			>>>     d.annotations_available
			>>> {("jdoe", "Property"): QiDataSet.AnnotationStatus.PARTIAL)}
		"""
		return copy.deepcopy(self._annotation_content)

	@property
	def annotators(self):
		"""
		Returns the list of people who annotated at least one file of the
		dataset
		"""
		return set([i[0] for i in self._annotation_content])

	@property
	def children(self):
		"""
		Return the list of supported files contained by the data set.
		"""
		ret = [fn
		           for fn in os.listdir(self.name)
		               if (qidata.isSupportedDataFile(fn))
		      ]
		ret.sort()
		return ret

	@property
	def context(self):
		"""
		Describes the context around the data sets.

		:rtype: qidata.metadata_objects.context.Context
		"""
		return self._context

	@context.setter
	@throwIfReadOnly
	def context(self, new_context):
		if isinstance(new_context, Context):
			self._context = new_context
		else:
			raise TypeError("Wrong type given to update context property")

	@property
	def datatypes_available(self):
		"""
		Returns a list of all data types present in the dataset
		"""
		return set([DataType[i] for i in self._files_type.keys()])

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
		Give the folder path
		"""
		return self._folder_path

	# ──────────
	# Public API

	def createNewStream(self, name, timestamp_file_pairs):
		"""
		Creates a new set of files which should be considered as part
		of the same data stream

		:param name: Name given to the stream
		:type name: str
		:param timestamp_file_pairs: List of pairs of filename and timestamp
		:type timestamp_file_pairs: list
		:raises: AttributeError if an empty list is given
		:raises: TypeError if the given files have different types
		"""
		if len(timestamp_file_pairs) == 0:
			raise AttributeError(
			        "At least one file is needed to create a stream"
			      )
		with self.openChild(timestamp_file_pairs[0][1]) as f:
			data_type = f.type
		for i in range(1,len(timestamp_file_pairs)):
			if timestamp_file_pairs[i][1] in self._files_type[str(data_type)]:
				continue
			with self.openChild(timestamp_file_pairs[i][1]) as f:
				if data_type == f.type:
					continue
			raise TypeError("Given files are not all of the same type")
		self._streams[name] = (data_type, dict(timestamp_file_pairs))

	def close(self):
		"""
		Closes the dataset after writing the metadata
		"""
		if self.mode != "r":
			# Erase current dataset content's metadata
			_raw_metadata = self._xmp_file.metadata[QIDATA_CONTENT_NS]
			for key in _raw_metadata.attributes():
				del _raw_metadata[key]

			# Save new dataset content's metadata
			for (key, value) in self._annotation_content.iteritems():
				setattr(
				    _raw_metadata.annotation_content,
				    key[0],
				    {key[1]:value}
				)

			setattr(
			    _raw_metadata,
			    "files_type",
			    self._files_type
			)

			setattr(
			    _raw_metadata,
			    "context",
			    self.context
			)

			# Save data streams (they need to be a little be reworked to fit
			# XMP base rules, namely numbers cannot be keys so we add the
			# letter "t" in front of the timestamps)
			tmp_streams = dict()
			for stream_name, stream in self._streams.iteritems():
				tmp_streams[stream_name] = (stream[0],dict())
				for (timestamp,filename) in stream[1].iteritems():
					tmp_streams[stream_name][1]["t%d.%09d"%timestamp] = filename

			setattr(_raw_metadata, "streams", tmp_streams)

		self._xmp_file.close()
		for f in self._frames:
			f.close()
		self._is_closed = True

	def examineContent(self):
		"""
		Examine all dataset's files to infer content information.

		For every supported file contained in the dataset, this function will:
		 - check if a DataType is already defined and infer one from the file
		   extension if not.
		 - open the file and look for present annotations

		Once all files have been studied, remaining annotations will be updated
		with any known status that might have been present before this function
		was called.
		"""
		_annotation_content = dict()
		self._files_type = dict()
		for name in self.children:
			path = os.path.join(self._folder_path, name)
			with qidata.open(path, "r") as _f:
				for annotator, annotations in _f.annotations.iteritems():
					for annotation_type in annotations.keys():
						_annotation_content[
						  (
						    annotator,
						    annotation_type
						  )
						] = QiDataSet.AnnotationStatus.PARTIAL
				if not self._files_type.has_key(str(_f.type)):
					self._files_type[str(_f.type)] = []
				self._files_type[str(_f.type)].append(name)

		for _f in self.getAllFrames():
			for annotator, annotations in _f.annotations.iteritems():
				for annotation_type in annotations.keys():
					_annotation_content[
					  (
					    annotator,
					    annotation_type
					  )
					] = QiDataSet.AnnotationStatus.PARTIAL

		# For all discovered annotation, grab the previously known status
		# If an annotation had a status before but was not seen, it does not
		# need to be kept, as the annotation probably disappeared from the
		# dataset
		for key in _annotation_content:
			if self._annotation_content.has_key(key):
				_annotation_content[key] = self._annotation_content[key]

		self._annotation_content = _annotation_content
		# files_info = dict()

		# # Keep track of the knowledge we have so far
		# if not hasattr(self, "_content"):
		# 	type_map = dict()
		# 	known_status = dict()
		# else:
		# 	type_map = self._content._type_content
		# 	known_status = self._content._data

		# supported_subpaths = self.children
		# for path in supported_subpaths:
		# 	if isDataset(path):
		# 		# Avoid it for the moment
		# 		# But later we will have to handle sub-datasets
		# 		continue

		# 	# Search if a specific type was set for this file
		# 	# If it does, then use it
		# 	# Otherwise, infer its type from the file extension
		# 	for data_type, file_list in type_map.iteritems():
		# 		if path in file_list:
		# 			file_type = data_type
		# 			break
		# 	else:
		# 		file_type = qidatafile.getFileDataType(path)

		# 	# And then add that file in the appropriate category
		# 	if not files_info.has_key(str(file_type)):
		# 		files_info[str(file_type)] = []
		# 	files_info[str(file_type)].append(path)

			# # Finally, open the file to look for annotations
			# with self.openChild(path, "r") as _child:
			# 	for child_annotator in _child.annotations.keys():
		# 			if not annotations_info.has_key(child_annotator):
		# 				annotations_info[child_annotator] = dict()
		# 			for metadata_type in _child.metadata[child_annotator]:
		# 				annotations_info[child_annotator][metadata_type] = False

		# # Create new content
		# self._content = QiDataSetContent(files_info, annotations_info)

		# # For each TOTAL status, update the new content
		# # Indeed, a TOTAL status is an input from a human and therefore must
		# # not be erased by the program.
		# # Any PARTIAL status present before and not in the new
		# # content would mean that NO file was found with this
		# # annotation from this person => annotations were probably
		# # removed => no need to re-add the information.
		# for key, value in known_status.iteritems():
		# 	if value == True:
		# 		self._content._data[key] = True

	@staticmethod
	def filter(
	    dataset_list,
	    only_annotated_by=None,
	    only_with_annotations=None,
	    only_total_annotations=False):

		"""
		Filters out dataset not fitting the given criteria.

		:param dataset_list: List of folders to filter
		:type dataset_list: list
		:param only_annotated_by: List of requested annotators
		:type only_annotated_by: list
		:param only_with_annotations: List of requested annotation types
		:type only_with_annotations: list
		:param only_total_annotations: States if only total annotations should
		be considered
		:type only_total_annotations: bool

		:Example:
			The following command will only accept datasets containing total
			"Property" annotations made by "jdoe" or "jsmith"
			>>> QiDataSet.filter(
			...     dataset_lists,["jdoe", "jsmith"],["Property"], True)

			The following command will only accept datasets containing "Dummy"
			and "Property" annotations (total or partial) made by "jdoe"
			exclusively
			>>> QiDataSet.filter(
			...     dataset_lists,["jdoe"],["Property","Dummy"], False)
		"""
		filtered = []

		for dataset_path in dataset_list:
			with QiDataSet(dataset_path,"r") as ds:
				for a_ref, a_status in ds.annotations_available.iteritems():
					if only_total_annotations\
					   and a_status==QiDataSet.AnnotationStatus.PARTIAL:
						continue
					if only_annotated_by is not None\
					   and not a_ref[0] in only_annotated_by:
						continue
					if only_with_annotations is not None\
					   and not a_ref[1] in only_with_annotations:
						continue
					filtered.append(dataset_path)
					break
		return filtered

	def getAllFilesOfType(self, type_name):
		"""
		Returns all the file names of a specific type

		:param type_name: Requested type
		:type type_name: ``qidata.DataType`` or str
		:return: List of filenames
		"""
		try:
			return copy.deepcopy(self._files_type[str(type_name)])
		except KeyError:
			# Check given type
			try:
				_ = DataType[str(type_name)]
			except KeyError:
				raise TypeError("%s is not a valid DataType"%type_name)
			# Type name is valid, but there is no file associated to it
			return []

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
		:raises: KeyError if stream_name does not exist
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
		:raises: KeyError if stream does not exist
		:raises: ValueError if file is not in the dataset
		"""
		_tmp=file_timestamp_pair_to_add
		if not _tmp[1] in self.children:
			raise ValueError("Given file is not in the dataset")
		self._streams[stream_name][1][_tmp[0]]=_tmp[1]

	def removeFromStream(self, stream_name, file_to_remove):
		"""
		Remove a file from a data stream

		:param stream_name: Name of the stream to modify
		:type stream_name: str
		:param file_to_remove: Name of the file to remove
		:type file_to_remove: str
		:raises: KeyError if stream does not exist
		:raises: ValueError if file is not in the stream
		"""
		for (ts, filename) in self._streams[stream_name][1].iteritems():
			if filename == file_to_remove:
				self._streams[stream_name][1].pop(ts)
				break
		else:
			raise ValueError("Given file is not in the stream")
		# si le stream devient vide, on devrait le supprimer

	@throwIfReadOnly
	def createNewFrame(self, *files):
		"""
		Creates a new association of files in a :class:``QiDataFrame``

		:param files: files to include in the frame
		:param files: str
		:return: Created frame
		:rtype: :class:``QiDataFrame``
		:raises: TypeError if not enough files are given
		"""
		if len(files) < 2:
			raise TypeError("createNewFrame needs at least 2 files (%d given)"%len(files))
		frame = qidataframe.QiDataFrame.create(files, self._folder_path)
		self._frames.append(frame)
		return frame

	@throwIfReadOnly
	def removeFrame(self, *files):
		"""
		Remove a frame from the dataset

		:param files: Files composing the frame to remove.

		..note::
			A frame cannot be composed of only one file. So if only one file is
			given as argument, it is considered to be directly the frame to
			remove.
		"""
		if len(files) == 1:
			f=files[0]
		else:
			f = self.getFrame(*files)
		if f is None:
			return
		try:
			self._frames.remove(f)
		except ValueError:
			pass
		else:
			f.close()
			f._is_valid=False
			os.remove(f._file_path)

	def getAllFrames(self):
		"""
		Returns all created frames

		:return: Every frames of the dataset
		:rtype: list
		"""
		return copy.copy(self._frames)

	def getFrame(self, *files):
		"""
		Get an already created frame

		:param files: files composing the researched frame
		:param files: str
		:return: Researched frame
		:rtype: :class:``QiDataFrame``
		:raises: IndexError if no frame matches the requested files
		"""
		try:
			return [f for f in self._frames if set(files)==f._files][0]
		except IndexError:
			return None

	def openChild(self, name):
		"""
		Open QiDataFile contained here

		:param name: Name of the file or folder to open
		:type name: str

		.. note::
			The opening mode used to open children is the opening mode of the
			QiDataSet itself
		"""
		path = os.path.join(self._folder_path, name)
		if not name in self.children:
			raise IOError("%s is not a child of the current dataset"%name)
		if os.path.isfile(path):
			return qidata.open(path, self.mode)
		# elif os.path.isdir(path):
		# 	return QiDataSet(path, self.mode)
		else:
			raise IOError("%s is neither a file nor a folder"%name)

	def setAnnotationStatus(self, annotator_name, metadata_type, is_total):
		"""
		Set an annotation's status

		:param annotator_name: The annotator who made the full annotation
		:type annotator_name: str
		:param metadata_type: The annotation type that was fully annotated
		:type metadata_type: str
		:param is_total: True if the annotation is covering the whole dataset
		:type is_total: bool

		.. warning::

			Annotations CANNOT and MUST NOT be declared "Total" automatically.
			The value of such a statement can only be guaranteed if it emanates
			from a human.
		"""
		self._annotation_content[(annotator_name,metadata_type)] = \
		  QiDataSet.AnnotationStatus.TOTAL\
		   if is_total else QiDataSet.AnnotationStatus.PARTIAL

	# ───────────
	# Private API

	def _open(self):
		"""
		Open the data set
		"""
		frames = glob.glob(self._folder_path+"/*.frame.xmp")
		for frame in frames:
			self._frames.append(
				qidataframe.QiDataFrame(
					frame,
					self.mode
				)
			)
		self._xmp_file.__enter__()
		self._is_closed = False

		# Load content info stored in metadata
		_raw_metadata = self._xmp_file.metadata[QIDATA_CONTENT_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			xmp_tools._removePrefixes(data)
			self._annotation_content = dict()
			if data.has_key("annotation_content"):
				content = data["annotation_content"]
				for annotator in content:
					for annot_type, value in content[annotator].iteritems():
						value = QiDataSet.AnnotationStatus[value]
						self._annotation_content[(annotator,annot_type)]=value

			if data.has_key("context"):
				self._context = Context(**data["context"])
			else:
				self._context = Context()

			for file_type, file_list in data["files_type"].iteritems():
				self._files_type[file_type]=file_list

		# 	# In a previous version, files_info was counting the number of file
		# 	# of each type. In the current version, we store for each type the
		# 	# list of all the corresponding files. This allows users to define
		# 	# more specific types than those which can be infered from the file
		# 	# extension.
		# 	# So if files_info is a string and not a list, it means it is an
		# 	# "old" version, therefore we need to rework it.
		# 	if len(data["files_info"])>0\
		# 	   and isinstance(data["files_info"].values()[0], basestring):
		# 		# Current file info is wrong
		# 		# Examine content to get proper file info
		# 		files_info = dict()
		# 		supported_subpaths = self.children
		# 		for path in supported_subpaths:
		# 			if isDataset(path):
		# 				# Avoid it for the moment
		# 				# But later we will have to handle sub-datasets
		# 				continue
		# 			file_type = qidatafile.getFileDataType(path)
		# 			if not files_info.has_key(str(file_type)):
		# 				files_info[str(file_type)] = []
		# 			files_info[str(file_type)].append(path)
		# 		self._content._type_content = dict(files_info)

			# If streams are defined, load them. We have to go through the
			# whole structure to make sure that timestamps are properly
			# converted to float (after removal of the appended prefix letter
			# and filenames must be converted to string, as this is the type we
			# use, but they are saved as unicode)
			if data.has_key("streams") and len(data["streams"])>0:
				for stream_name, stream in data["streams"].iteritems():
					self._streams[stream_name] = [DataType[stream[0]],dict()]
					for (timestamp,filename) in stream[1].iteritems():
						_ts = tuple(map(int, timestamp[1:].split(".")))
						self._streams[stream_name][1][_ts] = str(filename)

		else:
			# if no content info was stored, infere it from the files
			self._context = Context()
			self.examineContent()
		return self

	# ───────────────
	# Context Manager

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close()

	# ──────────────
	# Textualization

	def __str__(self):
		return unicode(self).encode(encoding="utf-8")

	def __unicode__(self):
		# Path
		res_str = ""
		res_str += "Dataset path: " + self.name + "\n"

		# Types
		_da = [str(i) for i in self.datatypes_available]
		_da.sort()
		res_str += "Available types: " + textualize_sequence(
		                                                     _da,
		                                                     unicode
		                                                    ) + "\n"

		# Streams
		_sn = self._streams.keys()
		_sn.sort()
		print _sn
		_s = OrderedDict(
		                  [(name, "%d files"%len(self._streams[name][1]))\
		                      for name in _sn]
		                )
		res_str += "Available streams: " + textualize_mapping(
		                                                      _s,
		                                                      unicode
		                                                     ) + "\n"

		# Frames
		res_str += "Defined frames: %d\n"%len(self._frames)

		# Context
		res_str += "Context: " + unicode(self.context) + "\n"

		# Annotations
		res_str += "Available annotations: " + textualize_sequence(
		                                           self.annotations_available,
		                                           unicode
		                                       ) + "\n"
		return res_str