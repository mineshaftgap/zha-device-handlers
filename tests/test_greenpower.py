"""Tests for the Green Power quirks."""

from __future__ import annotations

import pytest
from zigpy.quirks import get_green_power_quirk
from zigpy.zgp import GPDevice, SecurityKeyType, SecurityLevel

from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    COMMAND_ID,
    PARAMS,
    PRESSED,
)
from zhaquirks.greenpower.huetap import HueTap

# All four SrcIDs confirmed on real Taps (2026-06-09 via Z2M)
HUE_TAP_SRC_IDS = [0x00402725, 0x0040EE88, 0x00404C79, 0x0040F4E4]

# Expected (button, command_id) - cross-checks trigger map against Z2M decode
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
    assert HueTap.match(device)


def test_match_accepts_encrypted_device() -> None:
    """A Hue Tap commissioned with FullFrameCounterAndMIC must still be matched.

    Real-hardware finding (2026-06-11): the physical Hue Tap spare on lxc-ha-dev
    was commissioned with security_level=FullFrameCounterAndMIC / NetworkKey.
    Security is a deployment detail; the 0x0040xxxx SrcID block is the identifier.
    """
    device = GPDevice(
        source_id=0x0040F4E4,
        device_id=0x02,
        frame_counter=0,
        security_level=SecurityLevel.FullFrameCounterAndMIC,
    )
    assert HueTap.match(device)


def test_match_rejects_foreign_src_id() -> None:
    """A SrcID outside the 0x0040xxxx block is not a Tap (e.g. Busch-Jaeger)."""
    device = GPDevice(source_id=0x0171F886, device_id=0x02, frame_counter=0)
    assert not HueTap.match(device)


# --- HueTap.device_automation_triggers ----------------------------------------------


def test_triggers_cover_all_four_buttons() -> None:
    """Exactly four PRESSED entries, one per button."""
    assert len(HueTap.device_automation_triggers) == 4
    for button, _ in EXPECTED_TRIGGERS:
        assert (PRESSED, button) in HueTap.device_automation_triggers


@pytest.mark.parametrize("button,expected_cmd", EXPECTED_TRIGGERS)
def test_trigger_command_ids(button: str, expected_cmd: int) -> None:
    """Each button maps to the Z2M-verified command ID."""
    entry = HueTap.device_automation_triggers[(PRESSED, button)]
    assert entry[PARAMS][COMMAND_ID] == expected_cmd


# --- Registry resolution (P1 acceptance) ------------------------------------


@pytest.mark.parametrize("src_id", HUE_TAP_SRC_IDS)
def test_registry_resolves_hue_tap(src_id: int) -> None:
    """GP quirk registry returns HueTap for all four known Tap SrcIDs."""
    device = GPDevice(source_id=src_id, device_id=0x02, frame_counter=0)
    assert get_green_power_quirk(device) is HueTap


def test_registry_no_match_for_foreign_src_id() -> None:
    """A SrcID outside the Hue Tap block does not resolve to HueTap."""
    device = GPDevice(source_id=0x0171F886, device_id=0x02, frame_counter=0)
    result = get_green_power_quirk(device)
    assert result is not HueTap
