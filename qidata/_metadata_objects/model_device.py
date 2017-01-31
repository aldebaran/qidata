
# qidata
from qidata._metadata_objects import _QidataEnumMixin

device_model_list=[
	"PANASONIC__DMC_LX7",
	"SOFTBANK_ROBOTICS__NAO_V4",
	"SOFTBANK_ROBOTICS__NAO_V5",
	"SOFTBANK_ROBOTICS__PEPPER_V16",
	"SOFTBANK_ROBOTICS__PEPPER_V17",
	"UNSPECIFIED"
]

def generateEnum():
	return _QidataEnumMixin("DeviceModel", device_model_list)