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

# from qidata import QiDataSet, qidatafile
# from qidata.metadata_objects import Context

#[MODULE INFO]-----------------------------------------------------------------
__author__ = "sambrose"
__date__ = "2017-04-04"
__copyright__ = "Copyright 2017, Softbank Robotics (c)"
__version__ = "1.0.0"
__maintainer__ = "sambrose"
__email__ = "sambrose@softbankrobotics.com"

#[MODULE GLOBALS]--------------------------------------------------------------

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
SANDBOX_FOLDER = "/tmp/qidata/"

NON_EMPTY_FOLDER   = "A_folder_with_files" # Folder with files but not a dataset
DATASET   = "B_created_dataset" # QiDataSet with files added after creation
DATASET_WITH_NEW_ANNOTATIONS = "C0_annotated_file_added" # B + newly annotated file
FOLDER_WITH_ANNOTATIONS = "C1_folder_with_one_annotated_file" # A + annotated file
JPG_PHOTO = "SpringNebula.jpg"
WAV_SOUND = "Trumpet.wav"
FULL_DATASET = "Michal_Asus_2016-02-19-15-25-46"
ROSBAG_ASUS = "Michal_Asus_2016-02-19-15-25-46.bag"

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
def jpg_file_path():
	return sandboxed(JPG_PHOTO)

@pytest.fixture(scope="function")
def folder_with_non_annotated_files():
	return sandboxed(NON_EMPTY_FOLDER)

@pytest.fixture(scope="function")
def dataset_with_non_annotated_files():
	return sandboxed(DATASET)

@pytest.fixture(scope="function")
def dataset_with_new_annotations():
	return sandboxed(DATASET_WITH_NEW_ANNOTATIONS)

@pytest.fixture(scope="function")
def folder_with_annotations():
	return sandboxed(FOLDER_WITH_ANNOTATIONS)

@pytest.fixture(scope="function")
def full_dataset():
	return sandboxed(FULL_DATASET)
