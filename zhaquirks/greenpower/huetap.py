"""Philips Hue Tap (original round, GPD DeviceID 0x02).

Herdsman model 8718696743133 / modelID ``"GreenPower_2"``.  SrcID-addressed
GPD (``ApplicationID`` 0b000), ``SecurityLevel.NoSecurity`` — unencrypted,
commissions by button-press with no key exchange.

Written against zigpy PR #1814 head (d154a9f).  When ``CustomGreenPowerDevice``
lands in ``zigpy.quirks`` (see konistehrad/zha-device-handlers@zgp), refactor
to inherit from that base class and turn ``match_hue_tap()`` into a classmethod.

Four buttons, PRESSED events only.  Kinetic / energy-harvesting device — there
is no button-up frame.  Command IDs verified live via Zigbee2MQTT 2026-06-09:

    press_1 (button_1) → 0x22  Toggle
    press_2 (button_2) → 0x10  RecallScene0
    press_3 (button_3) → 0x11  RecallScene1
    press_4 (button_4) → 0x12  RecallScene2

SrcIDs in the 0x0040xxxx manufacturing block (verified: 0x00402725,
0x0040ee88, 0x00404c79, 0x0040f4e4).
"""

from __future__ import annotations

from zigpy.zgp import GP_CLUSTER_ID, GPDevice, SecurityKeyType, SecurityLevel
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

MANUFACTURER = "Philips"
MODEL = "Hue Tap"


def match_hue_tap(device: GPDevice) -> bool:
    """Return True if device fingerprints as an original Philips Hue Tap."""
    return (
        device.security_level is SecurityLevel.NoSecurity
        and device.security_key_type is SecurityKeyType.NoKey
        and (device.source_id & _SRC_ID_MASK) == _SRC_ID_MATCH
    )


DEVICE_AUTOMATION_TRIGGERS: dict[tuple[str, str], dict] = {
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
