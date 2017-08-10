# -*- coding: utf-8 -*-

# Standard Library
import os
import pytest

# Local modules
from qidata import QiDataSet, isDataset, DataType
from qidata.qidataframe import FrameIsInvalid
from qidata.qidatafile import ClosedFileException
from qidata.qidataobject import ReadOnlyException
from qidata.qidataimagefile import QiDataImageFile
from qidata.metadata_objects import Property, Context

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

def test_data_type_change_impact(folder_with_non_annotated_files):
	with QiDataSet(folder_with_non_annotated_files, "w") as d:
		assert(set([DataType.AUDIO, DataType.IMAGE]) == d.datatypes_available)
		with d.openChild("JPG_file.jpg") as f:
			f.type = DataType.IMAGE_2D
		d.examineContent()
		assert(set([DataType.AUDIO, DataType.IMAGE_2D]) == d.datatypes_available)

	with QiDataSet(folder_with_non_annotated_files, "r") as d:
		assert(set([DataType.AUDIO, DataType.IMAGE_2D]) == d.datatypes_available)

def test_get_file_list_of_specific_type(folder_with_annotations):
	with QiDataSet(folder_with_annotations,"w") as d:
		assert(
		    [
		      "Annotated_JPG_file.jpg",
		      "JPG_file.jpg",
		    ] == d.getAllFilesOfType(DataType.IMAGE)
		)
	with QiDataSet(folder_with_annotations,"r") as d:
		assert(
		    [
		      "Annotated_JPG_file.jpg",
		      "JPG_file.jpg",
		    ] == d.getAllFilesOfType(DataType.IMAGE)
		)
	with QiDataSet(folder_with_annotations, "w") as d:
		assert(
		    [] == d.getAllFilesOfType("IMAGE_2D")
		)
		with d.openChild("JPG_file.jpg") as f:
			f.type = DataType.IMAGE_2D
		d.examineContent()
		assert(
		    [
		      "Annotated_JPG_file.jpg",
		    ] == d.getAllFilesOfType(DataType.IMAGE)
		)
		assert(
		    [
		      "JPG_file.jpg",
		    ] == d.getAllFilesOfType("IMAGE_2D")
		)
		with pytest.raises(TypeError):
			d.getAllFilesOfType("Blablabla")

def test_data_stream(folder_with_annotations):
	with QiDataSet(folder_with_annotations, "w") as d:
		assert(dict() == d.getAllStreams())
		assert(dict() == d.getStreamsOfType(DataType.IMAGE_2D))
		with pytest.raises(KeyError):
			d.getStream("toto")

		imgs_2d = d.getAllFilesOfType("IMAGE")
		d.createNewStream("cam2d", zip([(0,0),(1,0)],imgs_2d))
		aud = d.getAllFilesOfType("AUDIO")
		d.createNewStream("audio", zip([(1,500000000)],aud))

		with pytest.raises(TypeError) as e:
			d.createNewStream("fail",
			                  zip([(0,0),(1,500000000)],
			                      [imgs_2d[0],aud[0]]
			                     )
			                 )
		assert("Given files are not all of the same type" == e.value.message)

		with pytest.raises(AttributeError) as e:
			d.createNewStream("fail",[])
		assert(
		  "At least one file is needed to create a stream" == e.value.message
		 )

		assert(DataType.IMAGE == d.getStreamType("cam2d"))
		assert(DataType.AUDIO == d.getStreamType("audio"))
		assert(
		    {
		        (0,000000000):"Annotated_JPG_file.jpg",
		        (1,000000000):"JPG_file.jpg"
		    } == d.getStream("cam2d")
		)
		assert(
		    {
		        (1,500000000):"WAV_file.wav"
		    } == d.getStream("audio")
		)
		assert(
		    {
		        "cam2d":
		        {
		            (0,000000000):"Annotated_JPG_file.jpg",
		            (1,000000000):"JPG_file.jpg"
		        }
		    } == d.getStreamsOfType(DataType.IMAGE)
		)
		assert(
		    {
		        "audio":
		        {
		            (1,500000000):"WAV_file.wav"
		        }
		    } == d.getStreamsOfType(DataType.AUDIO)
		)
		assert(
		    {
		        "cam2d":
		        {
		            (0,000000000):"Annotated_JPG_file.jpg",
		            (1,000000000):"JPG_file.jpg"
		        },
		        "audio":
		        {
		            (1,500000000):"WAV_file.wav"
		        }
		    } == d.getAllStreams()
		)

		d.removeFromStream("cam2d", "JPG_file.jpg")
		assert(
		    {
		        "cam2d":
		        {
		            (0,000000000):"Annotated_JPG_file.jpg"
		        }
		    } == d.getStreamsOfType(DataType.IMAGE)
		)
		assert(
		    {
		        "cam2d":
		        {
		            (0,000000000):"Annotated_JPG_file.jpg"
		        },
		        "audio":
		        {
		            (1,500000000):"WAV_file.wav"
		        }
		    } == d.getAllStreams()
		)
		with pytest.raises(ValueError) as e:
			d.removeFromStream("cam2d", "JPG_file.jpg")
		assert(
		    "Given file is not in the stream" == e.value.message
		)
		with pytest.raises(KeyError) as e:
			d.removeFromStream("camxd", "JPG_file.jpg")

		d.addToStream("cam2d", ((0,500000000),"JPG_file.jpg"))
		assert(
		    {
		        "cam2d":
		        {
		            (0,000000000):"Annotated_JPG_file.jpg",
		            (0,500000000):"JPG_file.jpg"
		        },
		        "audio":
		        {
		            (1,500000000):"WAV_file.wav"
		        }
		    } == d.getAllStreams()
		)
		with pytest.raises(KeyError) as e:
			d.addToStream("camxd", ((0,500000000),"JPG_file.jpg"))

		with pytest.raises(ValueError) as e:
			d.addToStream("cam2d", ((0,500000000),"JPG_file20.jpg"))
		assert("Given file is not in the dataset" == e.value.message)

	with QiDataSet(folder_with_annotations, "r") as d:
		assert(
		    {
		        "cam2d":{(0,000000000):"Annotated_JPG_file.jpg",
		                 (0,500000000):"JPG_file.jpg"},
		        "audio":{(1,500000000):"WAV_file.wav"}
		    } == d.getAllStreams()
		)

