# -*- coding: utf-8 -*-

# Standard Library
import os.path
from distutils.version import StrictVersion

# Qidata
from qidata import qidatafile
from qidata.files.conversion import qidataFileConversionToCurrentVersion
from qidata.files.version import identifyFileAnnotationVersion, CURRENT_VERSION

# Argparse
import argparse
try:
	import argcomplete
	has_argcomplete = True
except ImportError:
	has_argcomplete = False

DESCRIPTION = "Analyze QiDataObjects stored in QiDataFiles"

class QiDataFilesCommand:

	@staticmethod
	def show(args):
		throwIfAbsent(args.file)
		version = identifyFileAnnotationVersion(args.file)
		if version is None:
			print "File does not contain any qidata annotation"
		else:
			if StrictVersion(version)<StrictVersion(CURRENT_VERSION):
				print "File is out-dated: use \"convert\" command to upgrade your file"
			else:
				with qidatafile.open(args.file) as p:
					print p

	@staticmethod
	def convert(args):
		for file in args.file:
			throwIfAbsent(file)
			qidataFileConversionToCurrentVersion(file, vars(args))

	@staticmethod
	def version(args):
		for file in args.file:
			throwIfAbsent(file)
			print "%s: %s"%(file, identifyFileAnnotationVersion(file))

# ───────
# Helpers

def throwIfAbsent(file_path):
	if not os.path.isfile(file_path):
		import sys
		sys.exit("File "+file_path+" doesn't exist")


# ──────
# Parser

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):
	subparsers = parent_parser.add_subparsers()

	# ────────────────
	# show sub-command

	show_parser = subparsers.add_parser("show", description="Show QiData objects stored in file",
	                                    help="Show QiData objects stored in file")
	file_argument = show_parser.add_argument("file", help="what to examine")
	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	show_parser.set_defaults(func=QiDataFilesCommand.show)

	# ────────────────
	# convert sub-command

	convert_parser = subparsers.add_parser("convert",
	                        description="Updates Qidata files metadata to fit the newest convention",
	                        help="Updates Qidata files metadata to fit the newest convention")
	file_argument = convert_parser.add_argument("file", nargs="+", help="what to examine")
	annotator_argument = convert_parser.add_argument("--annotator",
	                        help="user who annotated this file (mandatory for v0.1 files)")

	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	convert_parser.set_defaults(func=QiDataFilesCommand.convert)

	# ───────────────────
	# version sub-command

	version_parser = subparsers.add_parser("version",
	                        description="Identify Qidata file version",
	                        help="Identify Qidata file version")
	file_argument = version_parser.add_argument("file", nargs="+", help="what to examine")

	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	version_parser.set_defaults(func=QiDataFilesCommand.version)

	return parent_parser

file_parser = make_command_parser()