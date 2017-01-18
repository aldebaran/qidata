# -*- coding: utf-8 -*-

from xmp.xmp import XMPFile, registerNamespace

from version import identifyFileAnnotationVersion
from distutils.version import StrictVersion

# ────────────────
# File versionning

QIDATA_NS={
    "0.1":u"http://aldebaran.com/xmp/1",
    "0.2":u"http://aldebaran.com/xmp/1",
    "1.0":u"http://softbank-robotics.com/qidata/1"
    }
registerNamespace(QIDATA_NS["0.1"], "aldebaran")
registerNamespace(QIDATA_NS["1.0"], "qidata")

# 0.2 -> 1.0 : Namespace change
# 0.1 -> 0.2 : First children are annotators' name instead of object types

# ──────────────────
# Conversion methods

def qidataFileConversionFromv01Tov02(file_path, annotator_id):
    """
    Convert QiDataFile from v0.1 to v0.2

    :param file_path: path to the file to convert
    :param annotator_id: name of annotator (mandatory from v0.1) (str)
    """
    if type(annotator_id) is not str:
        raise TypeError("annotator_id must be a string")
    with XMPFile(file_path, rw=True) as file:
        metadata = file.metadata[QIDATA_NS["0.1"]]
        if metadata.children:
            metadata[annotator_id] = metadata.value
        for child in metadata.children.keys():
            if child.split(":")[-1] != annotator_id:
                del metadata[child]

def _changePrefix(input_data, new_prefix):
    from collections import OrderedDict
    if isinstance(input_data, OrderedDict):
        keys = input_data.keys()
        for key in input_data.keys():
            _changePrefix(input_data[key], new_prefix)
            input_data[new_prefix+":"+key.split(":")[-1]] = input_data.pop(key)
    elif isinstance(input_data, list):
        for element in input_data:
            _changePrefix(element, new_prefix)

def qidataFileConversionFromv02Tov10(file_path):
    """
    Convert QiDataFile from v0.2 to v1.0

    :param file_path: path to the file to convert
    """
    with XMPFile(file_path, rw=True) as file:
        old_metadata = file.metadata[QIDATA_NS["0.2"]]
        new_metadata = file.metadata[QIDATA_NS["1.0"]]
        data = old_metadata.value
        _changePrefix(data, "qidata")
        for annotator in data.keys():
            new_metadata[annotator] = data[annotator]
        for key in old_metadata.children:
            old_metadata.pop(key)

def qidataFileConversionToCurrentVersion(file_path, args=dict()):
    """
    Convert QiDataFile to the latest version

    :param file_path: path to the file to convert
    :param args: dict of all requested arguments

    .. note::
        Requested arguments are:

        - "annotator"      if converting from v0.1
    """
    version = identifyFileAnnotationVersion(file_path)
    if version is None:
        return
    version = StrictVersion(version)
    if version<StrictVersion("0.2"):
        if not args.has_key("annotator") or args["annotator"] is None:
            raise TypeError("annotator argument is mandatory to convert a v0.1 qidata file")
        qidataFileConversionFromv01Tov02(file_path, args["annotator"])
    if version<StrictVersion("1.0"):
        qidataFileConversionFromv02Tov10(file_path)
