# -*- coding: utf-8 -*-

# Argparse
import argparse
# qidata
import qidata.version

DESCRIPTION = "Manage data-sets"
SUBCOMMANDS = []

try:
	from annotator.commands import main as AnnotationMain
	SUBCOMMANDS.append([AnnotationMain, "annotate"])
except:
	pass

try:
	from qidata_file.commands import main as QiDataFileMain
	SUBCOMMANDS.append([QiDataFileMain, "file"])
except:
	pass

try:
	from qidata_objects.commands import main as ObjectsMain
	SUBCOMMANDS.append([ObjectsMain, "objects"])
except:
	pass

try:
	from xmp.commands import main as XmpMain
	SUBCOMMANDS.append([XmpMain, "xmp"])
except:
	pass

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
