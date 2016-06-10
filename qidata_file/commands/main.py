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

    return parent_parser

main_parser = make_command_parser()
