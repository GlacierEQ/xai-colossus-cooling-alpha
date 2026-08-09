# Cooling Alpha — Thermal Envelope Evaluator

A small, independently testable thermal-envelope component for compute-infrastructure scenario modeling.

> **Independent portfolio project.** This repository is not affiliated with, endorsed by, employed by, or deployed at xAI. It does not claim proprietary Colossus data, facility access, live telemetry, or hardware control.

## Recruiter view

The canonical public implementation is [`src/thermal_spec.py`](src/thermal_spec.py). Given a modeled inlet temperature, allowed temperature rise, and measured outlet temperature, it evaluates whether the outlet remains inside a bounded thermal envelope and reports remaining margin.

Current verified behavior:

- computes a design outlet from `inlet_c + max_delta_t`;
- caps the accepted outlet against the local throttle constant;
- reports pass/fail and thermal margin;
- carries `design_mw` as scenario context but does **not** currently derive flow or cooling capacity from it;
- performs no network queries, telemetry reads, or external actions.

This is an envelope evaluator, not a datacenter cooling controller or CFD/digital-twin proof.

## Engineering boundary

```text
modeled inlet + allowed delta + observed/scenario outlet
                    │
                    ▼
          src/thermal_spec.py
                    │
                    ▼
      pass/fail + margin + design outlet
```

Canonical proof paths:

| Path | Role |
|---|---|
| `src/thermal_spec.py` | bounded thermal-envelope evaluator |
| `tests/test_thermal_spec.py` | deterministic nominal/hot-path checks |
| `scripts/verify_public_core.py` | receipt-producing public verifier |
| `.github/workflows/ci.yml` | exact-branch Python truth gate |

The repository also contains older root-level physics, PINN, telemetry-named, integrity, and experimental surfaces. They are preserved as historical/experimental material and are **not** promoted by this public contract unless separately verified.

## Alpha / Omega relationship

Cooling Alpha and [`xai-colossus-cooling-omega`](https://github.com/GlacierEQ/xai-colossus-cooling-omega) are an architectural pair: Alpha evaluates the thermal requirement/envelope; Omega models a stateful flow response. The repositories do not currently establish a live cross-repository runtime integration or physical actuator connection.

## Verify

```bash
python tests/test_thermal_spec.py
python scripts/verify_public_core.py
```

Successful verification establishes only the local deterministic model/test contract on the checked source revision.

## Machine contract

```yaml
schema: glaciereq.component-surface.v1
repository: GlacierEQ/xai-colossus-cooling-alpha
canonical_branch: master
role: SPECIALIST_COMPONENT
capability: thermal_envelope_evaluator
evidence_level: TEST
external_queries: 0
external_actions: 0
live_telemetry: false
hardware_actuation: false
runtime_pairing_with_omega: false
company_affiliation_claim: false
```

## Nonclaims

This repository does not establish xAI affiliation, proprietary access, production deployment, live Colossus telemetry, pump/valve/chiller actuation, measured PUE or efficiency, validation at a specific GPU/MW/rack scale, or physical-system safety certification.
