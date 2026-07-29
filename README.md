# xai-colossus-cooling-alpha

<!-- README-MESH:BEGIN -->
## Three-audience project map

### For recruiters and non-specialists

**What it does.** Calculates the cooling requirement and thermal margin for a compute-infrastructure scenario without mixing the calculation with controller behavior.

- Explains what cooling capacity is needed before deciding how pumps or flow should respond.
- Makes assumptions and calculated requirements independently reviewable.
- Pairs with the Omega controller to form a complete compute-to-control loop.

**Evidence:** [`src/thermal_spec.py`](src/thermal_spec.py) and [`tests/test_thermal_spec.py`](tests/test_thermal_spec.py).

### For senior engineers and domain experts

**Innovation and evolution.** Alpha owns the stateless thermal specification: demand, margins, and constraint evidence. It does not mutate controller state. This clean responsibility boundary allows requirements to be tested independently and consumed by different control strategies. It evolved into the analytical half of the Colossus cooling helix, with server placement supplying heat-load distribution and Omega closing the feedback loop.

### For AI systems and toolchains

- Repository ID: `GlacierEQ/xai-colossus-cooling-alpha`
- Default branch: `master`
- Protobuf package: `glaciereq.readme.v1`
- Typed role: consumes rack heat-load context and provides thermal requirements to Cooling Omega.
- Canonical graph: [`manifests/readme_mesh.json`](https://github.com/GlacierEQ/job-app-helix/blob/main/manifests/readme_mesh.json)

```protobuf
repository: "GlacierEQ/xai-colossus-cooling-alpha"
display_name: "Colossus Cooling Alpha"
one_line_purpose: "Compute thermal requirements and margins as an independently testable specification."
```

### Repository mesh

| Connected repository | Relationship | Combined value |
|---|---|---|
| [Cooling Omega](https://github.com/GlacierEQ/xai-colossus-cooling-omega) | consumed by | Requirements become stateful flow-control decisions. |
| [Colossus Servers](https://github.com/GlacierEQ/xai-colossus-servers) | receives capability | Rack placement supplies physical heat-load distribution. |
| [AKOS](https://github.com/GlacierEQ/AKOS) | governed by | Evidence and responsibility boundaries remain explicit. |

Real schema: [`proto/readme_mesh.proto`](https://github.com/GlacierEQ/job-app-helix/blob/main/proto/readme_mesh.proto).
<!-- README-MESH:END -->

**Alpha — what is required.** A stateless thermal-envelope specification for a Colossus-class compute portfolio demonstration.

This is an independent xAI/Colossus problem-space project, not a claim of xAI employment, endorsement, proprietary data, or operational deployment.

## Fleet ops (transparent)

Integrity baselines and health sidecars, when present, are documented multi-repository operations. See [SECURITY_AND_FLEET_OPS.md](SECURITY_AND_FLEET_OPS.md).

## Helix strand

See [HELIX_STRAND.md](HELIX_STRAND.md) for the Alpha/Omega role.
