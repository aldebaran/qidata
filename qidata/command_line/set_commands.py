# -*- coding: utf-8 -*-

# Standard libraries
import sys

# Third-party libraries
import argparse
try:
	import argcomplete
	has_argcomplete = True
except ImportError:
	has_argcomplete = False

# Local modules
from qidata import qidataset

DESCRIPTION = "Shows information about a QiDataSet"

class QiDataSetCommand:

	@staticmethod
	def show(args):
		throwIfAbsent(args.dataset)
		with qidataset.QiDataSet(args.dataset) as p:
			return str(p)

# ───────
# Helpers

def throwIfAbsent(qidataset_path):
	if not qidataset.isDataset(qidataset_path):
		sys.exit(qidataset_path+" doesn't exist or isn't a valid QiDataSet")


# ──────
# Parser

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):
	subparsers = parent_parser.add_subparsers()

	# ────────────────
	# show sub-command

	show_parser = subparsers.add_parser("show", description="Show QiData objects stored in dataset",
	                                    help="Show QiData objects stored in dataset")
	dataset_argument = show_parser.add_argument("dataset", help="what to examine")
	if has_argcomplete: dataset_argument.completer = argcomplete.completers.FilesCompleter()
	show_parser.set_defaults(func=QiDataSetCommand.show)

	return parent_parser

dataset_parser = make_command_parser()