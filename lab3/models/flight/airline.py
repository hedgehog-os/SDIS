from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.flight.aircraft import Aircraft
    from models.flight.flight import Flight
    from models.passenger.loyalty_program import LoyaltyProgram
    from models.staff.pilot import Pilot
    from models.staff.flight_attendant import FlightAttendant

class Airline:
    def __init__(self, name: str, code: str, country: str) -> None:
        self.name: str = name
        self.code: str = code
        self.country: str = country
        self.fleet: List[Aircraft] = []
        self.flights: List[Flight] = []
        self.loyalty_programs: List[LoyaltyProgram] = []
        self.pilots: List[Pilot] = []
        self.attendants: List[FlightAttendant] = []

    def full_name(self) -> str:
        return f"{self.name} ({self.code})"

    def add_aircraft(self, aircraft: Aircraft) -> None:
        self.fleet.append(aircraft)

    def register_flight(self, flight: Flight) -> None:
        self.flights.append(flight)

    def assign_pilot(self, pilot: Pilot) -> None:
        self.pilots.append(pilot)

    def assign_attendant(self, attendant: FlightAttendant) -> None:
        self.attendants.append(attendant)

    def create_loyalty_program(self, program: LoyaltyProgram) -> None:
        self.loyalty_programs.append(program)

    def get_aircraft_by_model(self, model: str) -> List[Aircraft]:
        return [a for a in self.fleet if a.model == model]

    def get_flights_by_destination(self, destination_code: str) -> List[Flight]:
        return [f for f in self.flights if f.route.destination.code == destination_code]

    def total_seats_available(self) -> int:
        return sum(a.capacity for a in self.fleet)

    def is_international_carrier(self) -> bool:
        return any(f.route.is_international() for f in self.flights)

    def get_loyalty_tiers(self) -> List[str]:
        return list({p.tier for p in self.loyalty_programs})

    def has_aircraft(self, registration_number: str) -> bool:
        return any(a.registration_number == registration_number for a in self.fleet)

    def get_pilot_by_license(self, license_number: str) -> Pilot | None:
        return next((p for p in self.pilots if p.license_number == license_number), None)

    def get_attendants_by_language(self, language: str) -> List[FlightAttendant]:
        return [a for a in self.attendants if language in a.languages]
