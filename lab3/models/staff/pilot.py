from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from models.flight.flight import Flight
    from models.flight.aircraft import Aircraft

class Pilot:
    def __init__(self, name: str, license_number: str, experience_years: int) -> None:
        self.name: str = name
        self.license_number: str = license_number
        self.experience_years: int = experience_years
        self.certifications: List[str] = []
        self.assigned_flights: List[Flight] = []
        self.notes: List[str] = []
        self.flight_log: List[Dict[str, str]] = []

    def assign_flight(self, flight: Flight) -> None:
        if flight not in self.assigned_flights:
            self.assigned_flights.append(flight)
            self.notes.append(f"Assigned to flight {flight.flight_number}")
            self.flight_log.append({
                "flight": flight.flight_number,
                "aircraft": flight.aircraft.model,
                "route": f"{flight.route.origin.code} → {flight.route.destination.code}",
                "departure": flight.schedule.departure_time
            })
            flight.pilots.append(self)

    def is_certified_for(self, aircraft: Aircraft) -> bool:
        return aircraft.model in self.certifications

    def add_certification(self, aircraft_model: str) -> None:
        if aircraft_model not in self.certifications:
            self.certifications.append(aircraft_model)
            self.notes.append(f"Certified for {aircraft_model}")

    def remove_certification(self, aircraft_model: str) -> None:
        if aircraft_model in self.certifications:
            self.certifications.remove(aircraft_model)
            self.notes.append(f"Certification removed for {aircraft_model}")

    def get_flight_numbers(self) -> List[str]:
        return [f.flight_number for f in self.assigned_flights]

    def get_certification_summary(self) -> str:
        return ", ".join(sorted(self.certifications)) or "None"

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

    def reset_schedule(self) -> None:
        cleared = len(self.assigned_flights)
        self.assigned_flights.clear()
        self.notes.append(f"Reset schedule with {cleared} flights")

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "license_number": self.license_number,
            "experience_years": self.experience_years,
            "certifications": self.certifications.copy(),
            "assigned_flights": self.get_flight_numbers(),
            "notes": self.notes.copy(),
            "flight_log": self.flight_log.copy()
        }

    def summary(self) -> str:
        return (
            f"{self.name} — License: {self.license_number}, "
            f"Experience: {self.experience_years} years, "
            f"Certified for: {self.get_certification_summary()}, "
            f"Flights assigned: {len(self.assigned_flights)}"
        )
