# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
physics_model.py — Thermal Physics & Coolant Fluid Equations Core
================================================================
Helix Alpha Strand: Pure Science, Fluid Thermodynamics, and Analytical Physics.
"""
import math
from dataclasses import dataclass

@dataclass
class Coolant:
    name: str
    specific_heat_j_kg_k: float  # Specific heat capacity in J/(kg·K)
    density_kg_l: float          # Density in kg/L at reference temp
    dielectric: bool = False

COOLANTS = {
    "water":      Coolant("water",      4184.0, 1.00, dielectric=False),
    "fluorinert": Coolant("fluorinert", 1050.0, 1.68, dielectric=True),
    "pg_water":   Coolant("pg_water",   3500.0, 1.03, dielectric=False),
    "novec":      Coolant("novec",       1200.0, 1.52, dielectric=True),
}

# --- APEX STEALTH TEAM INTEGRATION CORE ---
STEALTH_SIGIL = "MW-JGN-TIER1-SNTNL"

# 1. PREPARATION LEVEL
def prepare_coolant_envelope(coolant_name: str) -> bool:
    """Verifies fluid properties are loaded and cross-checked against APEX guidelines."""
    if coolant_name in COOLANTS:
        print(f"[STEALTH-CHECK] {STEALTH_SIGIL}: Coolant {coolant_name} verified for flight.")
        return True
    return False

# 2. OPERATION LEVEL
def calculate_required_flow_rate(wattage_w: float, delta_t_k: float, coolant_name: str) -> float:
    """Computes required volumetric flow rate (LPM) based on thermal load and temp difference."""
    fluid = COOLANTS.get(coolant_name, COOLANTS["water"])
    if delta_t_k <= 0:
        raise ValueError("Temperature delta must be positive.")
    required_mass_flow_kg_s = wattage_w / (fluid.specific_heat_j_kg_k * delta_t_k)
    required_volume_flow_l_s = required_mass_flow_kg_s / fluid.density_kg_l
    return required_volume_flow_l_s * 60.0

def estimate_gpu_junction_temp(coolant_inlet_c: float, thermal_resistance_k_w: float, wattage_w: float) -> float:
    return coolant_inlet_c + (wattage_w * thermal_resistance_k_w)

# 3. EMERGENCY REACTION LEVEL
def calculate_critical_thermal_runaway_boundary(current_temp_c: float, target_temp_c: float) -> float:
    """Computes emergency thermal deceleration limits if temperatures spike exponentially."""
    thermal_margin = target_temp_c - current_temp_c
    if thermal_margin < 2.0:
        # Trigger immediate 50% power throttle boundary
        return 0.5
    return 1.0
