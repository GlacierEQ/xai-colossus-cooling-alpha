from __future__ import annotations

import pytest

from thermal_spec import Envelope, modeled_heat_removal_mw, within_spec


def test_non_finite_measurement_refuses() -> None:
    with pytest.raises(ValueError, match="measured_outlet_c_must_be_finite"):
        within_spec(Envelope(25.0, 15.0, 50.0), float("nan"))


def test_negative_flow_refuses() -> None:
    with pytest.raises(ValueError, match="observed_flow_lpm_must_be_non_negative"):
        within_spec(Envelope(25.0, 15.0, 50.0), 38.0, -1.0)


def test_negative_delta_heat_removal_refuses() -> None:
    with pytest.raises(ValueError, match="delta_t_c_must_be_non_negative"):
        modeled_heat_removal_mw(1000.0, -1.0)


def test_below_inlet_is_explicit_failure() -> None:
    result = within_spec(Envelope(25.0, 15.0, 5.0), 20.0)
    assert result["ok"] is False
    assert result["reasons"] == ["OUTLET_BELOW_INLET"]
