from thermal_spec import Envelope, within_spec


def test_thermal_overrun_is_a_refusal_not_an_emergency_actuation() -> None:
    result = within_spec(Envelope(25.0, 15.0, 5.0), 90.0, 1_000.0)
    assert result["ok"] is False
    assert "OUTLET_LIMIT_EXCEEDED" in result["reasons"]
    assert result["hardware_actuation"] is False
    assert result["external_actions"] == 0
