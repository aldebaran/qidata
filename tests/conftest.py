#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

from qidata.command_line import show_command

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
JPG_WITH_INTERNAL_ANNOTATIONS = "Annotated_JPG_file.jpg"
JPG_WITH_EXTERNAL_ANNOTATIONS = "JPG_with_external_annotations.jpg"
JPG_EXTERNAL_ANNOTATIONS = "JPG_with_external_annotations.jpg.xmp"
JPG_PHOTO = "SpringNebula.jpg"
WAV_SOUND = "Trumpet.wav"
FULL_DATASET = "Michal_Asus_2016-02-19-15-25-46"

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

@pytest.fixture(scope="session")
def show_command_parser():
	return show_command.make_command_parser()

@pytest.fixture(scope="function")
def jpg_with_internal_annotations():
	return sandboxed(JPG_WITH_INTERNAL_ANNOTATIONS)

@pytest.fixture(scope="function")
def jpg_with_external_annotations():
	sandboxed(JPG_EXTERNAL_ANNOTATIONS)
	return sandboxed(JPG_WITH_EXTERNAL_ANNOTATIONS)
