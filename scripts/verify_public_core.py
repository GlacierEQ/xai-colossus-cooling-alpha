#!/usr/bin/env python3
"""Fail-closed verification for Cooling Alpha's public/product truth surface."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from thermal_spec import EVIDENCE_STATE, Envelope, required_volume_flow_lpm, within_spec  # noqa: E402

FORBIDDEN_README = (
    "<<<<<<<",
    "=======",
    ">>>>>>>",
    "100,000+ GPU",
    "primary cooling loop controller",
    "PID control loops",
    "Target PUE",
    "2000-5000 L/min",
    "Neural PID",
    "cooling_status(zone_id)",
)


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in FORBIDDEN_README:
        if token.lower() in readme.lower():
            raise SystemExit(f"forbidden_public_claim:{token}")

    capabilities = json.loads((ROOT / "machine" / "capabilities.json").read_text())
    target = json.loads((ROOT / "machine" / "target-contract.json").read_text())
    excellence = json.loads((ROOT / "machine" / "excellence-state.json").read_text())
    promotion = json.loads((ROOT / "machine" / "promotion_authority.json").read_text())
    gaps = json.loads((ROOT / "machine" / "crystallization" / "gap-matrix.json").read_text())

    if capabilities["evidence_state"] != EVIDENCE_STATE:
        raise SystemExit("capability_evidence_state_mismatch")
    if target["evidence_state"] != EVIDENCE_STATE:
        raise SystemExit("target_evidence_state_mismatch")
    if excellence["state"] != "FUNCTIONAL_CRYSTALLIZATION_CANDIDATE":
        raise SystemExit("false_terminal_state")
    if promotion["status"] != "RETIRED":
        raise SystemExit("legacy_local_promotion_not_retired")
    if gaps["gaps"] != []:
        raise SystemExit("material_gaps_remain")

    env = Envelope(25.0, 15.0, 50.0)
    nominal = within_spec(env, 38.0, 60_000.0)
    constrained = within_spec(env, 47.0, 25_000.0)
    if not nominal["ok"] or constrained["ok"]:
        raise SystemExit("scenario_contract_failed")
    if required_volume_flow_lpm(env) <= 0:
        raise SystemExit("flow_requirement_not_materialized")

    source_sha = hashlib.sha256((ROOT / "src" / "thermal_spec.py").read_bytes()).hexdigest()
    receipt = {
        "schema": "glaciereq.cooling-alpha.public-proof.v2",
        "evidence_state": EVIDENCE_STATE,
        "source_sha256": source_sha,
        "required_flow_lpm": nominal["required_flow_lpm"],
        "nominal_digest": nominal["digest"],
        "constrained_digest": constrained["digest"],
        "external_queries": 0,
        "external_actions": 0,
        "hardware_actuation": False,
        "runtime_pairing_with_omega": False,
        "legacy_promotion_authority": "RETIRED",
        "result": "PASS",
    }
    out = ROOT / "artifacts" / "public-core" / "verification.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
