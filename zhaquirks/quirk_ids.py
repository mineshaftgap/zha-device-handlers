"""Quirk IDs used for matching quirked devices in ZHA."""

# Konke
# Danfoss
DANFOSS_ALLY_THERMOSTAT = "danfoss.ally_thermostat"

KONKE_BUTTON = "konke.button_remote"  # remote with custom handling in cluster handler

# SE (Smart Energy)
SE_POLL_SUMMATION = "se.poll_summation"  # SE devices with poll summation cluster

# Siren
SIREN_BASIC = "siren.basic"  # basic siren with on/off

# Tuya
TUYA_PLUG_ONOFF = "tuya.plug_on_off_attributes"  # plugs with configurable attributes on the OnOff cluster
TUYA_PLUG_MANUFACTURER = "tuya.plug_manufacturer_attributes"  # plugs with configurable attributes on a custom cluster

# Xiaomi
XIAOMI_AQARA_VIBRATION_AQ1 = (
    "xiaomi.aqara_vibration_aq1"  # vibration sensor with custom cluster handler
)
