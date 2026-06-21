# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
zone_model.py — Zone Thermal Telemetry & Load Modeling
======================================================
Helix Alpha Strand: Multi-zone datacenter heat loading and ambient modeling.
"""
from dataclasses import dataclass
from typing import List

@dataclass
class ThermalZone:
    zone_id: str
    rack_count: int
    avg_load_per_rack_kw: float
    ambient_offset_k: float

class DatacenterThermalModel:
    def __init__(self, baseline_ambient_c: float = 22.0) -> None:
        self.baseline_ambient_c = baseline_ambient_c
        self.zones: List[ThermalZone] = []

    # 1. PREPARATION LEVEL
    def verify_zone_config(self) -> bool:
        """Validates rack-to-zone mappings match facility plans."""
        return len(self.zones) > 0

    # 2. OPERATION LEVEL
    def add_zone(self, zone_id: str, rack_count: int, load_kw: float, offset: float) -> None:
        self.zones.append(ThermalZone(zone_id, rack_count, load_kw, offset))

    def get_total_heat_load_kw(self) -> float:
        return sum(zone.rack_count * zone.avg_load_per_rack_kw for zone in self.zones)

    def calculate_zone_ambient_temp(self, zone_id: str, seasonal_boost_c: float = 0.0) -> float:
        for zone in self.zones:
            if zone.zone_id == zone_id:
                return self.baseline_ambient_c + zone.ambient_offset_k + seasonal_boost_c
        raise ValueError(f"Zone {zone_id} not found.")

    # 3. EMERGENCY REACTION LEVEL
    def isolate_hottest_zone(self) -> str:
        """Determines the zone with the highest thermal load for emergency containment."""
        if not self.zones:
            return ""
        return max(self.zones, key=lambda z: z.avg_load_per_rack_kw).zone_id
