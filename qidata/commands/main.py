# -*- coding: utf-8 -*-

# Argparse
import argparse
# qidata
import qidata.version

DESCRIPTION = "Manage metadata information"
SUBCOMMANDS = []

try:
	from qidata_gui.apps.annotator.commands import main as AnnotationMain
	SUBCOMMANDS.append([AnnotationMain, "annotate"])
except:
	pass

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

def parser():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	subparsers = parser.add_subparsers()
	for sc in SUBCOMMANDS:
		sub_parser = subparsers.add_parser(sc[1],
		                                      description=sc[0].DESCRIPTION,
		                                      help=sc[0].DESCRIPTION)
		sc[0].make_command_parser(sub_parser)

	parser.add_argument("-v", "--version", action=qidata.version.VersionAction, nargs=0,
	                    help="print qidata release version number")
	return parser

main_parser = parser()
