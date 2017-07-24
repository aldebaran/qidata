
from xmp.xmp import registerNamespace
from collections import OrderedDict
from qidata import makeMetadataObject, MetadataType

# Namespace reserved for annotation
QIDATA_NS=u"http://softbank-robotics.com/qidata/1"
registerNamespace(QIDATA_NS, "qidata")

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

def _removePrefixes(map_from_xmp):
	"""
	Removes prefix part of keys imported from XMP files.

	:param map_from_xmp: Map imported from an XMP file

	.. note::
		This function is recursive and returns nothing (in-place changes)
	"""
	if isinstance(map_from_xmp, OrderedDict):
		keys = map_from_xmp.keys()
		for key in map_from_xmp.keys():
			_removePrefixes(map_from_xmp[key])
			map_from_xmp[key.split(":")[-1]] = map_from_xmp.pop(key)
	elif isinstance(map_from_xmp, list):
		for element in map_from_xmp:
			_removePrefixes(element)

def _load_annotations(xmp_file):
	"""
	Load annotations from XMPFile into an OrderedDict with MetadataObject
	instances.

	:param xmp_file: XMP file to read from
	:type xmp_file: xmp.xmp.XMPFile
	:return: OrderedDict containing annotations
	:rtype: collections.OrderedDict
	"""
	out = OrderedDict()

	# Retrieve all metadata from the annotation namespace
	_raw_metadata = xmp_file.metadata[QIDATA_NS]

	# If there are annotations
	if _raw_metadata.children:
		# Remove all "qidata" prefixes
		data = _raw_metadata.value
		_removePrefixes(data)

		# Build the annotation structure
		for annotatorID in data.keys():
			out[annotatorID] = dict()
			for metadata_type in list(MetadataType):
				try:
					if len(data[annotatorID][str(metadata_type)]) != 0:
						out[annotatorID][str(metadata_type)] = []
					else:
						continue
				except KeyError:
					# metadata_type does not exist in file => it's ok
					continue

				for annotation in data[annotatorID][str(metadata_type)]:
					obj = makeMetadataObject(
						    metadata_type,
						    annotation["info"]
						  )
					if annotation.has_key("location"):
						loc = annotation["location"]
						if isinstance(loc, list):
							_unicodeListToBuiltInList(loc)
						else:
							loc = _unicodeToBuiltInType(loc)
						out[annotatorID][str(metadata_type)].append(
						                                       [obj, loc]
						                                     )
					else:
						out[annotatorID][str(metadata_type)].append(
							                                   [obj, None]
							                                 )
	return out

def _save_annotations(xmp_file, annotations):
	"""
	Save changes made to annotations

	:param xmp_file: XMP file to write in
	:type xmp_file: xmp.xmp.XMPFile
	:param annotations: OrderedDict containing annotations
	:type annotations: collections.OrderedDict

	.. note::

		This prepares the metadata to be written in the file, but
		it is actually saved only when the file is closed.
	"""
	# Get metadata from annotation namespace and erase it
	_raw_metadata = xmp_file.metadata[QIDATA_NS]
	for key in _raw_metadata.children:
		_raw_metadata.pop(key)

	for (annotation_maker, personal_annotations) in annotations.iteritems():
		# Make a new dict for each annotator
		_raw_metadata[annotation_maker] = dict()

		for (annotation_typename, typed_annotations) in personal_annotations.iteritems():
			# Make a new list for each annotation type
			_raw_metadata[annotation_maker][annotation_typename] = []

			for annotation in typed_annotations:
				# Store annotion details and location in a dict along with
				# the metadata object version
				tmp_dict = dict(info=annotation[0])
				if annotation[1] is not None:
					tmp_dict["location"]=annotation[1]
				_raw_metadata[annotation_maker][annotation_typename].append(tmp_dict)
				_raw_metadata[annotation_maker][annotation_typename][-1]["info"]["version"] = annotation[0].version
