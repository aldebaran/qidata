
from xmp.xmp import registerNamespace
from collections import OrderedDict
from qidata import makeMetadataObject, MetadataType

QIDATA_NS=u"http://softbank-robotics.com/qidata/1"
registerNamespace(QIDATA_NS, "qidata")

class XMPHandlerMixin:

	@classmethod
	def _load(self, xmp_file):
		"""
		Load metadata from XMPFile into an OrderedDict with Metadata
		objects instances.

		:param xmp_file: XMP file to read
		:return: OrderedDict containing annotations
		"""
		res = OrderedDict()
		_raw_metadata = xmp_file.metadata[QIDATA_NS]
		if _raw_metadata.children:
			data = _raw_metadata.value
			XMPHandlerMixin._removePrefix(data)
			for annotatorID in data.keys():
				res[annotatorID] = dict()
				for metadata_type in list(MetadataType):
					try:
						if len(data[annotatorID][str(metadata_type)]) != 0:
							res[annotatorID][str(metadata_type)] = []
						else:
							continue
						for annotation in data[annotatorID][str(metadata_type)]:
							obj = makeMetadataObject(metadata_type, annotation["info"])
							if annotation.has_key("location"):
								loc = annotation["location"]
								self._unicodeListToBuiltInList(loc)
								res[annotatorID][str(metadata_type)].append([obj, loc])
							else:
								res[annotatorID][str(metadata_type)].append([obj, None])

					except KeyError, e:
						# metadata_type does not exist in file => it's ok
						pass
		return res

	@classmethod
	def _save(self, xmp_file, metadata):
		"""
		Save changes made to annotations

		.. note::

			This prepares the metadata to be written in the file, but
			it is actually saved only when the file is closed.
		"""
		_raw_metadata = xmp_file.metadata[QIDATA_NS]
		for key in _raw_metadata.children:
			_raw_metadata.pop(key)
		for (annotation_maker, annotations) in metadata.iteritems():
			if annotations == dict():
				continue
			_raw_metadata[annotation_maker] = dict()
			for (annotationClassName, typed_annotations) in annotations.iteritems():
				if typed_annotations == []:
					continue
				_raw_metadata[annotation_maker][annotationClassName] = []
				for annotation in typed_annotations:
					tmp_dict = dict(info=annotation[0])
					if annotation[1] is not None:
						tmp_dict["location"]=annotation[1]
					_raw_metadata[annotation_maker][annotationClassName].append(tmp_dict)
					_raw_metadata[annotation_maker][annotationClassName][-1]["info"]["version"] = annotation[0].version

			if not _raw_metadata[annotation_maker].children:
				_raw_metadata.pop(annotation_maker)


	@staticmethod
	def _unicodeListToBuiltInList(list_to_convert):
		"""
		Convert a list containing unicode values into a list of built-in types.
		The conversion is in-place.

		:param list_to_convert: list of unicode elements to convert (can be nested)

		:Example:

			>>> data = ["1"]
			>>> _unicodeListToBuiltInList(data)
			>>> data
			[1]
			>>> data = ["1.0", "1"]
			>>> _unicodeListToBuiltInList(data)
			>>> data
			[1.0, 1]
			>>> data = ["a",["1","2.0"]]
			>>> _unicodeListToBuiltInList(data)
			>>> data
			["a", [1, 2.0]]
		"""
		if not isinstance(list_to_convert, list):
			raise TypeError("_unicodeListToBuiltInList can only handle lists")
		for i in range(0,len(list_to_convert)):
			if isinstance(list_to_convert[i], list):
				XMPHandlerMixin._unicodeListToBuiltInList(list_to_convert[i])
			elif isinstance(list_to_convert[i], basestring):
				list_to_convert[i] = XMPHandlerMixin._unicodeToBuiltInType(list_to_convert[i])

	@staticmethod
	def _unicodeToBuiltInType(input_to_convert):
		"""
		Convert a string into a string, a float or an int depending on the string

		:param input_to_convert: unicode or string element to convert

		:Example:

			>>> _unicodeToBuiltInType("1")
			1
			>>> _unicodeToBuiltInType("1.0")
			1.0
			>>> _unicodeToBuiltInType("a")
			'a'
		"""
		if not isinstance(input_to_convert, basestring):
			raise TypeError("Only unicode or string can be converted")

		try:
			output=int(input_to_convert)
			return output
		except ValueError, e:
			# input cannot be converted to int
			pass
		try:
			output=float(input_to_convert)
			return output
		except ValueError, e:
			# input cannot be converted to float
			pass

		# Input could not be converted so it's probably a string, return it as is.
		return input_to_convert

	@staticmethod
	def _removePrefix(data):
		"""
		Removes prefix parts of keys imported from XMP files.

		This function is recursive and returns nothing (in-place changes)
		"""
		from collections import OrderedDict
		if isinstance(data, OrderedDict):
			keys = data.keys()
			for key in data.keys():
				XMPHandlerMixin._removePrefix(data[key])
				data[key.split(":")[-1]] = data.pop(key)
		elif isinstance(data, list):
			for element in data:
				XMPHandlerMixin._removePrefix(element)
