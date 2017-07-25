# -*- coding: utf-8 -*-
# Standard library
import pytest

# Third-party libraries

# Local modules
from qidata.command_line import main

@pytest.mark.parametrize("command_args",
	[
		[
			"file",
			"show",
			"tests/data/SpringNebula.jg"
		],
	]
)
def test_failing_file_command(command_args):
	parser = main.parser()
	parsed_arguments = parser.parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)

@pytest.mark.parametrize("command_args,expected",
                          [
                            (
                              [
                                "file",
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
                                "file",
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
def test_file_command(command_args, expected):
	parser = main.parser()
	parsed_arguments = parser.parse_args(command_args)
	res = parsed_arguments.func(parsed_arguments)
	print res
	assert(expected == res)

@pytest.mark.parametrize("command_args",
	[
		[
			"set",
			"show",
			"tests/data/unknown"
		],
	]
)
def test_failing_set_command(command_args):
	parser = main.parser()
	parsed_arguments = parser.parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)
