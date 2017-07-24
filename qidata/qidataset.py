# -*- coding: utf-8 -*-

# Standard libraries
import copy
import os

# Third-party libraries
from xmp.xmp import XMPFile, registerNamespace

# Local modules
from qidata import qidatafile, DataType, _BaseEnum
from qidata.qidataobject import QiDataObject
from ._mixin import XMPHandlerMixin
# from qidata.exceptions import ReadOnlyException, throwIfReadOnly

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
		self._files_type = set()
		self._xmp_file = XMPFile(metadata_path, rw=(mode=="w"))
		self._is_closed = True
		# self._streams = dict()
		# self._frames = list()
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
			>>> [("jdoe", "Property", QiDataSet.AnnotationStatus.PARTIAL)]
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
		               if (qidatafile.isSupported(fn))
		      ]
		ret.sort()
		return ret

	@property
	def datatypes_available(self):
		"""
		Returns a list of all data types present in the dataset
		"""
		return copy.deepcopy(self._files_type)

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
			    list(self._files_type)
			)

		# 	# Save data streams (they need to be a little be reworked to fit
		# 	# XMP base rules, namely numbers cannot be keys so we add the
		# 	# letter "t" in front of the timestamps)
		# 	tmp_streams = dict()
		# 	for stream_name, stream in self._streams.iteritems():
		# 		tmp_streams[stream_name] = (stream[0],dict())
		# 		for (timestamp,filename) in stream[1].iteritems():
		# 			tmp_streams[stream_name][1]["t%d.%09d"%timestamp] = filename

		# 	setattr(_raw_metadata, "streams", tmp_streams)

		self._xmp_file.close()
		# for f in self._frames:
		# 	f.close()
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
		self._annotation_content = dict()
		self._files_type = set()
		for name in self.children:
			path = os.path.join(self._folder_path, name)
			with qidatafile.open(path, "r") as _f:
				for annotator, annotations in _f.annotations.iteritems():
					for annotation_type in annotations.keys():
						self._annotation_content[
						  (
						    annotator,
						    annotation_type
						  )
						] = QiDataSet.AnnotationStatus.PARTIAL
				self._files_type.add(_f.type)
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
	def filter(dataset_list,
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
			return qidatafile.open(path, self.mode)
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
		# frames = glob.glob(self._folder_path+"/*.frame.xmp")
		# for frame in frames:
		# 	self._frames.append(
		# 		qidataframe.QiDataFrame(
		# 			frame,
		# 			self.mode
		# 		)
		# 	)
		self._xmp_file.__enter__()
		self._is_closed = False

		# Load content info stored in metadata
		_raw_metadata = self._xmp_file.metadata[QIDATA_CONTENT_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			XMPHandlerMixin._removePrefixes(data)
			content = data["annotation_content"]
			self._annotation_content = dict()
			for annotator in content:
				for annotation_type, value in content[annotator].iteritems():
					value = QiDataSet.AnnotationStatus[value]
					self._annotation_content[(annotator,annotation_type)]=value

			for file_type in data["files_type"]:
				self._files_type.add(DataType[file_type])

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

			# # If streams are defined, load them. We have to go through the
			# # whole structure to make sure that timestamps are properly
			# # converted to float (after removal of the appended prefix letter
			# # and filenames must be converted to string, as this is the type we
			# # use, but they are saved as unicode)
			# if data.has_key("streams") and len(data["streams"])>0:
			# 	for stream_name, stream in data["streams"].iteritems():
			# 		self._streams[stream_name] = [DataType[stream[0]],dict()]
			# 		for (timestamp,filename) in stream[1].iteritems():
			# 			_ts = tuple(map(int, timestamp[1:].split(".")))
			# 			self._streams[stream_name][1][_ts] = str(filename)

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