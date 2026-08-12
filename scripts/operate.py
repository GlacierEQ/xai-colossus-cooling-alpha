#!/usr/bin/env python3
"""Execute Cooling Alpha's actual bounded thermal requirement mechanism."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from thermal_spec import EVIDENCE_STATE, Envelope, within_spec  # noqa: E402


def main() -> int:
    nominal = within_spec(Envelope(25.0, 15.0, 50.0), 38.0, 60_000.0)
    constrained = within_spec(Envelope(25.0, 15.0, 50.0), 47.0, 25_000.0)
    receipt = {
        "schema": "glaciereq.cooling-alpha.operability.v1",
        "evidence_state": EVIDENCE_STATE,
        "nominal": nominal,
        "constrained": constrained,
        "result": "PASS" if nominal["ok"] and not constrained["ok"] else "FAIL",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
