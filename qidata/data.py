# -*- coding: utf-8 -*-

# Standard Library
import os.path
import re
# qidata
from qidata.models import *


# ────────
# Datasets

METADATA_FILENAME = "metadata.yaml" # Place-holder

def isDataset(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, METADATA_FILENAME))

def isMetadataFile(path):
    return  os.path.isfile(path) and os.path.basename(path) == METADATA_FILENAME

# ──────────
# Data Items

LOOKUP_ITEM_MODEL = {
    re.compile(".*\.png"): image.Image,
    re.compile(".*\.jpg"): image.Image
}

def isSupportedItem(path):
    for pattern in LOOKUP_ITEM_MODEL:
        if pattern.match(path):
            return True
    return False

def makeDataItem(path):
    for pattern in LOOKUP_ITEM_MODEL:
        if pattern.match(path):
            return LOOKUP_ITEM_MODEL[pattern](path)
    raise TypeError("Item not supported")
