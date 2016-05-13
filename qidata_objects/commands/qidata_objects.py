# -*- coding: utf-8 -*-

# Standard Library
import os.path

# Qidata
from .. import DataObjectTypes, printHelp

class QiDataObjectsCommand:

	@staticmethod
	def show(args):
		printHelp(args.type_name)
		pass

	@staticmethod
	def list(args):
		print DataObjectTypes
