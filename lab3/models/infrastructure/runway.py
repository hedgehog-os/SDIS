from __future__ import annotations
from typing import List

class Runway:
    MIN_LENGTH_METERS = 1000
    MAX_LENGTH_METERS = 5000

    def __init__(self, identifier: str, length_meters: int, is_active: bool = True) -> None:
        if not (self.MIN_LENGTH_METERS <= length_meters <= self.MAX_LENGTH_METERS):
            raise ValueError(f"Runway length must be between {self.MIN_LENGTH_METERS} and {self.MAX_LENGTH_METERS} meters.")
        self.identifier: str = identifier
        self.length_meters: int = length_meters
        self.is_active: bool = is_active
        self.maintenance_required: bool = False
        self.landing_log: List[str] = []
        self.takeoff_log: List[str] = []

    def close(self) -> None:
        self.is_active = False

    def open(self) -> None:
        self.is_active = True

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def is_operational(self) -> bool:
        return self.is_active and not self.maintenance_required

    def log_landing(self, flight_number: str) -> None:
        self.landing_log.append(flight_number)

    def log_takeoff(self, flight_number: str) -> None:
        self.takeoff_log.append(flight_number)

    def get_landing_count(self) -> int:
        return len(self.landing_log)

    def get_takeoff_count(self) -> int:
        return len(self.takeoff_log)

    def reset(self) -> None:
        self.is_active = True
        self.maintenance_required = False
        self.landing_log.clear()
        self.takeoff_log.clear()

    def supports_aircraft_size(self, required_length: int) -> bool:
        return self.length_meters >= required_length

    def summary(self) -> str:
        status = "active" if self.is_active else "closed"
        return f"Runway {self.identifier} ({self.length_meters}m, {status})"
