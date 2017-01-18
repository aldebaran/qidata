# -*- coding: utf-8 -*-

"""
The ``qidata.qidatafile`` module provides the ``QiDataFile`` class which is a ``QiDataObject``
wrapping the ``:mod:xmp`` package. It provides the access to a file's metadata through the
QiDataObject's interface.
"""

from xmp.xmp import XMPFile, registerNamespace
from qidata import makeMetadataObject, DataType, MetadataType
from qidata.files import getFileDataType
from qidata.qidataobject import QiDataObject
from collections import OrderedDict
import copy

QIDATA_NS=u"http://softbank-robotics.com/qidata/1"
registerNamespace(QIDATA_NS, "qidata")

def open(file_path, mode="r"):
    """
    Open a file as a QiDataFile.
    This is the preferred way to open a QiDatafile.

    :param file_path: Path to the file to open
    :param mode: Mode of opening ("r" for reading, "w" for writing)
    :return: QiDataFile object
    :Example:
        >>> from qidata import qidatafile
        >>> myFile = qidatafile.open("path/to/file")

    .. warning::

        The mode behavior is different from the regular Python file mode.
        The file is NEVER created if it does not exist. Besides, opening
        an existing file in "w" mode does not overwrite it.
    """
    return QiDataFile(file_path, mode)

