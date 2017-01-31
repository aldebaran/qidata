# -*- coding: utf-8 -*-

# Standard Library
import errno
import os
import shutil
# libXMP
import libxmp.consts

# ──────────
# Parameters

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
SANDBOX_FOLDER = "/tmp/qidata/"

# ───────────
# Groundtruth

DATASET   = "dataset"
DATASET_ANNOTATED   = "dataset_annotated"
DATASET_WITH_NEW_ANNOTATIONS   = "dataset_with_new_annotations"
DATASET_INVALID   = "invalid_dataset"
JPG_PHOTO = "SpringNebula.jpg"
QIDATA_V1 = "qidatafile_v1.png"
QIDATA_V2 = "qidatafile_v2.png"
QIDATA_V3 = "qidatafile_v3.png"


QIDATA_TEST_FILE = QIDATA_V3

# ─────────
# Utilities

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

def verifyAnnotations(qidata_file, annotator):
	from qidata.metadata_objects import Person
	annotations = qidata_file.metadata
	assert(annotations.has_key(annotator))
	assert(annotations[annotator].has_key("Person"))
	assert(len(annotations[annotator]["Person"][0])==2)
	assert(isinstance(annotations[annotator]["Person"][0][0], Person))
	person = annotations[annotator]["Person"][0][0]
	location = annotations[annotator]["Person"][0][1]
	assert(person.name == "yfukuda")
	assert(location == [[4.0, 25.0],[154.0, 235.0]])

def sha1(file_path):
	import hashlib
	hasher = hashlib.sha1()
	with open(file_path,'rb') as file:
		file_data = file.read()
	hasher.update(file_data)
	return hasher.hexdigest()

def cleanData():
	if os.path.exists(SANDBOX_FOLDER):
		shutil.rmtree(SANDBOX_FOLDER)