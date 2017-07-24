# -*- coding: utf-8 -*-

# Standard Library
import os
import pytest

# Local modules
from qidata import QiDataSet, isDataset, DataType
from qidata.qidataimagefile import QiDataImageFile

def test_wrong_path(jpg_file_path):
	"""
	If path is not a folder, it cannot be opened as a QiDataSet
	"""
	with pytest.raises(IOError):
		with QiDataSet(jpg_file_path, "r") as a:
			pass

	with pytest.raises(IOError):
		with QiDataSet(jpg_file_path, "w") as a:
			pass

def test_dataset_creation(folder_with_non_annotated_files):
	with pytest.raises(IOError):
		with QiDataSet(folder_with_non_annotated_files, "r") as a:
			pass

	with QiDataSet(folder_with_non_annotated_files, "w") as a:
		assert(
			["JPG_file.jpg", "WAV_file.wav"] == a.children
		)

	assert(isDataset(folder_with_non_annotated_files))
	assert(os.path.exists(
		      os.path.join(folder_with_non_annotated_files, "metadata.xmp"))
	       )

def test_child_opening(dataset_with_non_annotated_files):
	with QiDataSet(dataset_with_non_annotated_files, "r") as d:
		with d.openChild("JPG_file.jpg") as f:
			assert(not f.closed)
			assert(isinstance(f, QiDataImageFile))
			assert(f.mode == "r")

	with QiDataSet(dataset_with_non_annotated_files, "w") as d:
		with d.openChild("JPG_file.jpg") as f:
			assert(not f.closed)
			assert(f.mode == "w")

def test_content(folder_with_annotations):
	with QiDataSet(folder_with_annotations, "w") as d:
		assert(set(["sambrose"]) == d.annotators)
		assert(
		    {
		        ("sambrose", "Property"): QiDataSet.AnnotationStatus.PARTIAL
		    } == d.annotations_available
		)
		assert(set([DataType.AUDIO, DataType.IMAGE]) == d.datatypes_available)

def test_content_reexamination(dataset_with_new_annotations):
	with QiDataSet(dataset_with_new_annotations, "w") as d:
		assert(set([]) == d.annotators)
		assert(dict()  == d.annotations_available)
		assert(set([]) == d.datatypes_available)
		d.examineContent()
		assert(set(["sambrose"]) == d.annotators)
		assert(
		    {
		        ("sambrose", "Property"): QiDataSet.AnnotationStatus.PARTIAL
		    } == d.annotations_available
		)
		assert(set([DataType.AUDIO, DataType.IMAGE]) == d.datatypes_available)

	with QiDataSet(dataset_with_new_annotations, "r") as d:
		assert(set(["sambrose"]) == d.annotators)
		assert(
		    {
		        ("sambrose", "Property"): QiDataSet.AnnotationStatus.PARTIAL
		    } == d.annotations_available
		)
		assert(set([DataType.AUDIO, DataType.IMAGE]) == d.datatypes_available)

def test_annotation_status(folder_with_annotations):
	with QiDataSet(folder_with_annotations, "w") as d:
		assert(
		    {
		        ("sambrose", "Property"): QiDataSet.AnnotationStatus.PARTIAL
		    } == d.annotations_available
		)
		d.setAnnotationStatus("sambrose", "Property", True)
		assert(
		    {
		        ("sambrose", "Property"): QiDataSet.AnnotationStatus.TOTAL
		    } == d.annotations_available
		)

	with QiDataSet(folder_with_annotations, "r") as d:
		assert(
		    {
		        ("sambrose", "Property"): QiDataSet.AnnotationStatus.TOTAL
		    } == d.annotations_available
		)

def test_dataset_filter(folder_with_annotations,
                        dataset_with_new_annotations,
                        dataset_with_non_annotated_files):
	with QiDataSet(folder_with_annotations, "w"):
		pass
	dataset_lists = [folder_with_annotations,
	                 dataset_with_new_annotations,
	                 dataset_with_non_annotated_files]

	assert([] == QiDataSet.filter(dataset_lists,
	                              only_annotated_by=["sambrose"],
	                              only_with_annotations=["Property"],
	                              only_total_annotations=True
	                             )
	)
	assert([] == QiDataSet.filter(dataset_lists,
	                              only_annotated_by=[],
	                              only_with_annotations=["Property"]
	                             )
	)

	assert([] == QiDataSet.filter(dataset_lists,
	                              only_with_annotations=[]
	                             )
	)

	assert(
	[folder_with_annotations] == QiDataSet.filter(dataset_lists,
	                              only_with_annotations=["Property"]
	                             )
	)
	assert(
	[folder_with_annotations] == QiDataSet.filter(dataset_lists,
	                              only_annotated_by=["sambrose", "jdoe"]
	                             )
	)

	with QiDataSet(dataset_with_new_annotations, "w") as d:
		d.examineContent()
		d.setAnnotationStatus("sambrose", "Property", True)

	assert(
	[
	  folder_with_annotations,
	  dataset_with_new_annotations
	] == QiDataSet.filter(dataset_lists,
	                      only_annotated_by=["sambrose"]
	                     )
	)
	assert(
	[
	  dataset_with_new_annotations
	] == QiDataSet.filter(dataset_lists,
	                      only_total_annotations=True
	                     )
	)