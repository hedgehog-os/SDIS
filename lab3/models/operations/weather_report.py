from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from models.flight.aircraft import Aircraft
    from models.infrastructure.runway import Runway

class WeatherReport:
    UNSAFE_CONDITIONS = {"storm", "fog", "snow", "hail", "tornado"}
    EXTREME_WIND_KPH = 60.0
    EXTREME_TEMP_C = (-30.0, 45.0)

    def __init__(
        self,
        location: str,
        temperature_c: float,
        wind_kph: float,
        condition: str,
        aircraft: Optional[Aircraft] = None,
        runway: Optional[Runway] = None
    ) -> None:
        self.location: str = location
        self.temperature_c: float = temperature_c
        self.wind_kph: float = wind_kph
        self.condition: str = condition.strip().lower()
        self.aircraft: Optional[Aircraft] = aircraft
        self.runway: Optional[Runway] = runway
        self.notes: List[str] = []
        self.is_verified: bool = False

    def is_safe_for_flight(self) -> bool:
        return (
            self.condition not in self.UNSAFE_CONDITIONS and
            self.wind_kph <= self.EXTREME_WIND_KPH and
            self.EXTREME_TEMP_C[0] <= self.temperature_c <= self.EXTREME_TEMP_C[1]
        )

    def is_safe_for_aircraft(self) -> bool:
        if not self.aircraft:
            return self.is_safe_for_flight()
        return (
            self.is_safe_for_flight() and
            self.temperature_c >= self.aircraft.min_operating_temp_c and
            self.wind_kph <= self.aircraft.max_crosswind_kph
        )

    def is_safe_for_runway(self) -> bool:
        if not self.runway:
            return self.is_safe_for_flight()
        return (
            self.is_safe_for_flight() and
            not self.runway.is_flooded and
            not self.runway.is_icy
        )

    def mark_verified(self) -> None:
        self.is_verified = True

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def reset(self) -> None:
        self.notes.clear()
        self.is_verified = False

    def summary(self) -> str:
        status = "VERIFIED" if self.is_verified else "UNVERIFIED"
        safety = "SAFE" if self.is_safe_for_aircraft() and self.is_safe_for_runway() else "UNSAFE"
        aircraft_info = f" for aircraft {self.aircraft.registration}" if self.aircraft else ""
        runway_info = f" on runway {self.runway.code}" if self.runway else ""
        return (
            f"Weather at {self.location}{aircraft_info}{runway_info}: "
            f"{self.temperature_c:.1f}°C, {self.wind_kph:.1f} kph wind, {self.condition.capitalize()} — "
            f"{safety}, {status}"
        )
