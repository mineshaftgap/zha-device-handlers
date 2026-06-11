"""Module for Green Power quirk implementations."""

# Inject GP-specific constants into zhaquirks.const so that quirk files can use
# the standard `from zhaquirks.const import ...` pattern without diverging from
# upstream. PyPI zha-quirks==1.2.0 doesn't include these constants.
import zhaquirks.const as _const

_GP_EXTRAS = {
    "BUTTON_1_AND_2": "button_1_and_2",
    "BUTTON_1_AND_3": "button_1_and_3",
    "BUTTON_1_AND_4": "button_1_and_4",
    "BUTTON_2_AND_3": "button_2_and_3",
    "BUTTON_2_AND_4": "button_2_and_4",
    "BUTTON_3_AND_4": "button_3_and_4",
    "COMMAND_NOTIFICATION": "notification",
    "ENERGY_BAR": "energy_bar",
}
for _k, _v in _GP_EXTRAS.items():
    if not hasattr(_const, _k):
        setattr(_const, _k, _v)
