from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.infrastructure.airport import Airport

class Route:
    def __init__(self, origin: Airport, destination: Airport, distance_km: float) -> None:
        self.origin: Airport = origin
        self.destination: Airport = destination
        self.distance_km: float = distance_km
        self.alternate_airports: list[Airport] = []

    def is_international(self) -> bool:
        return self.origin.country != self.destination.country

    def is_domestic(self) -> bool:
        return self.origin.country == self.destination.country

    def is_short_haul(self) -> bool:
        return self.distance_km < 1500

    def is_long_haul(self) -> bool:
        return self.distance_km > 3500

    def midpoint_city(self) -> str:
        return f"{self.origin.city}–{self.destination.city}"

    def add_alternate_airport(self, airport: Airport) -> None:
        self.alternate_airports.append(airport)

    def has_alternate_airport(self, code: str) -> bool:
        return any(a.code == code for a in self.alternate_airports)

    def get_country_pair(self) -> tuple[str, str]:
        return (self.origin.country, self.destination.country)

    def get_airport_codes(self) -> tuple[str, str]:
        return (self.origin.code, self.destination.code)

    def summary(self) -> str:
        return f"{self.origin.code} → {self.destination.code} ({self.distance_km} km)"