class QiDataFile(QiDataObject, file):

    # ───────────
    # Constructor

    def __init__(self, file_path, mode = "r"):
        """
        Create and open a QiDataFile.
        QiDataFile wraps the xmp library specifically to store QiDataObjects under the
        QiData namespace.

        :param file_path: path to the file to open (str)
        :param mode: opening mode, "r" for reading, "w" for writing (str)

        .. warnings:: The mode behavior is different from the regular Python file mode.
                      The file is NEVER created if it does not exist. Besides, opening
                      an existing file in "w" mode does not overwrite it.
        """

        self._type = getFileDataType(file_path)
        self._file_path = file_path
        self._xmp_file = XMPFile(file_path, rw=(mode=="w"))
        self._annotations = None
        self._is_closed = True
        self._open()
        file.__init__(self, file_path, "r")

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
    def metadata(self):
        """
        Return metadata content in the form of a ``collections.OrderedDict`` containing
        metadata object instances or built-in types.
        The returned object is a copy of the real metadata, therefore modifying it has no
        impact on the file.
        """
        return copy.deepcopy(self._annotations)

    @metadata.setter
    def metadata(self, new_metadata):
        ## Check new_metadata has the correct shape
        if not isinstance(new_metadata, dict):
            raise AttributeError("Metadata must be a mapping")
        for annotator in new_metadata:
            if not isinstance(new_metadata[annotator], dict):
                msg = "Metadata from annotator {} must be a dict, not {}"
                raise AttributeError(msg.format(annotator, type(new_metadata[annotator]).__name__))
            for type_name in new_metadata[annotator]:
                try:
                    obj_type = MetadataType[type_name]
                except KeyError:
                    msg = "Type {} in {}'s metadata does not exist"
                    raise AttributeError(msg.format(type_name, annotator))

                if not isinstance(new_metadata[annotator][type_name], list):
                    msg = "List of {} metadata from annotator {} must be a list"
                    raise AttributeError(msg.format(type_name, annotator))

                for annotation in new_metadata[annotator][type_name]:
                    if not isinstance(annotation, (tuple, list)):
                        msg = "Metadata stored in {}'s metadata list must be a list or tuple, not {}"
                        raise AttributeError(msg.format(type_name, type(annotation).__name__))
                    if len(annotation) != 2:
                        msg = "Metadata of type {0} in {0}'s metadata from {1} must be of size 2"
                        raise AttributeError(msg.format(type_name, annotator))
                    if type(annotation[0]).__name__ != type_name:
                        msg = "{} metadata received instead of {} in {}'s metadata"
                        raise AttributeError(msg.format(type(annotation[0]).__name__, type_name, annotator))
                    if (annotation[1] is not None) and (not isinstance(annotation[1], list)):
                        msg = "Location of metadata of type {0} in {0}'s metadata from {1} is incorrect. "
                        msg += "Must be list or None"
                        raise AttributeError(msg.format(type_name, annotator))

        ## Make a copy of it
        tmp = copy.deepcopy(new_metadata)
        self._annotations = OrderedDict(tmp)

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

    @property
    def _raw_metadata(self):
        """
        Return metadata content in raw form
        """
        return self._xmp_file.metadata[QIDATA_NS]

    @property
    def annotators(self):
        """
        Return the list of annotators for this file
        """
        out = []
        if self._raw_metadata.children:
            for qualifiedAnnotatorID in self._raw_metadata.children.keys():
                out.append(qualifiedAnnotatorID.split(":")[1])
        return out

    # ──────────
    # Public API

    def close(self):
        """
        Closes the file after writing the metadata
        """
        self._save()
        self._xmp_file.close()
        file.close(self)
        self._is_closed = True

    def reload(self):
        """
        Reset metadata by reloading information from the file
        """
        self._load()

    # ───────────
    # Private API

    def _open(self):
        """
        Open the file
        """
        self._xmp_file.__enter__()
        self._is_closed = False
        self._load()
        return self

    def _load(self):
        """
        Load metadata from XMPFile into local `annotations` property
        """
        self._annotations = OrderedDict()
        if self._raw_metadata.children:
            data = self._raw_metadata.value
            self._removePrefix(data)
            for annotatorID in data.keys():
                self._annotations[annotatorID] = dict()
                for metadata_type in list(MetadataType):
                    self._annotations[annotatorID][str(metadata_type)] = []
                    try:
                        for annotation in data[annotatorID][str(metadata_type)]:
                            obj = makeMetadataObject(metadata_type, annotation["info"])
                            if annotation.has_key("location"):
                                loc = annotation["location"]
                                self._unicodeListToBuiltInList(loc)
                                self._annotations[annotatorID][str(metadata_type)].append([obj, loc])
                            else:
                                self._annotations[annotatorID][str(metadata_type)].append([obj, None])

                    except KeyError, e:
                        # metadata_type does not exist in file => it's ok
                        pass

    def _save(self):
        """
        Save changes made to annotations

        .. note::

            This prepares the metadata to be written in the file, but
            it is actually saved only when the file is closed.
        """
        for key in self._raw_metadata.children:
            self._raw_metadata.pop(key)
        for (annotation_maker, annotations) in self._annotations.iteritems():
            for (annotationClassName, typed_annotations) in annotations.iteritems():
                self._raw_metadata[annotation_maker] = dict()
                self._raw_metadata[annotation_maker][annotationClassName] = []
                for annotation in typed_annotations:
                    tmp_dict = dict(info=annotation[0].toDict())
                    if annotation[1] is not None:
                        tmp_dict["location"]=annotation[1]
                    tmp_dict["info"]["version"] = annotation[0].version
                    self._raw_metadata[annotation_maker].__getattr__(annotationClassName).append(tmp_dict)

    def _unicodeListToBuiltInList(self, list_to_convert):
        """
        Convert a list containing unicode values into a list of built-in types

        :param list_to_convert: list of unicode elements to convert (can be nested)

        :Example:

        >>> _unicodeListToBuiltInList(["1"])
        [1]
        >>> _unicodeListToBuiltInList(["1.0", "1"])
        [1.0, 1]
        >>> _unicodeListToBuiltInList(["a",["1","2.0"]])
        ["a", [1, 2.0]]
        """
        if type(list_to_convert) != list:
            raise TypeError("_unicodeListToBuiltInList can only hande lists")
        for i in range(0,len(list_to_convert)):
            if type(list_to_convert[i]) == list:
                self._unicodeListToBuiltInList(list_to_convert[i])
            elif type(list_to_convert[i]) in [unicode, str]:
                list_to_convert[i] = self._unicodeToBuiltInType(list_to_convert[i])

    def _unicodeToBuiltInType(self, input_to_convert):
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
        if type(input_to_convert) not in [str, unicode]:
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

    def _removePrefix(self, data):
        """
        Removes prefix parts of keys imported from XMP files.

        This function is recursive
        """
        from collections import OrderedDict
        if isinstance(data, OrderedDict):
            keys = data.keys()
            for key in data.keys():
                self._removePrefix(data[key])
                data[key.split(":")[-1]] = data.pop(key)
        elif isinstance(data, list):
            for element in data:
                self._removePrefix(element)

    # ───────────────
    # Context Manager

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

__all__=["open", "QiDataFile"]