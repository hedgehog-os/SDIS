from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from models.flight.flight import Flight

class FlightAttendant:
    def __init__(self, name: str, languages: List[str]) -> None:
        self.name: str = name
        self.languages: List[str] = languages
        self.assigned_flights: List[Flight] = []
        self.notes: List[str] = []

    def assign_to_flight(self, flight: Flight) -> None:
        if flight not in self.assigned_flights:
            self.assigned_flights.append(flight)
            self.notes.append(f"Assigned to flight {flight.flight_number}")
            flight.attendants.append(self)  # bidirectional association

    def remove_from_flight(self, flight: Flight) -> bool:
        if flight in self.assigned_flights:
            self.assigned_flights.remove(flight)
            self.notes.append(f"Removed from flight {flight.flight_number}")
            if self in flight.attendants:
                flight.attendants.remove(self)
            return True
        return False

    def get_flight_numbers(self) -> List[str]:
        return [f.flight_number for f in self.assigned_flights]

    def get_routes(self) -> List[str]:
        return [f"{f.route.origin.code} → {f.route.destination.code}" for f in self.assigned_flights]

    def get_languages_coverage(self) -> str:
        return ", ".join(sorted(set(self.languages)))

    def is_available_for(self, date: str) -> bool:
        return all(f.schedule.departure_time[:10] != date for f in self.assigned_flights)

    def get_schedule_summary(self) -> str:
        if not self.assigned_flights:
            return f"{self.name} has no assigned flights."
        lines = [f"Schedule for {self.name}:"]
        for flight in self.assigned_flights:
            lines.append(
                f"• {flight.flight_number}: {flight.route.origin.code} → {flight.route.destination.code} "
                f"on {flight.schedule.departure_time}"
            )
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "languages": self.languages.copy(),
            "assigned_flights": self.get_flight_numbers(),
            "notes": self.notes.copy()
        }

    def summary(self) -> str:
        return (
            f"{self.name} — Languages: {self.get_languages_coverage()}, "
            f"Flights: {len(self.assigned_flights)} assigned"
        )
