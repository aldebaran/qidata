
# Third-party
import enum

device_model_list=[
	"SOFTBANK_ROBOTICS__NAO_V4",
	"SOFTBANK_ROBOTICS__NAO_V5",
	"SOFTBANK_ROBOTICS__PEPPER_V16",
	"SOFTBANK_ROBOTICS__PEPPER_V17",
	"UNSPECIFIED"
]




def generateEnum():
	return enum.EnumMeta("DeviceModel",
	                        (enum.Enum,),
	                        dict(
	                            [[device_model_list[i], i] for i in range(len(device_model_list))]
	                        )
	                    )