from __future__ import annotations

import math
import pytest

from thermal_spec import (
    Envelope,
    modeled_heat_removal_mw,
    required_mass_flow_kg_s,
    required_volume_flow_lpm,
    within_spec,
)


def test_nominal_envelope_uses_design_heat_load() -> None:
    env = Envelope(25.0, 15.0, 50.0)
    result = within_spec(env, 38.0, 60_000.0)
    assert result["ok"] is True
    assert result["design_heat_load_mw"] == 50.0
    assert result["required_mass_flow_kg_s"] > 0
    assert result["required_flow_lpm"] > 0
    assert result["capacity_margin_mw"] > 0
    assert len(result["digest"]) == 64


def test_design_load_materially_changes_required_flow() -> None:
    low = required_volume_flow_lpm(Envelope(25.0, 15.0, 25.0))
    high = required_volume_flow_lpm(Envelope(25.0, 15.0, 50.0))
    assert high == pytest.approx(low * 2.0)


def test_low_flow_and_hot_outlet_fail_closed() -> None:
    result = within_spec(Envelope(25.0, 15.0, 50.0), 47.0, 25_000.0)
    assert result["ok"] is False
    assert "OUTLET_LIMIT_EXCEEDED" in result["reasons"]
    assert "FLOW_BELOW_DESIGN_REQUIREMENT" in result["reasons"]
    assert "MODELED_HEAT_REMOVAL_SHORTFALL" in result["reasons"]


def test_modeled_heat_removal_scales_with_flow() -> None:
    one = modeled_heat_removal_mw(10_000.0, 10.0)
    two = modeled_heat_removal_mw(20_000.0, 10.0)
    assert two == pytest.approx(one * 2.0)


@pytest.mark.parametrize(
    "env",
    [
        Envelope(25.0, 0.0, 50.0),
        Envelope(25.0, 15.0, 0.0),
        Envelope(float("nan"), 15.0, 50.0),
        Envelope(25.0, float("inf"), 50.0),
        Envelope(25.0, 15.0, 50.0, coolant="unknown"),
    ],
)
def test_invalid_envelopes_refuse(env: Envelope) -> None:
    with pytest.raises(ValueError):
        required_mass_flow_kg_s(env)
