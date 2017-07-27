# -*- coding: utf-8 -*-

# Standard libraries
import pkg_resources as _pkg

# Third-party libraries
import argparse

# Local modules
from qidata import VERSION

DESCRIPTION = "Manage metadata information"
SUBCOMMANDS = []

# Load command plugins
for _ep in _pkg.iter_entry_points(group="qidata.commands"):
	_name = _pkg.EntryPoint.pattern.match(str(_ep)).groupdict()["name"]
	SUBCOMMANDS.append([_ep.load(), _name])


# try:
# 	from qidata_gui.apps.annotator.commands import main as AnnotationMain
# 	SUBCOMMANDS.append([AnnotationMain, "annotate"])
# except:
# 	pass

class VersionAction(Action):
	def __init__(self, option_strings, dest, nargs, **kwargs):
		super(VersionAction, self).__init__(option_strings, dest, nargs=0, **kwargs)
	def __call__(self, parser, namespace, values, option_string):
		version_string = VERSION + "\n"
		parser.exit(message=version_string)

def parser():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	subparsers = parser.add_subparsers()
	for sc in SUBCOMMANDS:
		sub_parser = subparsers.add_parser(sc[1],
		                                      description=sc[0].DESCRIPTION,
		                                      help=sc[0].DESCRIPTION)
		sc[0].make_command_parser(sub_parser)

	parser.add_argument("-v", "--version", action=VersionAction, nargs=0,
	                    help="print qidata release version number")
	return parser

main_parser = parser()
