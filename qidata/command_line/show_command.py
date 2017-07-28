# -*- coding: utf-8 -*-

# Standard libraries
import os
import sys

# Third-party libraries
import argparse
try:
	import argcomplete
	has_argcomplete = True
except ImportError:
	has_argcomplete = False

# Local modules
import qidata
from qidata import qidataset

DESCRIPTION = "Shows information about a QiData element"

class ShowCommand:

	@staticmethod
	def show(args):
		throwIfAbsent(args.path)
		if qidataset.isDataset(args.path):
			with qidataset.QiDataSet(args.path) as p:
				return str(p)
		elif os.path.isdir(args.path):
			sys.exit(args.path+" isn't a valid QiDataSet")

		elif qidata.isSupported(args.path):
			with qidata.open(args.path) as p:
				return str(p)

		else:
			sys.exit(args.path+" is not supported")

# ───────
# Helpers

def throwIfAbsent(path):
	if not os.path.exists(path):
		sys.exit(path+" doesn't exist")

# ──────
# Parser

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):
	path_argument = parent_parser.add_argument("path", help="what to examine")
	if has_argcomplete: path_argument.completer = argcomplete.completers.FilesCompleter()
	parent_parser.set_defaults(func=ShowCommand.show)
	return parent_parser
