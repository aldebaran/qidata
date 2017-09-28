#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Use argcomplete if available on system; don't remove the following line, it's
# essential for argcomplete to work !
# PYTHON_ARGCOMPLETE_OK

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Standard libraries
import sys
import os

# Third-party libraries
try:
	import argcomplete
	has_argcomplete = True
except ImportError:
	has_argcomplete = False

# Local modules
from qidata.command_line.main import parser

def main(args=None):

	# –––––––––––––
	# Get arguments

	if args is None:
		args = sys.argv[1:]

	# ––––––––––––
	# Build parser

	main_parser = parser()

	# –––––––––––––––
	# Auto-completion

	if has_argcomplete:
		argcomplete.autocomplete(main_parser, exclude=["-h", "--help",
		                                               "-v", "--version"])
		# NOTE: The program exits here when launched for autocompletion

	# –––––––
	# Execute

	parsed_arguments = main_parser.parse_args(args)
	try:
		res = parsed_arguments.func(parsed_arguments)
		if res is not None:
			print res
		return 0
	except SystemExit, ex:
		raise ex
	except BaseException as exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()

		import traceback
		def rawEntry(e):
			return "\n".join([l.lstrip() for l in e.rstrip().split("\n")])
		print "Backtrace:"
		backtrace_entries = [rawEntry(e) for e in traceback.format_tb(exc_traceback)]
		for e in backtrace_entries[:-1]:
			print "├─ " + e.replace("\n", "\n│  \t")
		last_entry = backtrace_entries[-1]
		print "╰╼ " + last_entry.replace("\n", "\n   \t")

		print "Uncaught exception" + " " + type(exception).__name__
		exception_message = str(exception)
		if exception_message:
			print "\t" + exception_message.replace("\n", "\n\t")

		print "Send this to the maintainer for help"
		return 1

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#

if __name__ == "__main__":
	# When this program is launched by argcomplete, sys.argv only contains the name
	# of the program, and argcomplete.autocomplete actually uses the partial command
	# line for completion passed as an environment variable. This is normally
	# transparent, but here we're manually parsing the first argument of the command
	# to dynamically adjust the parser, so we must simulate a real sys.argv.
	if has_argcomplete and '_ARGCOMPLETE' in os.environ:
		launched_by_argcomplete = True
		argv = os.environ['COMP_LINE'].split()[1:]
	else:
		launched_by_argcomplete = False
		argv = sys.argv[1:]
	main(argv)