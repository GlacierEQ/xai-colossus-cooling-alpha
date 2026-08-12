from __future__ import annotations

import json
import subprocess
import sys


def test_direct_operator_exercises_pass_and_refuse_paths() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/operate.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = json.loads(result.stdout)
    assert receipt["result"] == "PASS"
    assert receipt["nominal"]["ok"] is True
    assert receipt["constrained"]["ok"] is False
