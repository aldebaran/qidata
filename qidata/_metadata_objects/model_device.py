
# Standard libraries
import pkg_resources as _pkg

# qidata
from qidata._metadata_objects import _QidataEnumMixin

# Create list
device_model_list=[
	"UNSPECIFIED"
]

# Load device model plugins
for _ep in _pkg.iter_entry_points(group="qidata.context.device_models"):
	device_model_list.extend(_ep.load())

device_model_list.sort()

def generateEnum():
	return _QidataEnumMixin("DeviceModel", device_model_list)