# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from physics_model import calculate_critical_thermal_runaway_boundary
def test_emergency():
    boundary = calculate_critical_thermal_runaway_boundary(82.5, 83.0)
    assert boundary == 0.2
    print("  [PASS] Emergency critical thermal runaway boundaries checked.")
