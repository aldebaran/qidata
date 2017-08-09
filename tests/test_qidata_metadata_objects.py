# -*- coding: utf-8 -*-

# Third-party libraries
import pytest

# Local modules
from qidata.metadata_objects import *
from qidata.metadata_objects import TimeStamp, Transform
from qidata import makeMetadataObject, MetadataType

def test_make_non_existing_metadata_object():
	with pytest.raises(TypeError):
		created_object = makeMetadataObject("")

def test_attributes():
	for metadata_type in list(MetadataType):
		created_object = makeMetadataObject(str(metadata_type))
		created_object = makeMetadataObject(metadata_type)
		copied_object = makeMetadataObject(metadata_type, created_object)
		assert(created_object == copied_object)
		assert(not created_object is copied_object)

		# Check it is accessible and does not raise
		created_object.version

@pytest.fixture(scope="function",params=[
  {
    "type":Face,
    "instance":Face("Pepper", 12),
    "inputs":[
              {
                  "name":"Pepper",
                  "id":10,
                  "version":"0.1"},
              {
                  "name":"gszwarc",
                  "fid":0,
                  "age":27,
                  "expression":[0.140624997439,
                                0.223124995478,
                                0.0318749987055,
                                0.247499989579,
                                0.356874989346],
                  "facial_parts":[
                                  [[98, 53], 0.175687507952],
                                  [[130, 60], 0.0129375002653],
                                  [[124, 106], 0.0884375025926],
                                  [[105, 58], 0.175687507952],
                                  [[89, 54], 0.175687507952],
                                  [[123, 61], 0.0129375002653],
                                  [[134, 62], 0.0129375002653],
                                  [[100, 105], 0.0884375025926],
                                  [[131, 109], 0.0884375025926],
                                  [[114, 83], 0.242000014216],
                                  [[128, 85], 0.242000014216],
                                  [[125, 96], 0.0884375025926]
                                 ],
                  "gender":"male",
                  "smile":[0.394999994896,0.0751250039757],
                  "version":"0.2"
                },
              {
                  "name":"gszwarc",
                  "age":27,
                  "expression":[0.140624997439,
                                0.223124995478,
                                0.0318749987055,
                                0.247499989579,
                                0.356874989346],
                  "facial_parts":[
                                  {
                                      "coordinates":[98, 53],
                                      "confidence":0.175687507952
                                  },
                                  {
                                      "coordinates":[130, 60],
                                      "confidence":0.0129375002653
                                  },
                                  {
                                      "coordinates":[124, 106],
                                      "confidence":0.0884375025926
                                  },
                                  {
                                      "coordinates":[105, 58],
                                      "confidence":0.175687507952
                                  },
                                  {
                                      "coordinates":[89, 54],
                                      "confidence":0.175687507952
                                  },
                                  {
                                      "coordinates":[123, 61],
                                      "confidence":0.0129375002653
                                  },
                                  {
                                      "coordinates":[134, 62],
                                      "confidence":0.0129375002653
                                  },
                                  {
                                      "coordinates":[100, 105],
                                      "confidence":0.0884375025926
                                  },
                                  {
                                      "coordinates":[131, 109],
                                      "confidence":0.0884375025926
                                  },
                                  {
                                      "coordinates":[114, 83],
                                      "confidence":0.242000014216
                                  },
                                  {
                                      "coordinates":[128, 85],
                                      "confidence":0.242000014216
                                  },
                                  {
                                      "coordinates":[125, 96],
                                      "confidence":0.0884375025926
                                  },
                                 ],
                  "gender":"male",
                  "smile":[0.394999994896,0.0751250039757],
                  "version":"0.3"
              }
          ],
    "outputs":[
            Face("Pepper", 0),
            Face("gszwarc",27,
                gender="male",
            ),
            Face("gszwarc",27,
                gender="male",
            )
        ],
  },
  {
    "type":Object,
    "instance":Object("qrcode", "10", 1),
    "inputs":[{"type":"qrcode", "value":"Hello!", "id":10, "version":"0.1"}],
    "outputs":[Object("qrcode", "Hello!", 10)],
  },
  {
    "type":Person,
    "instance":Person("Pepper"),
    "inputs":[{"name":"Pepper", "id":10, "version":"0.1"}],
    "outputs":[Person("Pepper")],
  },
  {
    "type":Property,
    "instance":Property(key="key", value="value"),
    "inputs":[dict(key="key", value="value")],
    "outputs":[Property(key="key", value="value")],
  },
  {
    "type":Speech,
    "instance":Speech("Pepper", "Hello, I'm Pepper"),
    "inputs":[{"name":"Pepper", "sentence":"Hello world", "id":10, "version":"0.1"}],
    "outputs":[Speech("Pepper", "Hello world")],
  },
  {
    "type":TimeStamp,
    "instance":TimeStamp(),
    "inputs":[dict()],
    "outputs":[TimeStamp()],
  },
  {
    "type":Transform,
    "instance":Transform(),
    "inputs":[dict()],
    "outputs":[Transform()],
  },
])
def metadata_objects(request):
	return request.param

def test_make_default_object(metadata_objects):
	def_object = metadata_objects["type"]()

def test_copy_object(metadata_objects):
	copy = metadata_objects["type"](metadata_objects["instance"])
	assert(copy == metadata_objects["instance"])
	assert(not (copy is metadata_objects["instance"]))

def test_too_many_arguments(metadata_objects):
	args = []
	for attrib in metadata_objects["type"].__ATTRIBUTES__:
		args.append(getattr(metadata_objects["instance"], attrib.id))
	args.append(0)
	with pytest.raises(TypeError):
		metadata_objects["type"](*args)

def test_wrong_keys(metadata_objects):
	with pytest.raises(TypeError):
		metadata_objects["type"](aspcfgbenrgahreb=0)

def test_import_from_old_versions(metadata_objects):
	for input_dict, gnd in zip(metadata_objects["inputs"], metadata_objects["outputs"]):
		output_object = metadata_objects["type"].fromDict(input_dict)
		assert(output_object == gnd)