def test_data_frame(folder_with_annotations):
	with QiDataSet(folder_with_annotations, "w") as d:
		assert([] == d.getAllFrames())

	with QiDataSet(folder_with_annotations, "r") as d:
		assert([] == d.getAllFrames())
		with pytest.raises(ReadOnlyException):
			_f = d.createNewFrame("JPG_file.jpg", "WAV_file.wav")

	with QiDataSet(folder_with_annotations, "w") as d:
		_f = d.createNewFrame("JPG_file.jpg", "WAV_file.wav")
		assert([_f] == d.getAllFrames())
		p = Property("key", "value")
		_f.addAnnotation("jdoe", p, None)
	assert(_f.closed)

	with QiDataSet(folder_with_annotations, "r") as d:
		frames = d.getAllFrames()
		assert(isinstance(frames, list))
		assert(len(frames)==1)
		assert("r" == frames[0].mode)
		assert(set(["JPG_file.jpg", "WAV_file.wav"]) == frames[0].raw_data)
		assert(set(["JPG_file.jpg", "WAV_file.wav"]) == frames[0].files)
		assert(frames[0].annotations.has_key("jdoe"))
		assert(frames[0].annotations["jdoe"].has_key("Property"))
		assert(1 == len(frames[0].annotations["jdoe"]["Property"]))
		assert(None == frames[0].annotations["jdoe"]["Property"][0][1])
		assert("key" == frames[0].annotations["jdoe"]["Property"][0][0].key)
		assert("value" == frames[0].annotations["jdoe"]["Property"][0][0].value)
		with pytest.raises(ReadOnlyException):
			d.removeFrame(frames[0])

	with QiDataSet(folder_with_annotations, "w") as d:
		frames = d.getAllFrames()
		f=frames[0]
		d.removeFrame(f)
		assert([] == d.getAllFrames())
		with pytest.raises(FrameIsInvalid):
			f.raw_data
		with pytest.raises(FrameIsInvalid):
			f.files
		with pytest.raises(FrameIsInvalid):
			f.mode
		with pytest.raises(FrameIsInvalid):
			f.annotations
		with pytest.raises(ClosedFileException):
			p = Property("key", "value")
			f.addAnnotation("jdoe", p, None)
		with pytest.raises(FrameIsInvalid):
			f._open()

	with QiDataSet(folder_with_annotations, "w") as d:
		assert([] == d.getAllFrames())
		_f = d.createNewFrame("JPG_file.jpg", "WAV_file.wav")
		assert(_f == d.getFrame("JPG_file.jpg", "WAV_file.wav"))
		assert(_f == d.getFrame("WAV_file.wav", "JPG_file.jpg"))
		d.removeFrame("WAV_file.wav", "JPG_file.jpg")
		assert([] == d.getAllFrames())

	with QiDataSet(folder_with_annotations, "r") as d:
		assert([] == d.getAllFrames())

def test_dataset_context(folder_with_annotations):
	with QiDataSet(folder_with_annotations, "w") as _ds:
		_ds.context.recorder_names = ["sambrose"]

	with QiDataSet(folder_with_annotations, "r") as _ds:
		assert(["sambrose"] == _ds.context.recorder_names)
		c=Context()
		with pytest.raises(ReadOnlyException):
			_ds.context = c

	with QiDataSet(folder_with_annotations, "w") as _ds:
		with pytest.raises(TypeError):
			_ds.context = Property()
		_ds.context = c

	with QiDataSet(folder_with_annotations, "r") as _ds:
		_ds.context.recorder_names = []