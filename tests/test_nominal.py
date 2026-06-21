# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physics_model import calculate_required_flow_rate, estimate_gpu_junction_temp
from pinn_digital_twin import PINNDigitalTwin

def test_nominal():
    # Verify nominal flow equations
    flow = calculate_required_flow_rate(500000.0, 10.0, "pg_water")
    assert flow > 0
    temp = estimate_gpu_junction_temp(35.0, 0.04, 800.0)
    assert temp == 67.0
    
    # Verify PINN Digital Twin calculations
    twin = PINNDigitalTwin(manifest={"critical_temp_c": 85.0})
    result = twin.validate({"zone_id": "A", "temp_celsius": 68.0, "power_draw_kw": 50000.0, "cooling_flow_lpm": 500.0})
    assert "confidence" in result
    print("  [PASS] Nominal calculation and PINN Twin verifications successful.")
