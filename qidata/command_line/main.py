# -*- coding: utf-8 -*-

# Argparse
import argparse
# qidata
# from qidata import VERSION

DESCRIPTION = "Manage metadata information"
SUBCOMMANDS = []

# try:
# 	from qidata_gui.apps.annotator.commands import main as AnnotationMain
# 	SUBCOMMANDS.append([AnnotationMain, "annotate"])
# except:
# 	pass

try:
	import file_commands
	SUBCOMMANDS.append([file_commands, "file"])
except Exception, e:
	print e

try:
	import set_commands
	SUBCOMMANDS.append([set_commands, "set"])
except Exception, e:
	print e

# class VersionAction(Action):
# 	def __init__(self, option_strings, dest, nargs, **kwargs):
# 		super(VersionAction, self).__init__(option_strings, dest, nargs=0, **kwargs)
# 	def __call__(self, parser, namespace, values, option_string):
# 		version_string = VERSION + "\n"
# 		parser.exit(message=version_string)

def parser():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	subparsers = parser.add_subparsers()
	for sc in SUBCOMMANDS:
		sub_parser = subparsers.add_parser(sc[1],
		                                      description=sc[0].DESCRIPTION,
		                                      help=sc[0].DESCRIPTION)
		sc[0].make_command_parser(sub_parser)

	# parser.add_argument("-v", "--version", action=VersionAction, nargs=0,
	#                     help="print qidata release version number")
	return parser

main_parser = parser()
