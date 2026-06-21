# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physics_model import calculate_required_flow_rate, estimate_gpu_junction_temp
def test_nominal():
    flow = calculate_required_flow_rate(500000.0, 10.0, "pg_water")
    assert flow > 0
    temp = estimate_gpu_junction_temp(35.0, 0.04, 800.0)
    assert temp == 67.0
    print("  [PASS] Nominal calculation verifications successful.")
