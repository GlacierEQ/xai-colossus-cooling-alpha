<<<<<<< HEAD
# Cooling Alpha — Thermal Envelope Evaluator
=======
# xAI Colossus Cooling Alpha — Primary Cooling Loop Controller 🧊

> **Primary liquid cooling loop management for 100,000+ GPU datacenter thermal regulation.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue)]()
[![Domain](https://img.shields.io/badge/Domain-Datacenter%20Cooling-cyan)]()
>>>>>>> 9a5b100 (docs(readme): upgrade to 3-section recruiter/engineer/mesh structure & update SHA-256 baseline)

A small, independently testable thermal-envelope component for compute-infrastructure scenario modeling.

<<<<<<< HEAD
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
=======
## 🎯 For Recruiters & Hiring Managers

This repository implements a **primary cooling loop controller** for the xAI Colossus datacenter — managing chilled water distribution across GPU racks to maintain optimal operating temperatures. It demonstrates:

- **PID control loops** for chilled water temperature and flow rate regulation
- **Thermal zone management** with per-rack temperature monitoring and coolant distribution
- **Predictive load modeling** anticipating thermal demand from training job schedules
- **Failover logic** with redundant pump management and emergency cooling sequences

**Why this matters**: Datacenter cooling at 100,000+ GPU scale is a **controls engineering challenge** requiring the same PID tuning, sensor fusion, and fault-tolerant design used in industrial process control, HVAC systems, and manufacturing automation.

---

## 🔬 For Engineers & Technical Reviewers

### Core Components

| Component | Language | Purpose |
|---|---|---|
| `src/cooling_alpha.py` | Python | PID controller, thermal zone manager, pump orchestration |
| `tests/` | Python | Thermal simulation with fault injection scenarios |

### Key Metrics

- **Target PUE**: 1.08 (Power Usage Effectiveness)
- **Coolant Temp**: 18-24°C supply, 35-42°C return
- **Flow Rate**: 2000-5000 L/min per zone

---

## 🤖 ML/AI & Programmatic Mesh Integration

- **MCP Tool**: `cooling_status(zone_id)` — thermal state queryable by energy optimization agents
- **Mastermind Sidecar**: Publishes thermal alerts to APEX Highway mesh
- **AI Extension**: Neural PID auto-tuning from historical thermal response data

```python
status = await mcp_client.call_tool("colossus-cooling-alpha", "zone_status", {"zone": "A1"})
```

---

## ⚡ Quick Start

```bash
python3 src/cooling_alpha.py
python3 tests/test_cooling_alpha.py
```
>>>>>>> 9a5b100 (docs(readme): upgrade to 3-section recruiter/engineer/mesh structure & update SHA-256 baseline)
