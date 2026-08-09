#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from thermal_spec import Envelope, within_spec  # noqa: E402


def sha256_json(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    test = subprocess.run(
        [sys.executable, "tests/test_thermal_spec.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if test.returncode != 0:
        raise SystemExit(test.stderr or test.stdout or "thermal-spec test failed")

    scenario = within_spec(Envelope(25.0, 10.0, 40.0), 32.0)
    if not scenario["ok"] or scenario["margin_c"] <= 0:
        raise SystemExit("bounded nominal scenario did not remain inside the envelope")

    receipt = {
        "schema": "glaciereq.cooling-alpha.public-proof.v1",
        "capability": "thermal_envelope_evaluator",
        "evidence_level": "TEST",
        "scenario": scenario,
        "scenario_context_design_mw": 40.0,
        "design_mw_used_in_current_calculation": False,
        "external_queries": 0,
        "external_actions": 0,
        "live_telemetry": False,
        "hardware_actuation": False,
        "runtime_pairing_with_omega": False,
        "test_returncode": test.returncode,
    }
    receipt["receipt_sha256"] = sha256_json(receipt)
    out = ROOT / "artifacts" / "public-core"
    out.mkdir(parents=True, exist_ok=True)
    (out / "verification.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
