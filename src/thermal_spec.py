#!/usr/bin/env python3
"""Bounded steady-state cooling requirement model for local scenarios.

This module performs transparent sensible-heat arithmetic only. It does not
read telemetry, actuate hardware, or establish facility-specific fluid data.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any

EVIDENCE_STATE = "LOCAL_STEADY_STATE_COOLING_REQUIREMENT_MODEL_NOT_XAI_FACILITY_CONTROL"
THROTTLE_C = 83.0
TARGET_C = 42.0


@dataclass(frozen=True)
class Coolant:
    name: str
    specific_heat_j_kg_k: float
    density_kg_l: float


# Illustrative water reference, not a certified facility-fluid specification.
WATER_REFERENCE = Coolant(
    name="water_reference",
    specific_heat_j_kg_k=4184.0,
    density_kg_l=0.997,
)
COOLANTS = {WATER_REFERENCE.name: WATER_REFERENCE}


@dataclass(frozen=True)
class Envelope:
    inlet_c: float
    max_delta_t: float
    design_mw: float
    coolant: str = WATER_REFERENCE.name
    outlet_tolerance_c: float = 5.0


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_must_be_number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name}_must_be_finite")
    return value


def validate_envelope(env: Envelope) -> Coolant:
    inlet = _finite("inlet_c", env.inlet_c)
    delta = _finite("max_delta_t", env.max_delta_t)
    load = _finite("design_mw", env.design_mw)
    tolerance = _finite("outlet_tolerance_c", env.outlet_tolerance_c)
    if delta <= 0:
        raise ValueError("max_delta_t_must_be_positive")
    if load <= 0:
        raise ValueError("design_mw_must_be_positive")
    if tolerance < 0:
        raise ValueError("outlet_tolerance_c_must_be_non_negative")
    if env.coolant not in COOLANTS:
        raise ValueError(f"unknown_coolant:{env.coolant}")
    coolant = COOLANTS[env.coolant]
    _finite("specific_heat_j_kg_k", coolant.specific_heat_j_kg_k)
    _finite("density_kg_l", coolant.density_kg_l)
    if coolant.specific_heat_j_kg_k <= 0 or coolant.density_kg_l <= 0:
        raise ValueError("coolant_properties_must_be_positive")
    # Rebind locals through validation so callers cannot smuggle NaN while
    # preserving the frozen dataclass API.
    _ = inlet
    return coolant


def outlet(env: Envelope) -> float:
    validate_envelope(env)
    return float(env.inlet_c) + float(env.max_delta_t)


def outlet_limit_c(env: Envelope) -> float:
    validate_envelope(env)
    return min(THROTTLE_C, outlet(env) + float(env.outlet_tolerance_c))


def required_mass_flow_kg_s(env: Envelope) -> float:
    coolant = validate_envelope(env)
    heat_w = float(env.design_mw) * 1_000_000.0
    return heat_w / (coolant.specific_heat_j_kg_k * float(env.max_delta_t))


def required_volume_flow_lpm(env: Envelope) -> float:
    coolant = validate_envelope(env)
    return required_mass_flow_kg_s(env) / coolant.density_kg_l * 60.0


def modeled_heat_removal_mw(
    flow_lpm: float,
    delta_t_c: float,
    coolant: Coolant = WATER_REFERENCE,
) -> float:
    flow = _finite("flow_lpm", flow_lpm)
    delta = _finite("delta_t_c", delta_t_c)
    if flow < 0:
        raise ValueError("flow_lpm_must_be_non_negative")
    if delta < 0:
        raise ValueError("delta_t_c_must_be_non_negative")
    if coolant.specific_heat_j_kg_k <= 0 or coolant.density_kg_l <= 0:
        raise ValueError("coolant_properties_must_be_positive")
    mass_flow_kg_s = flow * coolant.density_kg_l / 60.0
    return mass_flow_kg_s * coolant.specific_heat_j_kg_k * delta / 1_000_000.0


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def within_spec(
    env: Envelope,
    measured_outlet_c: float,
    observed_flow_lpm: float | None = None,
) -> dict[str, Any]:
    coolant = validate_envelope(env)
    measured = _finite("measured_outlet_c", measured_outlet_c)
    limit = outlet_limit_c(env)
    design_outlet = outlet(env)
    reasons: list[str] = []

    if measured < float(env.inlet_c):
        reasons.append("OUTLET_BELOW_INLET")
    if measured > limit:
        reasons.append("OUTLET_LIMIT_EXCEEDED")

    required_flow = required_volume_flow_lpm(env)
    observed_delta = max(0.0, measured - float(env.inlet_c))
    modeled_capacity = None
    capacity_margin = None
    flow_margin = None

    if observed_flow_lpm is not None:
        flow = _finite("observed_flow_lpm", observed_flow_lpm)
        if flow < 0:
            raise ValueError("observed_flow_lpm_must_be_non_negative")
        flow_margin = flow - required_flow
        modeled_capacity = modeled_heat_removal_mw(flow, observed_delta, coolant)
        capacity_margin = modeled_capacity - float(env.design_mw)
        if flow + 1e-9 < required_flow:
            reasons.append("FLOW_BELOW_DESIGN_REQUIREMENT")
        if modeled_capacity + 1e-9 < float(env.design_mw):
            reasons.append("MODELED_HEAT_REMOVAL_SHORTFALL")

    result: dict[str, Any] = {
        "schema": "glaciereq.cooling-alpha.evaluation.v1",
        "evidence_state": EVIDENCE_STATE,
        "ok": not reasons,
        "reasons": reasons,
        "inlet_c": round(float(env.inlet_c), 6),
        "measured_outlet_c": round(measured, 6),
        "observed_delta_t_c": round(observed_delta, 6),
        "design_outlet_c": round(design_outlet, 6),
        "outlet_limit_c": round(limit, 6),
        "thermal_margin_c": round(limit - measured, 6),
        "design_heat_load_mw": round(float(env.design_mw), 6),
        "coolant": coolant.name,
        "required_mass_flow_kg_s": round(required_mass_flow_kg_s(env), 6),
        "required_flow_lpm": round(required_flow, 6),
        "observed_flow_lpm": None if observed_flow_lpm is None else round(float(observed_flow_lpm), 6),
        "flow_margin_lpm": None if flow_margin is None else round(flow_margin, 6),
        "modeled_heat_removal_mw": None if modeled_capacity is None else round(modeled_capacity, 6),
        "capacity_margin_mw": None if capacity_margin is None else round(capacity_margin, 6),
        "target_c": TARGET_C,
        "strand": "alpha",
        "external_queries": 0,
        "external_actions": 0,
        "hardware_actuation": False,
    }
    result["digest"] = _digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(within_spec(Envelope(25, 15, 50), 38, 60_000), indent=2, sort_keys=True))
