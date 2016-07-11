# -*- coding: utf-8 -*-

from xmp.xmp import XMPFile, XMPMetadata, ALDEBARAN_NS
from qidata_objects import makeDataObject, DataObjectTypes


def open(file_path, mode="r"):
    """
    Open a QiDataFile using the QiDataFile() type, returns a QiDataFile object.
    This is the preferred way to open a QiDatafile.
    """
    return QiDataFile(file_path, mode)

class QiDataFile:

    # ───────────
    # Constructor

    def __init__(self, file_path, mode = "r"):
        """
        Create and open a QiDataFile.
        QiDataFile wraps the xmp library specifically to store QiDataObjects under the
        QiData namespace.

        @file_path : path to the file to open (str)
        @mode      : opening mode, "r" for reading, "w" for writing (str)

        .. warnings:: The mode behavior is different from the regular Python file mode.
                      The file is NEVER created if it does not exist
        """

        self.xmp_file = XMPFile(file_path, rw=(mode=="w"))
        self.__annotations = None
        self.is_closed = True
        self.open()

    # ──────────
    # Properties

    @property
    def closed(self):
        """
        True if the file is closed
        """
        return self.is_closed

    @property
    def mode(self):
        """
        Specify the file mode

        "r" => read-only mode
        "w" => read/write mode
        """
        return "w" if self.xmp_file.rw else "r"

    @property
    def path(self):
        """
        Give the file path
        """
        return self.xmp_file.file_path

    @property
    def metadata(self):
        """
        Return metadata content in raw form
        """
        return self.xmp_file.metadata[ALDEBARAN_NS]

    @property
    def annotations(self):
        """
        Return metadata content in the form of a dict containing QiDataObjects or built-in types.
        """
        if self.__annotations is None:
            self.__annotations = dict()
            with self.xmp_file as tmp:
                for annotationClassName in DataObjectTypes:
                    self.__annotations[annotationClassName] = []
                    try:
                        for annotation in self.metadata[annotationClassName]:
                            obj = makeDataObject(annotationClassName, annotation.info.value)
                            loc = annotation.location.value
                            self.__unicodeListToFloatList(loc)
                            self.__annotations[annotationClassName].append([obj, loc])

                    except KeyError, e:
                        # annotationClassName does not exist in file => it's ok
                        pass

        return self.__annotations

    @property

    # ──────────
    # Public API

    def open(self):
        """
        Open the file
        """
        self.xmp_file.__enter__()
        self.is_closed = False
        return self

    def close(self):
        """
        Close the file
        """
        self.xmp_file.__exit__(None, None, None)
        self.is_closed = True

    def save_annotations(self):
        with self.xmp_file as tmp:
            for (annotationClassName, annotations) in self.__annotations.iteritems():
                self.metadata[annotationClassName] = []
                for annotation in annotations:
                    tmp_dict = dict(info=annotation[0].toDict(), location=annotation[1])
                    tmp_dict["info"]["version"] = annotation[0].version
                    self.metadata.__getattr__(annotationClassName).append(tmp_dict)

    # ───────────
    # Private API

    def __unicodeListToBuiltInList(self, list_to_convert):
        """
        Convert a list containing unicode values into a list of built-in types

        @list_to_convert : list of unicode elements to convert (can be nested)

        :Example:

        >>> __unicodeListToBuiltInList(["1"])
        [1]
        >>> __unicodeListToBuiltInList(["1.0", "1"])
        [1.0, 1]
        >>> __unicodeListToBuiltInList(["a",["1","2.0"]])
        ["a", [1, 2.0]]
        """
        if type(list_to_convert) != list:
            raise TypeError("__unicodeListToBuiltInList can only hande lists")
        for i in range(0,len(list_to_convert)):
            if type(list_to_convert[i]) == list:
                self.__unicodeListToBuiltInList(list_to_convert[i])
            elif type(list_to_convert[i]) in [unicode, str]:
                list_to_convert[i] = __unicodeToBuiltInType(list_to_convert[i])

    def __unicodeToBuiltInType(self, input_to_convert):
        """
        Convert a string into a string, a float or an int depending on the string

        @input_to_convert : unicode or string element to convert

        :Example:

        >>> __unicodeToBuiltInType("1")
        1
        >>> __unicodeToBuiltInType("1.0")
        1.0
        >>> __unicodeToBuiltInType("a")
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



    # ───────────────
    # Context Manager

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.xmp_file.__exit__(type, value, traceback)
        self.is_closed = True
