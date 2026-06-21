# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
import os
import sys
import time

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physics_model import calculate_required_flow_rate, calculate_transient_thermal_inertia
from zone_model import DatacenterThermalModel

def test_cooling_calculations():
    print("[TEST] Running Cooling Physics calculations...")
    t0 = time.perf_counter()
    
    # 1. Test flow rate calculation
    flow_lpm = calculate_required_flow_rate(1000000.0, 15.0, "novec")
    assert flow_lpm > 0, "Flow rate should be positive"
    print(f"  - Verified 1MW Novec cooling flow rate: {flow_lpm:.2f} LPM")
    
    # 2. Test transient thermal inertia
    lag = calculate_transient_thermal_inertia("novec", 2.5, flow_lpm)
    assert lag > 0, "Lag time must be positive"
    print(f"  - Verified Novec transient thermal inertia lag: {lag:.4f} seconds")
    
    # 3. Test Thermal Zone models
    model = DatacenterThermalModel(baseline_ambient_c=22.0)
    model.add_zone("A", 10, 35.0, 1.5)
    model.add_zone("B", 10, 45.0, 3.0)
    assert model.get_total_heat_load_kw() == 800.0
    assert model.isolate_hottest_zone() == "B"
    print(f"  - Verified Datacenter thermal zones. Max load zone: {model.isolate_hottest_zone()}")
    
    duration_ms = (time.perf_counter() - t0) * 1000.0
    print(f"[TEST-METRICS] Status=SUCCESS Latency={duration_ms:.3f}ms")

if __name__ == '__main__':
    test_cooling_calculations()
