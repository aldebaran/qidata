# -*- coding: utf-8 -*-

# Standard Library
import unittest
import pytest
import os
import shutil

# Qidata
from qidata import QiDataSet, DataType
from qidata.qidataset import isDataset
from qidata.exceptions import ReadOnlyException
from qidata.qidataframe import FrameIsInvalid
from qidata.metadata_objects import Face, Context, TimeStamp
import utilities

def test_wrong_path(qidata_file_path):
    """
    If path is not a folder, it cannot be opened as a QiDataSet
    """
    with pytest.raises(IOError):
        with QiDataSet(qidata_file_path, "r") as a:
            pass

    with pytest.raises(IOError):
        with QiDataSet(qidata_file_path, "w") as a:
            pass

def test_invalid_dataset_opening(invalid_dataset_path):
    """
    If path is a folder but not already a QiDataSet, it can only be opened in
    "write" mode. Once this is done, it has become a QiDataSet, and can be
    opened in "read" mode
    """
    assert(not isDataset(invalid_dataset_path))
    with pytest.raises(IOError):
        with QiDataSet(invalid_dataset_path, "r") as a:
            pass

    with QiDataSet(invalid_dataset_path, "w") as a:
        # Here it is made valid !!
        assert(a.mode == "w")
        pass

    assert(isDataset(invalid_dataset_path))
    assert(os.path.exists(os.path.join(invalid_dataset_path, "metadata.xmp")))

def test_valid_dataset_opening(valid_dataset_path):
    """
    If path is a QiDataSet, make sure it can be opened
    """
    assert(isDataset(valid_dataset_path))
    with QiDataSet(valid_dataset_path, "r") as a:
        assert(a.mode == "r")

def test_valid_dataset_properties(valid_dataset_path):
    """
    Check we can access all the basic properties of a QiDataSet
    """
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

def test_dataset_with_newly_annotated_file_properties(dataset_with_newly_annotated_file_path):
    """
    Check new annotations have not been discovered yet and that they are after
    examination
    """
    with QiDataSet(dataset_with_newly_annotated_file_path, "w") as a:
        assert(a.content.toDict()["metadata_info"] == dict())
        a.examineContent()
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)
        assert(a.content.partial_annotations == [("sambrose","Context")])

    # Check it has been written properly
    with QiDataSet(dataset_with_newly_annotated_file_path, "r") as a:
        assert(a.content.toDict()["metadata_info"]["sambrose"]["Context"] == False)

def test_annotated_dataset_properties(annotated_dataset_path):
    """
    When facing an annotated dataset, we can retrieve information on its
    contained annotations. They also can be modified
    """
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
        assert(a.getAllFilesOfType("IMAGE")==["JPG_file.jpg"])
        assert(a.getAllFilesOfType(DataType.IMAGE)==["JPG_file.jpg"])
        assert(a.getAllFilesOfType("AUDIO")==["WAV_file.wav"])
        assert(a.getAllFilesOfType(DataType.AUDIO)==["WAV_file.wav"])
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

    with QiDataSet(annotated_dataset_path, "r") as a:
        with pytest.raises(IOError):
            with a.openChild("non_existing_file.jpg", "w") as img_file:
                pass

        with  pytest.raises(IOError):
            with a.openChild("non_existing_file.jpg", "w") as img_file:
                pass

        with  pytest.raises(IOError):
            with a.openChild("non_existing_file.jpg", "w") as img_file:
                pass

def test_annotated_dataset_create_data_bins(annotated_dataset_path):
    with QiDataSet(annotated_dataset_path, "w") as a:
        with pytest.raises(TypeError):
            a.setTypeOfFile("JPG_file.jpg", "TROLOLOLOLO")

        with pytest.raises(ValueError):
            a.setTypeOfFile("non_existing_file.jpg", "IMG_3D")

        a.setTypeOfFile("JPG_file.jpg", "IMG_3D")
        assert(a.getAllFilesOfType(DataType.IMG_3D)==["JPG_file.jpg"])

        a.setTypeOfFile("JPG_file.jpg", DataType.IMG_2D)
        assert(a.getAllFilesOfType("IMG_2D")==["JPG_file.jpg"])

        assert(set(["AUDIO", "IMG_2D"]) == set(a.content.file_types))
        assert(a.getAllFilesOfType("IMAGE")==[])

    with QiDataSet(annotated_dataset_path, "r") as a:
        assert(a.getAllFilesOfType("IMG_2D")==["JPG_file.jpg"])
        assert(a.getAllFilesOfType("IMAGE")==[])
        assert(set(["AUDIO", "IMG_2D"]) == set(a.content.file_types))

