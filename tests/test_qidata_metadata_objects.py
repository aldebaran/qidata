# -*- coding: utf-8 -*-

# Third-party libraries
import pytest

# Local modules
from qidata.metadata_objects import *
from qidata import makeMetadataObject, MetadataType

def test_make_non_existing_metadata_object():
	with pytest.raises(TypeError):
		created_object = makeMetadataObject("")

def test_attributes():
	for metadata_type in list(MetadataType):
		created_object = makeMetadataObject(metadata_type)
		copied_object = makeMetadataObject(metadata_type, created_object)
		assert(created_object == copied_object)
		assert(not created_object is copied_object)

		# Check it is accessible and does not raise
		created_object.version

@pytest.fixture(scope="function",params=[
  {
    "type":Property,
    "instance":Property(key="key", value="value"),
    "inputs":[dict(key="key", value="value")],
    "outputs":[Property(key="key", value="value")],
  },
  {
    "type":TimeStamp,
    "instance":TimeStamp(),
    "inputs":[dict()],
    "outputs":[TimeStamp()],
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