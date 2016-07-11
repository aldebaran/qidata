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

JPG_PHOTO = "SpringNebula.jpg"
QIDATA_V1 = "qidatafile_v1.png"


QIDATA_TEST_FILE = QIDATA_V1

# ─────────
# Utilities

def sandboxed(file_path):
	"""
	Makes a copy of the given file in /tmp and returns its path.
	"""
	source_path = os.path.join(DATA_FOLDER,    file_path)
	tmp_path    = os.path.join(SANDBOX_FOLDER, file_path)

	try:
		os.mkdir(SANDBOX_FOLDER)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	shutil.copyfile(source_path, tmp_path)

	return tmp_path

def verifyAnnotations(qidata_file, annotator):
	from qidata_objects import Person
	annotations = qidata_file.annotations
	assert(annotations.has_key(annotator))
	assert(annotations[annotator].has_key("Person"))
	assert(len(annotations[annotator]["Person"][0])==2)
	assert(isinstance(annotations[annotator]["Person"][0][0], Person))
	person = annotations[annotator]["Person"][0][0]
	location = annotations[annotator]["Person"][0][1]
	assert(person.id == 0)
	assert(person.name == "yfukuda")
	assert(location == [[4.0, 25.0],[154.0, 235.0]])
