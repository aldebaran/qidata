# Standard library
import pytest

# Third-party libraries
import argparse

# Local modules
from qidata.commands.main import parser

@pytest.mark.parametrize("command_args",
	[
		[
			"set",
			"show",
			"tests/data/dataset_annotated"
		],
		[
			"file",
			"show",
			"tests/data/dataset_annotated/JPG_file.jpg"
		],
		[
			"file",
			"version",
			"tests/data/dataset_annotated/JPG_file.jpg"
		]
	]
)
def test_successful_command(command_args):
	parsed_arguments = parser().parse_args(command_args)
	parsed_arguments.func(parsed_arguments)

@pytest.mark.parametrize("command_args",
	[
		[
			"set",
			"show",
			"tests/data/fake_dataset"
		],
		[
			"file",
			"show",
			"tests/data/fake_dataset/JPG_file.jpg"
		],
		[
			"file",
			"version",
			"tests/data/fake_dataset/JPG_file.jpg"
		]
	]
)
def test_failing_command(command_args):
	parsed_arguments = parser().parse_args(command_args)
	with pytest.raises(SystemExit):
		parsed_arguments.func(parsed_arguments)
