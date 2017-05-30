#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
#                            SOFTBANK  ROBOTICS
#==============================================================================
# PROJECT : QiData
# FILE : conftest.py
# DESCRIPTION :
"""
Prepare the conditions for proper unit testing
"""
#[MODULES IMPORTS]-------------------------------------------------------------
import os
import errno
import shutil
import pytest
import utilities

from qidata import QiDataSet, qidatafile
from qidata.metadata_objects import Context

#[MODULE INFO]-----------------------------------------------------------------
__author__ = "sambrose"
__date__ = "2017-04-04"
__copyright__ = "Copyright 2017, Softbank Robotics (c)"
__version__ = "0.0.1"
__maintainer__ = "sambrose"
__email__ = "sambrose@softbankrobotics.com"

#[MODULE GLOBALS]--------------------------------------------------------------

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
SANDBOX_FOLDER = "/tmp/qidata/"

DATASET   = "valid_dataset"
DATASET_ANNOTATED   = "dataset_annotated"
DATASET_WITH_DATATYPE_BINS = "dataset_annotated_with_type_bins"
DATASET_INVALID   = "invalid_dataset"
JPG_PHOTO = "SpringNebula.jpg"
QIDATA_V1 = "qidatafile_v1.png"
QIDATA_V2 = "qidatafile_v2.png"
QIDATA_V3 = "qidatafile_v3.png"


QIDATA_TEST_FILE = QIDATA_V3

#[MODULE CONTENT]--------------------------------------------------------------

def sandboxed(path):
    """
    Makes a copy of the given path in /tmp and returns its path.
    """
    source_path = os.path.join(DATA_FOLDER,    path)
    tmp_path    = os.path.join(SANDBOX_FOLDER, path)

    try:
        os.mkdir(SANDBOX_FOLDER)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if os.path.isdir(source_path):
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        shutil.copytree(source_path, tmp_path)
    else:
        shutil.copyfile(source_path, tmp_path)

    return tmp_path

@pytest.fixture(autouse=True, scope="function")
def begin(request):
    """
    Add a finalizer to clean tmp folder after each test
    """
    def fin():
        if os.path.exists(SANDBOX_FOLDER):
            shutil.rmtree(SANDBOX_FOLDER)

    request.addfinalizer(fin)

@pytest.fixture(scope="function")
def qidata_file_path():
    return sandboxed(QIDATA_TEST_FILE)

@pytest.fixture(scope="function")
def invalid_dataset_path():
    return sandboxed(DATASET_INVALID)

@pytest.fixture(scope="function",
    params=[(True, DATASET_INVALID), (False, DATASET)])
def valid_dataset_path(request):
    dataset_path = sandboxed(request.param[1])
    if request.param[0]:
        with QiDataSet(dataset_path, "w"):
            pass
    return dataset_path

@pytest.fixture(scope="function")
def dataset_with_newly_annotated_file_path(valid_dataset_path):
    with qidatafile.open(valid_dataset_path+"/JPG_file.jpg", "w") as qdf:
        annotations = qdf.metadata
        new_annot = [Context(), None]
        annotations["sambrose"]=dict()
        annotations["sambrose"]["Context"]=[new_annot]
        qdf.metadata = annotations
    return valid_dataset_path

@pytest.fixture(scope="function",
    params=[(True, DATASET_INVALID), (False, DATASET_ANNOTATED)])
def annotated_dataset_path(request):
    dataset_path = sandboxed(request.param[1])
    if request.param[0]:
        # Create annotation in file
        with qidatafile.open(dataset_path+"/JPG_file.jpg", "w") as qdf:
            annotations = qdf.metadata
            new_annot = [Context(), None]
            annotations["sambrose"]=dict()
            annotations["sambrose"]["Context"]=[new_annot]
            qdf.metadata = annotations

        # Init dataset
        with QiDataSet(dataset_path, "w") as a:
            a.examineContent()
    return dataset_path


