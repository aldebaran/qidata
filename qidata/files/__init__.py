# -*- coding: utf-8 -*-

import os.path
import re
from qidata import DataType


# ────────
# Datasets

METADATA_FILENAME = "metadata.yaml" # Place-holder

def isDataset(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, METADATA_FILENAME))

def isMetadataFile(path):
    return  os.path.isfile(path) and os.path.basename(path) == METADATA_FILENAME

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
