# -*- coding: utf-8 -*-
# Standard library
import pytest
import argparse
import subprocess

# Third-party libraries

# Local modules
from qidata.command_line import (file_commands,
                                 main,
                                 set_commands)

@pytest.mark.parametrize("command_args",
	[
		[
			"show",
			"tests/data/SpringNebula.jg"
		],
	]
)
def test_failing_file_command(command_args, file_command_parser):
	parsed_arguments = file_command_parser.parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)

@pytest.mark.parametrize("command_args,expected",
                          [
                            (
                              [
                                "show",
                                "tests/data/SpringNebula.jpg"
                              ],
"""File name: tests/data/SpringNebula.jpg
Object type: IMAGE
Object timestamp: 
├─ seconds: 0
└─ nanoseconds: 0
Object transform: 
├─ translation: 
│  ├─ x: 0.0
│  ├─ y: 0.0
│  └─ z: 0.0
└─ rotation: 
   ├─ x: 0.0
   ├─ y: 0.0
   ├─ z: 0.0
   └─ w: 1.0
Image shape: (2232, 3968, 3)
"""
                            ),
                            (
                              [
                                "show",
                                "tests/data/Annotated_JPG_file.jpg"
                              ],
"""File name: tests/data/Annotated_JPG_file.jpg
Object type: IMAGE
Object timestamp: 
├─ seconds: 0
└─ nanoseconds: 0
Object transform: 
├─ translation: 
│  ├─ x: 0.0
│  ├─ y: 0.0
│  └─ z: 0.0
└─ rotation: 
   ├─ x: 0.0
   ├─ y: 0.0
   ├─ z: 0.0
   └─ w: 1.0
Annotator: sambrose
└─ Property
   └─ 0:  (Location: None):
      ├─ key: key
      └─ value: value
Image shape: (2232, 3968, 3)
"""
                            ),
                          ]
                        )
def test_file_command(command_args, expected, file_command_parser):
	parsed_arguments = file_command_parser.parse_args(command_args)
	res = parsed_arguments.func(parsed_arguments)
	print res
	assert(expected == res)

@pytest.mark.parametrize("command_args",
	[
		[
			"show",
			"tests/data/unknown"
		],
	]
)
def test_failing_set_command(command_args, set_command_parser):
	parsed_arguments = set_command_parser.parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)

@pytest.mark.parametrize("command_args,expected",
                          [
                            (
                              [
                                "show",
                                "tests/data/Michal_Asus_2016-02-19-15-25-46"
                              ],
"""Dataset path: tests/data/Michal_Asus_2016-02-19-15-25-46
Available types: 
├─ 0: IMAGE_2D
├─ 1: IMAGE_3D
└─ 2: IMAGE_IR
Available streams: 
├─ depth: 52 files
├─ front: 40 files
└─ ir: 52 files
Defined frames: 141
Context: 
├─ recording_location: 
│  ├─ country: UNSPECIFIED
│  ├─ city: ""
│  ├─ latitude: None
│  ├─ longitude: None
│  └─ tags: []
├─ recording_datetime: 
│  ├─ year: None
│  ├─ month: None
│  ├─ day: None
│  ├─ hour: None
│  ├─ starting_timestamp: None
│  └─ length: None
├─ recording_device: 
│  ├─ device_model: UNSPECIFIED
│  ├─ device_id: ""
│  └─ sw_version: ""
├─ recorder_names: []
├─ environmental_description: 
│  ├─ category: UNSPECIFIED
│  ├─ light_conditions: 
│  │  ├─ outdoor_light: UNSPECIFIED
│  │  ├─ indoor_light: UNSPECIFIED
│  │  └─ ambient_luminosity: None
│  └─ sound_conditions: 
│     ├─ ambient_sound_reverberation: None
│     └─ ambient_sound_level: None
└─ tags: []
Available annotations: 
"""
                            ),
                          ]
                        )
def test_set_command(command_args, expected,set_command_parser):
	parsed_arguments = set_command_parser.parse_args(command_args)
	res = parsed_arguments.func(parsed_arguments)
	print res
	assert(expected == res)

def test_main_command():
  parser = main.parser()
  with pytest.raises(SystemExit):
    parser.parse_args(["-v"])

def test_main():
  subprocess.check_call(["qidata", "-h"])