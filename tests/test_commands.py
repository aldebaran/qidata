# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard library
import pytest
import subprocess

# Third-party libraries

# Local modules
from qidata.command_line import main
from qidata import VERSION

@pytest.mark.parametrize("command_args",
	[
		[
			"tests/data/SpringNebula.jg"
		],
	]
)
def test_failing_show_on_file_command(command_args, show_command_parser):
	parsed_arguments = show_command_parser.parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)

@pytest.mark.parametrize("command_args,expected",
                          [
                            (
                              [
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
                                "tests/data/JPG_with_external_annotations.jpg"
                              ],
"""File name: tests/data/JPG_with_external_annotations.jpg
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
                            (
                              [
                                "tests/data/JPG_with_external_annotations.jpg.xmp"
                              ],
"""File name: tests/data/JPG_with_external_annotations.jpg
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
                            (
                              [
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
def test_show_on_file_command(command_args, expected, show_command_parser):
	parsed_arguments = show_command_parser.parse_args(command_args)
	res = parsed_arguments.func(parsed_arguments)
	print res
	assert(expected == res)

@pytest.mark.parametrize("command_args",
	[
		[
			"tests/data/unknown"
		],
	]
)
def test_failing_show_on_set_command(command_args, show_command_parser):
	parsed_arguments = show_command_parser.parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)

@pytest.mark.parametrize("command_args,expected",
                          [
                            (
                              [
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
def test_show_on_set_command(command_args, expected,show_command_parser):
	parsed_arguments = show_command_parser.parse_args(command_args)
	res = parsed_arguments.func(parsed_arguments)
	print res
	assert(expected == res)

def test_main_command():
  parser = main.parser()
  with pytest.raises(SystemExit):
    parser.parse_args(["-v"])

def test_main():
  # Test something is printed
  subprocess.check_call(["qidata", "-h"])

  # Test version print
  assert(
    VERSION+"\n" == subprocess.check_output(["qidata", "-v"],
                                            stderr=subprocess.STDOUT)
  )

  # Test return of show function
  res = """File name: tests/data/Annotated_JPG_file.jpg
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
  assert(res == subprocess.check_output(["qidata",
                                         "show",
                                         "tests/data/Annotated_JPG_file.jpg"]))
