"""Philips Hue Tap (original round, GPD DeviceID 0x02).

Herdsman model 8718696743133 / modelID ``"GreenPower_2"``.  SrcID-addressed
GPD (``ApplicationID`` 0b000).  Depending on how it was commissioned the
security level can be NoSecurity (unencrypted, no key exchange) or
FullFrameCounterAndMIC with an out-of-band pre-configured link key -
security is a commissioning detail and is NOT used for identification.

Four buttons, PRESSED events only.  Kinetic / energy-harvesting device - there
is no button-up frame.  Command IDs verified live via Zigbee2MQTT 2026-06-09:

    press_1 (button_1) -> 0x22  Toggle
    press_2 (button_2) -> 0x10  RecallScene0
    press_3 (button_3) -> 0x11  RecallScene1
    press_4 (button_4) -> 0x12  RecallScene2

SrcIDs in the 0x0040xxxx manufacturing block (verified: 0x00402725,
0x0040ee88, 0x00404c79, 0x0040f4e4).
"""

from __future__ import annotations

from zigpy.quirks import CustomGreenPowerDevice
from zigpy.zgp import GP_CLUSTER_ID, GPDevice
from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    CLUSTER_ID,
    COMMAND,
    COMMAND_ID,
    COMMAND_NOTIFICATION,
    PARAMS,
    PRESSED,
)

_SRC_ID_MASK = 0xFFFF0000
_SRC_ID_MATCH = 0x00400000


class HueTap(CustomGreenPowerDevice, priority=5):
    """Philips Hue Tap (original round) Green Power quirk."""

    manufacturer = "Philips"
    model = "Hue Tap"
    device_automation_triggers: dict[tuple[str, str], dict] = {
        (PRESSED, BUTTON_1): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GP_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x22},  # Toggle
        },
        (PRESSED, BUTTON_2): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GP_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x10},  # RecallScene0
        },
        (PRESSED, BUTTON_3): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GP_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x11},  # RecallScene1
        },
        (PRESSED, BUTTON_4): {
            COMMAND: COMMAND_NOTIFICATION,
            CLUSTER_ID: GP_CLUSTER_ID,
            PARAMS: {COMMAND_ID: 0x12},  # RecallScene2
        },
    }

    @classmethod
    def match(cls, device: GPDevice) -> bool:
        # Security level and key type vary with how the Tap was commissioned
        # (NoSecurity or FullFrameCounterAndMIC observed in the wild).
        # The 0x0040xxxx SrcID block is the reliable identifier.
        return (device.source_id & _SRC_ID_MASK) == _SRC_ID_MATCH


# Module-level aliases so existing imports keep working.
match_hue_tap = HueTap.match
DEVICE_AUTOMATION_TRIGGERS = HueTap.device_automation_triggers
