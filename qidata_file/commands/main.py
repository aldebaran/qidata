# -*- coding: utf-8 -*-

# Argparse
import argparse
try:
    import argcomplete
    has_argcomplete = True
except ImportError:
    has_argcomplete = False

# qidata_file
from .qidata_file import QiDataFilesCommand
from .. import version

DESCRIPTION = "Analyze QiDataObjects stored in QiDataFiles"

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):
    subparsers = parent_parser.add_subparsers()

    parent_parser.add_argument("-v", "--version", action=version.VersionAction, nargs=0,
                        help="print QiDataFile release version number")

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
                            help="user who annotated this file (mandatory for V1 files)")

    if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
    convert_parser.set_defaults(func=QiDataFilesCommand.convert)

    return parent_parser

main_parser = make_command_parser()
