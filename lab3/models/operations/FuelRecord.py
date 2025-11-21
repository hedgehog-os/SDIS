from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.flight.Aircraft import Aircraft

class FuelRecord:
    def __init__(self, aircraft: Aircraft, fuel_liters: float, timestamp: str) -> None:
        if fuel_liters < 0:
            raise ValueError("Fuel amount cannot be negative.")
        self.aircraft: Aircraft = aircraft
        self.fuel_liters: float = fuel_liters
        self.timestamp: str = timestamp
        self.is_verified: bool = False
        self.notes: list[str] = []

    def verify(self) -> None:
        self.is_verified = True

    def invalidate(self, reason: str) -> None:
        self.is_verified = False
        self.notes.append(f"Invalidated: {reason}")

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def reset(self) -> None:
        self.is_verified = False
        self.notes.clear()

    def summary(self) -> str:
        status = "VERIFIED" if self.is_verified else "UNVERIFIED"
        return (
            f"FuelRecord for {self.aircraft.registration} at {self.timestamp}: "
            f"{self.fuel_liters:.2f} L, {status}"
        )

    def is_excessive(self) -> bool:
        return self.fuel_liters > self.aircraft.max_fuel_capacity_liters

    def fuel_percentage(self) -> float:
        return round((self.fuel_liters / self.aircraft.max_fuel_capacity_liters) * 100, 2)
