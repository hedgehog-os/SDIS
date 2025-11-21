from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.staff.Pilot import Pilot
    from models.staff.FlightAttendant import FlightAttendant
    from models.flight.Flight import Flight

class CrewSchedule:
    def __init__(self, flight: Flight) -> None:
        self.flight: Flight = flight
        self.pilots: List[Pilot] = []
        self.attendants: List[FlightAttendant] = []
        self.notes: List[str] = []

    def assign_pilot(self, pilot: Pilot) -> None:
        self.pilots.append(pilot)
        self.notes.append(f"Pilot {pilot.name} assigned to flight {self.flight.flight_number}")

    def assign_attendant(self, attendant: FlightAttendant) -> None:
        self.attendants.append(attendant)
        self.notes.append(f"Attendant {attendant.name} assigned to flight {self.flight.flight_number}")

    def is_complete(self) -> bool:
        return len(self.pilots) >= 1 and len(self.attendants) >= 2

    def get_languages(self) -> set[str]:
        return {lang for attendant in self.attendants for lang in attendant.languages}

    def get_crew_names(self) -> dict[str, List[str]]:
        return {
            "pilots": [p.name for p in self.pilots],
            "attendants": [a.name for a in self.attendants]
        }

    def summary(self) -> str:
        crew = self.get_crew_names()
        langs = ", ".join(sorted(self.get_languages()))
        return (
            f"Crew Schedule for Flight {self.flight.flight_number}\n"
            f"- Pilots: {', '.join(crew['pilots']) or 'None'}\n"
            f"- Attendants: {', '.join(crew['attendants']) or 'None'}\n"
            f"- Languages covered: {langs or 'None'}\n"
            f"- Status: {'Complete' if self.is_complete() else 'Incomplete'}"
        )

    def to_dict(self) -> dict:
        return {
            "flight_number": self.flight.flight_number,
            "pilots": [p.name for p in self.pilots],
            "attendants": [a.name for a in self.attendants],
            "languages": sorted(self.get_languages()),
            "is_complete": self.is_complete(),
            "notes": self.notes.copy()
        }
