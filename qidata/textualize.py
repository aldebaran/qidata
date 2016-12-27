# -*- coding: utf-8 -*-

# ─────────────────────
# Formatting parameters

INDENT_SIZE = 3
AFTER_MID_INDENT = u'│' + ' ' * (INDENT_SIZE-1)
AFTER_LAST_INDENT = ' ' * (INDENT_SIZE)
TREE_INDENT = u'─'*(INDENT_SIZE-2) + " "
TREE_MID_INDENT  = u"├" + TREE_INDENT
TREE_LAST_INDENT = u"└" + TREE_INDENT


def textualize_list(list_to_display):
	if len(list_to_display) == 0:
		return "[]"

	else:
		res_str = "\n"

	for index in range(len(list_to_display)):
		value = list_to_display[index]
		if index != len(list_to_display)-1:
			res_str += TREE_MID_INDENT + unicode(index) + ": " + unicode(value) + "\n"
		else:
			res_str += TREE_LAST_INDENT + unicode(index) + ": " + unicode(value)

	return res_str

def textualize_dict(dict_to_display):
	keys = dict_to_display.keys()
	keys.sort()
	if len(keys) == 0:
		return "{}"
	else:
		res_str = ""

	for key in keys:
		value = dict_to_display[key]
		if key != keys[-1]:
			res_str += "\n" + TREE_MID_INDENT
			indent_level = AFTER_MID_INDENT
		else:
			res_str += "\n" + TREE_LAST_INDENT
			indent_level = AFTER_LAST_INDENT
		res_str += key + "="
		res_str += unicode(value).replace("\n","\n"+(indent_level))

	return res_str

def textualize_annotations(annotations_to_display):
	res_str = ""
	if len(annotations_to_display) > 0:
		for i in range(len(annotations_to_display)):
			annotation_str = "\n"
			if i != len(annotations_to_display)-1:
				annotation_str += TREE_MID_INDENT
				indent_level = AFTER_MID_INDENT
			else:
				annotation_str += TREE_LAST_INDENT
				indent_level = AFTER_LAST_INDENT
			annotation_str += "%d: "%i
			annotation_str += " (Location: " + unicode(annotations_to_display[i][1]) + "):"
			annotation_str += unicode(annotations_to_display[i][0]).replace("\n","\n"+(indent_level))
			res_str += annotation_str
	else:
		res_str += "\n" + TREE_LAST_INDENT + "[]"
	return res_str

def textualize_metadata(metadata_to_display):
	res_str = ""
	for metadata_type in metadata_to_display:
		key = metadata_type
		metadata_type_str = "\n"
		if metadata_type != metadata_to_display.keys()[-1]:
			metadata_type_str += TREE_MID_INDENT + metadata_type
			indent_level = AFTER_MID_INDENT
		else:
			metadata_type_str += TREE_LAST_INDENT + metadata_type
			indent_level = AFTER_LAST_INDENT
		res_str += metadata_type_str
		res_str += textualize_annotations(metadata_to_display[metadata_type]).replace("\n","\n"+(indent_level))
	return res_str