def test_data_stream(dataset_with_several_images_path):
    with QiDataSet(dataset_with_several_images_path, "w") as a:
        assert(dict() == a.getAllStreams())
        assert(dict() == a.getStreamsOfType(DataType.IMG_2D))
        with pytest.raises(KeyError):
            a.getStream("toto")

        imgs_2d = a.getAllFilesOfType("IMG_2D")
        a.createNewStream(DataType.IMG_2D, "cam2d", zip([(0,0),(1,0)],imgs_2d))
        aud = a.getAllFilesOfType("AUDIO")
        a.createNewStream(DataType.AUDIO, "audio", zip([(1,500000000)],aud))

        assert(DataType.IMG_2D == a.getStreamType("cam2d"))
        assert(DataType.AUDIO == a.getStreamType("audio"))
        assert(
            {
                (0,000000000):"JPG_file.jpg",
                (1,000000000):"JPG_file2.jpg"
            } == a.getStream("cam2d")
        )
        assert(
            {
                (1,500000000):"WAV_file.wav"
            } == a.getStream("audio")
        )
        assert(
            {
                "cam2d":
                {
                    (0,000000000):"JPG_file.jpg",
                    (1,000000000):"JPG_file2.jpg"
                }
            } == a.getStreamsOfType(DataType.IMG_2D)
        )
        assert(
            {
                "audio":
                {
                    (1,500000000):"WAV_file.wav"
                }
            } == a.getStreamsOfType(DataType.AUDIO)
        )
        assert(
            {
                "cam2d":
                {
                    (0,000000000):"JPG_file.jpg",
                    (1,000000000):"JPG_file2.jpg"
                },
                "audio":
                {
                    (1,500000000):"WAV_file.wav"
                }
            } == a.getAllStreams()
        )

        a.removeFromStream("cam2d", "JPG_file2.jpg")
        assert(
            {
                "cam2d":
                {
                    (0,000000000):"JPG_file.jpg"
                }
            } == a.getStreamsOfType(DataType.IMG_2D)
        )
        assert(
            {
                "cam2d":
                {
                    (0,000000000):"JPG_file.jpg"
                },
                "audio":
                {
                    (1,500000000):"WAV_file.wav"
                }
            } == a.getAllStreams()
        )

        a.addToStream("cam2d", ((0,500000000),"JPG_file2.jpg"))
        assert(
            {
                "cam2d":
                {
                    (0,000000000):"JPG_file.jpg",
                    (0,500000000):"JPG_file2.jpg"
                },
                "audio":
                {
                    (1,500000000):"WAV_file.wav"
                }
            } == a.getAllStreams()
        )

    with QiDataSet(dataset_with_several_images_path, "r") as a:
        assert(
            {
                "cam2d":{(0,000000000):"JPG_file.jpg", (0,500000000):"JPG_file2.jpg"},
                "audio":{(1,500000000):"WAV_file.wav"}
            } == a.getAllStreams()
        )

def test_data_frame(annotated_dataset_path):
    with QiDataSet(annotated_dataset_path, "r") as a:
        assert([] == a.getAllFrames())
        with pytest.raises(ReadOnlyException):
            _f = a.createNewFrame("JPG_file.jpg", "WAV_file.wav")

    with QiDataSet(annotated_dataset_path, "w") as a:
        assert([] == a.getAllFrames())
        _f = a.createNewFrame("JPG_file.jpg", "WAV_file.wav")
        assert([_f] == a.getAllFrames())
        annotations = _f.metadata
        timestamp = [TimeStamp(1491454120,0), []]
        annotations["jdoe"]=dict()
        annotations["jdoe"]["TimeStamp"]=[timestamp]
        _f.metadata = annotations

    with QiDataSet(annotated_dataset_path, "r") as a:
        frames = a.getAllFrames()
        assert(isinstance(frames, list))
        assert(len(frames)==1)
        assert(set(["JPG_file.jpg", "WAV_file.wav"]) == frames[0].raw_data)
        assert(set(["JPG_file.jpg", "WAV_file.wav"]) == frames[0].files)
        assert(frames[0].metadata.has_key("jdoe"))
        assert(frames[0].metadata["jdoe"].has_key("TimeStamp"))
        assert(1 == len(frames[0].metadata["jdoe"]["TimeStamp"]))
        assert([] == frames[0].metadata["jdoe"]["TimeStamp"][0][1])
        assert(1491454120 == frames[0].metadata["jdoe"]["TimeStamp"][0][0].seconds)
        assert(0 == frames[0].metadata["jdoe"]["TimeStamp"][0][0].nanoseconds)
        with pytest.raises(ReadOnlyException):
            a.removeFrame(frames[0])

    with QiDataSet(annotated_dataset_path, "w") as a:
        frames = a.getAllFrames()
        a.removeFrame(frames[0])
        assert([] == a.getAllFrames())

    with QiDataSet(annotated_dataset_path, "w") as a:
        assert([] == a.getAllFrames())
        _f = a.createNewFrame("JPG_file.jpg", "WAV_file.wav")
        assert(_f == a.getFrame("JPG_file.jpg", "WAV_file.wav"))
        assert(_f == a.getFrame("WAV_file.wav", "JPG_file.jpg"))
        a.removeFrame("WAV_file.wav", "JPG_file.jpg")
        assert([] == a.getAllFrames())
        with pytest.raises(FrameIsInvalid):
            _f._open()

        with pytest.raises(FrameIsInvalid):
            _f.metadata

        with pytest.raises(FrameIsInvalid):
            _f.metadata = []

    with QiDataSet(annotated_dataset_path, "r") as a:
        assert([] == a.getAllFrames())
