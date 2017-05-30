# -*- coding: utf-8 -*-

# Standard Library
import unittest
import pytest
import os
import shutil

# Qidata
from qidata import QiDataSet, DataType
from qidata.metadata_objects import Face, Context
import utilities

def test_wrong_path(qidata_file_path):
    with pytest.raises(IOError):
        with QiDataSet(qidata_file_path, "r") as a:
            pass

    with pytest.raises(IOError):
        with QiDataSet(qidata_file_path, "w") as a:
            pass

def test_invalid_dataset_opening(invalid_dataset_path):
    with pytest.raises(IOError):
        with QiDataSet(invalid_dataset_path, "r") as a:
            pass

    with QiDataSet(invalid_dataset_path, "w") as a:
        # Here it is made valid !!
        assert(a.mode == "w")
        pass

    assert(os.path.exists(os.path.join(invalid_dataset_path, "metadata.xmp")))

def test_valid_dataset_opening(valid_dataset_path):
    with QiDataSet(valid_dataset_path, "r") as a:
        assert(a.mode == "r")

def test_dataset_properties(valid_dataset_path):
    with QiDataSet(valid_dataset_path, "r") as a:
        assert(a.children == ["JPG_file.jpg", "WAV_file.wav"])
        assert(a.raw_data == (["JPG_file.jpg", "WAV_file.wav"], a.content))
        assert(a.type == DataType.DATASET)
        assert(not a.closed)
        assert(a.mode == "r")
        c = a.content
        assert(c.annotators == [])
        assert(c.annotation_types == [])
        assert(set(c.file_types) == set(["IMAGE", "AUDIO"]))
        assert(c.partial_annotations == [])
    assert(a.closed)

def test_dataset_with_new_annotations_path_properties(dataset_with_newly_annotated_file_path):
    # Check new annotations have not been discovered yet
    # And that they are after examination
    with QiDataSet(dataset_with_newly_annotated_file_path, "w") as a:
        assert(a.content.toDict()["metadata_info"] == dict())
        a.examineContent()
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)
        assert(a.content.partial_annotations == [("sambrose","Context")])
        assert(1 == a.content._type_content["AUDIO"])
        assert(1 == a.content._type_content["IMAGE"])

    # Check it has been written properly
    with QiDataSet(dataset_with_newly_annotated_file_path, "r") as a:
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)

def test_annotated_dataset_properties(annotated_dataset_path):
    # Check data set content info are correct
    with QiDataSet(annotated_dataset_path, "r") as a:
        assert(a.children == ["JPG_file.jpg", "WAV_file.wav"])
        assert(a.raw_data == (["JPG_file.jpg", "WAV_file.wav"], a.content))
        assert(a.type == DataType.DATASET)
        assert(not a.closed)
        assert(a.mode == "r")
        c = a.content
        assert(c.annotators == [])
        assert(c.annotation_types == [])
        assert(set(c.file_types) == set(["IMAGE", "AUDIO"]))
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)
    assert(a.closed)
    # Mark the annotation as total (and check the content is changed)
    with QiDataSet(annotated_dataset_path, "w") as a:
        c = a.content
        c.setMetadataTotalityStatus("sambrose", "Context", True)
        assert(c.annotators == ["sambrose"])
        assert(c.annotation_types == ["Context"])
        assert(a.content.partial_annotations == [])
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == True)

    # Check the changes were properly written
    with QiDataSet(annotated_dataset_path, "r") as a:
        c = a.content
        assert(c.annotators == ["sambrose"])
        assert(c.annotation_types == ["Context"])
        assert(a.content.partial_annotations == [])
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == True)

    with QiDataSet(annotated_dataset_path, "w") as a:
        # Add new annotations in one of the file
        new_face = Face()
        new_ctxt = Context()
        with a.openChild("JPG_file.jpg", "w") as img_file:
            metadata = img_file.metadata
            metadata["sambrose"] = dict()
            metadata["sambrose"]["Context"]=list()
            metadata["sambrose"]["Face"]=list()
            metadata["sambrose"]["Context"].append((new_ctxt, None))
            metadata["sambrose"]["Face"].append((new_face, None))
            metadata["jdoe"] = dict()
            metadata["jdoe"]["Context"]=list()
            metadata["jdoe"]["Context"].append((new_ctxt, None))
            img_file.metadata = metadata

        # Refresh the content information
        a.examineContent()
        c = a.content.toDict()
        # Check Context status did not change although a new annotation was added
        assert(c["metadata_info"]["sambrose"]["Context"] == True)
        # Check Face exists but is declared as uncomplete
        assert(c["metadata_info"]["sambrose"]["Face"] == False)
        # Check a new annotator was added as uncomplete
        assert(c["metadata_info"]["jdoe"]["Context"] == False)

    # Get content information just from path
    c = QiDataSet.contentFromPath(annotated_dataset_path).toDict()
    assert(c["metadata_info"]["sambrose"]["Context"] == True)
    assert(c["metadata_info"]["jdoe"]["Context"] == False)
    assert(c["metadata_info"]["sambrose"]["Face"] == False)

def test_child_opening():
    dataset_annotated_path = utilities.sandboxed(utilities.DATASET_ANNOTATED)
    with QiDataSet(dataset_annotated_path, "r") as a:
        with pytest.raises(IOError):
            with a.openChild("non_existing_file.jpg", "w") as img_file:
                pass

        with  pytest.raises(IOError):
            with a.openChild("non_existing_file.jpg", "w") as img_file:
                pass

        with  pytest.raises(IOError):
            with a.openChild("non_existing_file.jpg", "w") as img_file:
                pass
