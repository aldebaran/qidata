# -*- coding: utf-8 -*-

"""
    ``QiDataFile`` module
    =====================

    This module wraps xmp package and uses it to store QiDataObjects in a file
    metadata.

    Reading a QiDataFile
    --------------------

    Importing `XMPFile` is enough to fulfill almost all of use cases.

    :Example:

    >>> from qidata_file import qidatafile
    >>> myFile = qidatafile.open("path/to/file")


    Metadata is then accessible through two different properties, `metadata` and
    `annotations`. `metadata` gives access to the raw data. `annotations`
    transforms the metadata into QiDataObjects instances before returning it.

    :Example:

    >>> myFile.metadata
    <xmp.xmp.XMPNamespace object at 0x7fb8df4a1310>
    >>> myFile.metadata.children
    OrderedDict([(u'qidata:sambrose', <xmp.xmp.XMPStructure object at\
     0x7fb8df4a1390>)])
    >>> myFile.annotations
    OrderedDict([(u'sambrose', {'Person': [[<qidata_objects.person.Person\
     object at 0x7fb8df4a1d90>, [[4.0, 25.0], [154.0, 235.0]]]], 'Face': []})])


    It is also possible to get the list of annotators

    :Example:

    >>> myFile.annotators
    [u'sambrose']


    Don't forget to close the file when finished. You can also use the `with`
    statement.

    :Example:

    >>> myFile = qidatafile.open("path/to/file")
    >>> myFile.annotations
    OrderedDict([(u'sambrose', {'Person': [[<qidata_objects.person.Person\
     object at 0x7fb8df4a1d90>, [[4.0, 25.0], [154.0, 235.0]]]], 'Face': []})])
    >>> myFile.close()
    >>> myFile.closed
    True

    >>> with qidatafile.open("path/to/file") as myFile:
    ...     myFile.annotations
    ...
    OrderedDict([(u'sambrose', {'Person': [[<qidata_objects.person.Person\
     object at 0x7fb8df4a1d90>, [[4.0, 25.0], [154.0, 235.0]]]], 'Face': []})])

    >>> myFile.closed
    True


    Updating a QiDataFile
    ---------------------

    To update, you must open the file in rw mode. Retrieve the annotations
    property and modify it the way you want. Then call `save_annotations` to
    convert QiDataObjects into XMP objects and close the file.

    ..note::

    All your changes are written only when the file is closed.


    The only restrictions are:
    * annotations is a dict with keys representing contained QiDataObject type
    * Values of this dict must be 2-uple.
    * First element of it is the QiDataObject
    * Second element of if is a list describing QiDataObject's location (which
        is dependent on file type)

    Failure to respect those guidelines might lead to unability to write the
    annotations, or unability to read it properly afterwards.

    :Example:

    >>> from qidata_file import qidatafile
    >>> from qidata_objects import Person
    >>> myFile = qidatafile.open("path/to/file", "w")
    >>> annotations = myFile.annotations
    >>> myObject = Person()
    >>> if not annotations.has_key("jdoe"):
    ...     annotations["jdoe"] = dict()
    >>> if annotations["jdoe"].has_key("Person"):
    ...     annotations["jdoe"]["Person"].append((myObject, [0,0]))
    ... else:
    ...     annotations["jdoe"]["Person"] = [(myObject, [0,0])]
    ... 
    >>> myFile.save()
    >>> myFile.close()


    Upgrading a QiDataFile
    ----------------------

    It is sometimes possible that the way data is stored in QiDataFile will
    change. If this happens, QiDataFiles created the old way might not be
    readable anymore. To avoid loosing all data, it is always possible to
    convert old QiDataFiles to the newest version.

    :Example:

    >>> from qidata_file.conversion import qidataFileConversionToCurrentVersion
    >>> qidataFileConversionToCurrentVersion("file/to/convert/path")

    Depending on your file version, some extra arguments might be needed. See
    command line help to know which arguments to use.

    :Example:

    >>> qidataFileConversionToCurrentVersion("file/to/convert/path",\
     dict(annotator="jdoe")) # Call to transform a file from version 1.
"""

from image import Image
import os.path
import re

# ──────────
# Data Items

LOOKUP_ITEM_MODEL = {
    re.compile(".*\.png"): Image,
    re.compile(".*\.jpg"): Image
}

def isSupported(dataPath):
    for pattern in LOOKUP_ITEM_MODEL:
        if pattern.match(dataPath):
            return True
    return False

def openQiDataFile(path):
    for pattern in LOOKUP_ITEM_MODEL:
        if pattern.match(path):
            return LOOKUP_ITEM_MODEL[pattern](path)
    raise TypeError("Data type not supported")

# ────────
# Datasets

METADATA_FILENAME = "metadata.yaml" # Place-holder

def isDataset(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, METADATA_FILENAME))

def isMetadataFile(path):
    return  os.path.isfile(path) and os.path.basename(path) == METADATA_FILENAME

# ––––––––––––––––––––––––––––
# Convenience version variable

import os
VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")).read().split()[0]

# ––––––––––––––––––––
# Hook for qiq plugins

QIQ_PLUGIN_PACKAGES = ["qiq"]

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
