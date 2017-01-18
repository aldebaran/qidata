# -*- coding: utf-8 -*-

import os.path
import re
from qidata import DataType

# ──────────
# Data Items

LOOKUP_ITEM_MODEL = {
    re.compile(".*\.png"): DataType.IMAGE,
    re.compile(".*\.jpg"): DataType.IMAGE,
    re.compile(".*\.wav"): DataType.AUDIO
}

def isSupported(dataPath):
    """
    Return True if file extension can be opened as QiDataFile
    """
    for pattern in LOOKUP_ITEM_MODEL:
        if pattern.match(dataPath):
            return True
    return False

def getFileDataType(path):
    """
    Return type of data stored in given file
    """
    for pattern in LOOKUP_ITEM_MODEL:
        if pattern.match(path):
            return LOOKUP_ITEM_MODEL[pattern]
    raise TypeError("Data type not supported")

# ────────
# Datasets

METADATA_FILENAME = "metadata.yaml" # Place-holder

def isDataset(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, METADATA_FILENAME))

def isMetadataFile(path):
    return  os.path.isfile(path) and os.path.basename(path) == METADATA_FILENAME

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
