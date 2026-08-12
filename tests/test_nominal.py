from thermal_spec import Envelope, required_volume_flow_lpm, within_spec


def test_nominal_requirement_is_positive_and_passes_with_capacity() -> None:
    env = Envelope(25.0, 15.0, 0.5)
    required = required_volume_flow_lpm(env)
    assert required > 0
    result = within_spec(env, 35.0, required * 1.6)
    assert result["ok"] is True
    assert result["external_queries"] == 0
    assert result["external_actions"] == 0
