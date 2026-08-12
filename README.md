# Cooling Alpha — Thermal Requirement Evaluator

**Installable, deterministic steady-state cooling-requirement and thermal-envelope software for local compute-infrastructure scenarios.**

> **Independent portfolio project.** This repository is not affiliated with, endorsed by, employed by, or deployed at xAI. It does not establish proprietary Colossus data, facility access, live telemetry, pump/valve/chiller actuation, or physical-system safety authority.

Evidence state: `LOCAL_STEADY_STATE_COOLING_REQUIREMENT_MODEL_NOT_XAI_FACILITY_CONTROL`

## What the product does

The canonical product is `src/thermal_spec.py`. It turns a modeled heat load and coolant temperature-rise envelope into a transparent steady-state requirement:

- validates finite, positive design inputs and fails closed on malformed scenarios;
- computes design outlet temperature from inlet plus allowed temperature rise;
- uses the steady-state sensible-heat relation `Q = m_dot * cp * delta_T` to derive required coolant mass flow;
- converts mass flow to volumetric flow using an explicit reference coolant density;
- evaluates measured/scenario outlet temperature against the bounded envelope;
- when an observed/scenario flow is supplied, estimates modeled heat removal and reports capacity margin/shortfall;
- emits deterministic machine-readable receipts and performs zero external queries or actions.

The default `water_reference` properties are **illustrative engineering reference constants**, not facility-fluid certification. A different coolant requires explicit properties rather than a silent fallback.

## Install and run

```bash
python -m pip install .
cooling-alpha-evaluate
cooling-alpha-evaluate --inlet-c 25 --max-delta-t 15 --design-mw 50 --measured-outlet-c 38 --observed-flow-lpm 60000
python scripts/operate.py
```

## Core API

```python
from thermal_spec import Envelope, within_spec, required_volume_flow_lpm

env = Envelope(inlet_c=25.0, max_delta_t=15.0, design_mw=50.0)
print(required_volume_flow_lpm(env))
print(within_spec(env, measured_outlet_c=38.0, observed_flow_lpm=60000.0))
```

The result separates thermal-envelope status from optional modeled flow/capacity status. It does not issue hardware commands.

## Alpha / Omega boundary

Cooling Alpha owns the **requirement/envelope calculation**. `xai-colossus-cooling-omega` may consume such a requirement as an architectural peer, but this repository does not claim a live cross-repository runtime, actuator path, or shared production control loop.

## Historical material

Older root-level `physics_model.py`, `pinn_digital_twin.py`, integrity/watchdog files, and prior promotion receipts are preserved for lineage. They are **not canonical runtime authority** and are not imported by the installed product. In particular, old PID, emergency-mitigation, APEX/MCP, 100,000+ GPU, PUE, flow-range, and neural-controller language is not evidence for this repository.

The previous local HMAC `PROMOTED` mechanism used a repository-known reference secret and is retired. Cryptographic ceremony with a public secret is not independent promotion authority. Terminal status now comes only from exact-head repository behavior and a source-bound completion receipt.

## Verify

```bash
python -m pytest -q
python scripts/verify_public_core.py
```

CI additionally builds/installs the wheel, executes the installed CLI and direct operator, rejects merge-conflict markers and legacy unsupported public claims, and requires every crystallization capability to be `WORKING` with an empty material gap matrix.

## Evidence boundary

This repository does **not** establish:

- xAI affiliation, employment, endorsement, proprietary access, or facility data;
- a 100,000+ GPU cooling controller or any particular rack/MW deployment scale;
- measured PUE, production efficiency, or validated facility flow ranges;
- live telemetry, sensor fusion, PID control, pump/valve/chiller control, emergency cooling, or hardware actuation;
- CFD/digital-twin validation, calibrated transient behavior, or physical-system safety certification;
- live MCP, APEX, AKOS, Mastermind, or agent-mesh connectivity;
- production deployment or production-scale reliability.

The target is a complete, inspectable local **thermal requirement evaluator**, not a fictional datacenter control system.
