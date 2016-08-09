# -*- coding: utf-8 -*-

from xmp.xmp import XMPFile, registerNamespace
from qidata.metadata_objects import makeMetadataObject, DataObjectTypes

from version import identifyFileAnnotationVersion

# ────────────────
# File versionning

QIDATA_NS=dict(
    V1=u"http://aldebaran.com/xmp/1",
    V2=u"http://aldebaran.com/xmp/1",
    V3=u"http://softbank-robotics.com/qidata/1"
    )
registerNamespace(QIDATA_NS["V1"], "aldebaran")
registerNamespace(QIDATA_NS["V3"], "qidata")

# V2 -> V3 : Namespace change
# V1 -> V2 : First children are annotators' name instead of object types

# ──────────────────
# Conversion methods

def qidataFileConversionFromV1ToV2(file_path, annotator_id):
    """
    Convert QiDataFile from V1 to V2

    @file_path    : path to the file to convert
    @annotator_id : name of annotator (mandatory from V2) (str)
    """
    if type(annotator_id) is not str:
        raise TypeError("annotator_id must be a string")
    with XMPFile(file_path, rw=True) as file:
        metadata = file.metadata[QIDATA_NS["V1"]]
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

def qidataFileConversionFromV2ToV3(file_path):
    """
    Convert QiDataFile from V2 to V3

    @file_path    : path to the file to convert
    """
    with XMPFile(file_path, rw=True) as file:
        old_metadata = file.metadata[QIDATA_NS["V2"]]
        new_metadata = file.metadata[QIDATA_NS["V3"]]
        data = old_metadata.value
        _changePrefix(data, "qidata")
        for annotator in data.keys():
            new_metadata[annotator] = data[annotator]
        for key in old_metadata.children:
            old_metadata.pop(key)

def qidataFileConversionToCurrentVersion(file_path, args=dict()):
    """
    Convert QiDataFile to the latest version

    @file_path    : path to the file to convert
    @args         : dict of all requested arguments

    Requested arguments are:
     - "annotator"      if converting from V1
    """
    version = identifyFileAnnotationVersion(file_path)
    if version is None:
        return
    if version<2:
        if not args.has_key("annotator") or args["annotator"] is None:
            raise TypeError("annotator argument is mandatory to convert a V1 qidata file")
        qidataFileConversionFromV1ToV2(file_path, args["annotator"])
    if version<3:
        qidataFileConversionFromV2ToV3(file_path)
