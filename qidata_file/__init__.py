# -*- coding: utf-8 -*-

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
