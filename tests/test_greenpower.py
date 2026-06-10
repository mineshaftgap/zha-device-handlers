"""Tests for the Green Power quirks.

Uses zigpy PR #1814's GPDevice directly — the same object the quirks
will receive when CustomGreenPowerDevice lands in zigpy.quirks.
"""

from __future__ import annotations

import pytest
from zigpy.zgp import GPDevice, SecurityKeyType, SecurityLevel

from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    CLUSTER_ID,
    COMMAND_ID,
    PARAMS,
    PRESSED,
)
from zhaquirks.greenpower.huetap import DEVICE_AUTOMATION_TRIGGERS, match_hue_tap

# All four SrcIDs confirmed on real Taps (2026-06-09 via Z2M)
HUE_TAP_SRC_IDS = [0x00402725, 0x0040EE88, 0x00404C79, 0x0040F4E4]

# Expected (button, command_id) — cross-checks trigger map against Z2M decode
EXPECTED_TRIGGERS = [
    (BUTTON_1, 0x22),  # Toggle   / press_1
    (BUTTON_2, 0x10),  # RecallScene0 / press_2
    (BUTTON_3, 0x11),  # RecallScene1 / press_3
    (BUTTON_4, 0x12),  # RecallScene2 / press_4
]


# --- match_hue_tap -----------------------------------------------------------


@pytest.mark.parametrize("src_id", HUE_TAP_SRC_IDS)
def test_match_returns_true_for_known_taps(src_id: int) -> None:
    """All four known Hue Tap SrcIDs match."""
    device = GPDevice(source_id=src_id, device_id=0x02, frame_counter=0)
    assert device.security_level is SecurityLevel.NoSecurity
    assert device.security_key_type is SecurityKeyType.NoKey
    assert match_hue_tap(device)


def test_match_rejects_encrypted_device() -> None:
    """A device with FullFrameCounterAndMIC (Busch-Jaeger style) is not a Tap."""
    device = GPDevice(
        source_id=0x0040F4E4,
        device_id=0x02,
        frame_counter=0,
        security_level=SecurityLevel.FullFrameCounterAndMIC,
    )
    assert not match_hue_tap(device)


def test_match_rejects_foreign_src_id() -> None:
    """A SrcID outside the 0x0040xxxx block is not a Tap (e.g. Busch-Jaeger)."""
    device = GPDevice(source_id=0x0171F886, device_id=0x02, frame_counter=0)
    assert not match_hue_tap(device)


# --- DEVICE_AUTOMATION_TRIGGERS ----------------------------------------------


def test_triggers_cover_all_four_buttons() -> None:
    """Exactly four PRESSED entries, one per button."""
    assert len(DEVICE_AUTOMATION_TRIGGERS) == 4
    for button, _ in EXPECTED_TRIGGERS:
        assert (PRESSED, button) in DEVICE_AUTOMATION_TRIGGERS


@pytest.mark.parametrize("button,expected_cmd", EXPECTED_TRIGGERS)
def test_trigger_command_ids(button: str, expected_cmd: int) -> None:
    """Each button maps to the Z2M-verified command ID."""
    entry = DEVICE_AUTOMATION_TRIGGERS[(PRESSED, button)]
    assert entry[PARAMS][COMMAND_ID] == expected_cmd
