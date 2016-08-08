# -*- coding: utf-8 -*-

# Argparse
import argparse
try:
    import argcomplete
    has_argcomplete = True
except ImportError:
    has_argcomplete = False

# xmp
from .qidata_objects import QiDataObjectsCommand
from .. import version, DataObjectTypes

DESCRIPTION = "QiData objects definition tools"

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):

    subparsers = parent_parser.add_subparsers()

    parent_parser.add_argument("-v", "--version", action=version.VersionAction, nargs=0,
                        help="print QiData objects release version number")

    # ────────────────
    # show sub-command

    show_parser = subparsers.add_parser("show", description="show details on a specific type")
    file_argument = show_parser.add_argument("type_name", help="which type to detail")
    if has_argcomplete: file_argument.completer = argcomplete.completers.ChoicesCompleter(DataObjectTypes)
    show_parser.set_defaults(func=QiDataObjectsCommand.show)

    # ───────────────
    # list sub-command

    list_parser = subparsers.add_parser("list", description="show all available types")
    list_parser.set_defaults(func=QiDataObjectsCommand.list)

    return parent_parser

main_parser = make_command_parser()
