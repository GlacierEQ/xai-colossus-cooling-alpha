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

# High-accuracy thermal fluid specs
COOLANTS = {
    "water":      Coolant("water",      4184.0, 1.00, dielectric=False),
    "fluorinert": Coolant("fluorinert", 1050.0, 1.68, dielectric=True),   # 3M FC-72
    "pg_water":   Coolant("pg_water",   3500.0, 1.03, dielectric=False),  # PG 25/75
    "novec":      Coolant("novec",       1200.0, 1.52, dielectric=True),   # 3M Novec 7100
}

def calculate_required_flow_rate(wattage_w: float, delta_t_k: float, coolant_name: str) -> float:
    """
    Computes required volumetric flow rate (LPM) based on thermal load and temp difference.
    Equation: Q = P / (m_dot * C_p) => Flow (LPM) = (P_w / (C_p * delta_T * density)) * 60
    """
    fluid = COOLANTS.get(coolant_name, COOLANTS["water"])
    # C_p is in J/kg*K. mass_flow = P / (C_p * delta_t)
    if delta_t_k <= 0:
        raise ValueError("Temperature delta must be positive.")
    
    required_mass_flow_kg_s = wattage_w / (fluid.specific_heat_j_kg_k * delta_t_k)
    required_volume_flow_l_s = required_mass_flow_kg_s / fluid.density_kg_l
    required_lpm = required_volume_flow_l_s * 60.0
    return required_lpm

def estimate_gpu_junction_temp(coolant_inlet_c: float, thermal_resistance_k_w: float, wattage_w: float) -> float:
    """
    Predicts steady-state GPU silicon junction temperature.
    Equation: T_j = T_inlet + (Q * R_theta)
    """
    return coolant_inlet_c + (wattage_w * thermal_resistance_k_w)
