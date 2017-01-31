# -*- coding: utf-8 -*-

# Standard Library
import unittest
import os
import shutil

# Qidata
from qidata import QiDataSet, DataType
from qidata.metadata_objects import Face, Context
import fixtures

class Dataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.not_a_folder_path = fixtures.sandboxed(fixtures.QIDATA_TEST_FILE)
        cls.invalid_dataset_path = fixtures.sandboxed(fixtures.DATASET_INVALID)
        cls.dataset_path = fixtures.sandboxed(fixtures.DATASET)
        cls.dataset_annotated_path = fixtures.sandboxed(fixtures.DATASET_ANNOTATED)
        cls.dataset_with_new_annotations_path = fixtures.sandboxed(fixtures.DATASET_WITH_NEW_ANNOTATIONS)

    def test_wrong_path(self):
        with self.assertRaises(IOError):
            with QiDataSet(self.not_a_folder_path, "r") as a:
                pass

    def test_invalid_dataset_opening(self):
        with self.assertRaises(IOError):
            with QiDataSet(self.invalid_dataset_path, "r") as a:
                pass

        with QiDataSet(self.invalid_dataset_path, "w") as a:
            assert(a.mode == "w")
            pass

        assert(os.path.exists(os.path.join(self.invalid_dataset_path, "metadata.xmp")))

    def test_valid_dataset_opening(self):
        with QiDataSet(self.dataset_path, "r") as a:
            assert(a.mode == "r")

    def test_dataset_properties(self):
        with QiDataSet(self.dataset_path, "r") as a:
            assert(a.raw_data == ["JPG_file.jpg", "WAV_file.wav"])
            assert(a.type == DataType.DATASET)
            assert(not a.closed)
            assert(a.mode == "r")
            c = a.content
            assert(c.annotators == [])
            assert(c.annotation_types == [])
            assert(set(c.file_types) == set(["IMAGE", "AUDIO"]))
            assert(c.partial_annotations == [])
        assert(a.closed)

    def test_dataset_with_new_annotations_path_properties(self):
        # Check new annotations have not been discovered yet
        # Check that they are after examination
        with QiDataSet(self.dataset_with_new_annotations_path, "w") as a:
            assert(a.content.toDict()["metadata_info"] == dict())
            a.examineContent()
            assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)
            assert(a.content.partial_annotations == [("sambrose","Context")])

        # Check it has been written properly
        with QiDataSet(self.dataset_with_new_annotations_path, "r") as a:
            assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)

    def test_annotated_dataset_properties(self):
        # Check data set content info are correct
        with QiDataSet(self.dataset_annotated_path, "r") as a:
            assert(a.raw_data == ["JPG_file.jpg", "WAV_file.wav"])
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
        with QiDataSet(self.dataset_annotated_path, "w") as a:
            c = a.content
            c.setMetadataAsTotal("sambrose", "Context")
            assert(c.annotators == ["sambrose"])
            assert(c.annotation_types == ["Context"])
            assert(a.content.partial_annotations == [])
            assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == True)

        # Check the changes were properly written
        with QiDataSet(self.dataset_annotated_path, "r") as a:
            c = a.content
            assert(c.annotators == ["sambrose"])
            assert(c.annotation_types == ["Context"])
            assert(a.content.partial_annotations == [])
            assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == True)

        with QiDataSet(self.dataset_annotated_path, "w") as a:
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
        c = QiDataSet.contentFromPath(self.dataset_annotated_path).toDict()
        assert(c["metadata_info"]["sambrose"]["Context"] == True)
        assert(c["metadata_info"]["jdoe"]["Context"] == False)
        assert(c["metadata_info"]["sambrose"]["Face"] == False)

    def test_child_opening(self):
         with QiDataSet(self.dataset_annotated_path, "r") as a:
            with self.assertRaises(IOError):
                with a.openChild("non_existing_file.jpg", "w") as img_file:
                    pass

            with self.assertRaises(IOError):
                with a.openChild("non_existing_file.jpg", "w") as img_file:
                    pass

            with self.assertRaises(IOError):
                with a.openChild("non_existing_file.jpg", "w") as img_file:
                    pass