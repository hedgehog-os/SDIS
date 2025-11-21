from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.flight.Route import Route
    from models.flight.Aircraft import Aircraft

class FlightPlan:
    MIN_ALTITUDE_FT = 10000
    MAX_ALTITUDE_FT = 45000

    def __init__(self, route: Route, aircraft: Aircraft, cruising_altitude_ft: int, estimated_duration_min: int) -> None:
        if not (self.MIN_ALTITUDE_FT <= cruising_altitude_ft <= self.MAX_ALTITUDE_FT):
            raise ValueError(f"Cruising altitude must be between {self.MIN_ALTITUDE_FT} and {self.MAX_ALTITUDE_FT} feet.")
        if estimated_duration_min <= 0:
            raise ValueError("Estimated duration must be positive.")
        self.route: Route = route
        self.aircraft: Aircraft = aircraft
        self.cruising_altitude_ft: int = cruising_altitude_ft
        self.estimated_duration_min: int = estimated_duration_min
        self.is_approved: bool = False
        self.notes: list[str] = []

    def approve(self) -> None:
        self.is_approved = True

    def reject(self, reason: str) -> None:
        self.is_approved = False
        self.notes.append(f"Rejected: {reason}")

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def reset(self) -> None:
        self.is_approved = False
        self.notes.clear()

    def summary(self) -> str:
        status = "APPROVED" if self.is_approved else "PENDING"
        return (
            f"FlightPlan for {self.aircraft.registration} via {self.route.origin} → {self.route.destination}, "
            f"{self.cruising_altitude_ft} ft, {self.estimated_duration_min} min, {status}"
        )

    def is_suitable_for_aircraft(self) -> bool:
        return self.cruising_altitude_ft <= self.aircraft.max_altitude_ft

    def estimated_fuel_usage(self) -> float:
        return round(self.aircraft.fuel_burn_rate_per_min * self.estimated_duration_min, 2)
