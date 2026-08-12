from thermal_spec import Envelope, within_spec


def test_receipt_is_deterministic_for_same_scenario() -> None:
    env = Envelope(25.0, 15.0, 50.0)
    first = within_spec(env, 38.0, 60_000.0)
    second = within_spec(env, 38.0, 60_000.0)
    assert first == second
    assert first["digest"] == second["digest"]
