from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Optional
from exceptions.flight_exceptions import GateConflictException

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger
    from models.flight.route import Route
    from models.flight.flight_schedule import FlightSchedule
    from models.flight.aircraft import Aircraft
    from models.flight.airline import Airline
    from models.infrastructure.gate import Gate
    from models.operations.boarding_pass import BoardingPass
    from models.staff.pilot import Pilot
    from models.staff.flight_attendant import FlightAttendant

class Flight:
    def __init__(
        self,
        flight_number: str,
        airline: Airline,
        aircraft: Aircraft,
        route: Route,
        schedule: FlightSchedule,
        departure_gate: Gate,
        arrival_gate: Gate
    ) -> None:
        self.flight_number = flight_number
        self.airline = airline
        self.aircraft = aircraft
        self.route = route
        self.schedule = schedule
        self.departure_gate = departure_gate
        self.arrival_gate = arrival_gate
        self.passengers: List[Passenger] = []
        self.boarding_passes: List[BoardingPass] = []
        self.pilots: List[Pilot] = []
        self.attendants: List[FlightAttendant] = []
        self.notes: List[str] = []
        self.status: str = "Scheduled"

    def board_passenger(self, passenger: Passenger) -> None:
        if self.is_full():
            raise Exception("Flight is full.")
        self.passengers.append(passenger)
        self.notes.append(f"Boarded {passenger.full_name}")

    def remove_passenger(self, passport_number: str) -> bool:
        for p in self.passengers:
            if p.passport.number == passport_number:
                self.passengers.remove(p)
                self.notes.append(f"Removed passenger {p.full_name}")
                return True
        return False

    def get_manifest(self) -> List[Passenger]:
        return self.passengers.copy()

    def is_full(self) -> bool:
        return len(self.passengers) >= self.aircraft.capacity

    def available_seats(self) -> int:
        return self.aircraft.capacity - len(self.passengers)

    def has_passenger(self, passport_number: str) -> bool:
        return any(p.passport.number == passport_number for p in self.passengers)

    def assign_gate(self, gate: Gate) -> None:
        if gate.current_flight and gate.current_flight != self:
            raise GateConflictException(gate.gate_number)
        self.departure_gate = gate
        gate.assign_flight(self)
        self.notes.append(f"Gate {gate.gate_number} assigned")

    def get_passenger_by_name(self, name: str) -> Optional[Passenger]:
        return next((p for p in self.passengers if p.full_name == name), None)

    def assign_crew(self, pilot: Pilot, attendants: List[FlightAttendant]) -> None:
        self.pilots.append(pilot)
        self.attendants.extend(attendants)
        self.notes.append(f"Crew assigned: Pilot {pilot.name}, {len(attendants)} attendants")

    def get_languages_onboard(self) -> List[str]:
        return list({lang for a in self.attendants for lang in a.languages})

    def generate_boarding_passes(self) -> None:
        for passenger in self.passengers:
            bp = BoardingPass(ticket=passenger.ticket, passenger=passenger, gate_number=self.departure_gate.gate_number)
            self.boarding_passes.append(bp)
        self.notes.append(f"{len(self.boarding_passes)} boarding passes generated")

    def get_boarding_pass(self, passport_number: str) -> Optional[BoardingPass]:
        return next((bp for bp in self.boarding_passes if bp.passenger.passport.number == passport_number), None)

    def is_ready_for_departure(self) -> bool:
        return (
            self.schedule.is_valid_range()
            and self.departure_gate is not None
            and self.aircraft is not None
            and self.pilots
            and len(self.attendants) >= 2
            and not self.is_full()
        )

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        self.notes.append(f"Status updated to {new_status}")

    def get_flight_summary(self) -> str:
        return (
            f"{self.flight_number}: {self.route.origin.code} → {self.route.destination.code}, "
            f"{self.schedule.departure_time} → {self.schedule.arrival_time}, "
            f"{len(self.passengers)}/{self.aircraft.capacity} passengers, Status: {self.status}"
        )

    def to_dict(self) -> Dict:
        return {
            "flight_number": self.flight_number,
            "airline": self.airline.name,
            "aircraft": self.aircraft.model,
            "route": f"{self.route.origin.code} → {self.route.destination.code}",
            "schedule": {
                "departure": self.schedule.departure_time,
                "arrival": self.schedule.arrival_time
            },
            "crew": {
                "pilots": [p.name for p in self.pilots],
                "attendants": [a.name for a in self.attendants]
            },
            "passenger_count": len(self.passengers),
            "boarding_passes": [bp.passenger.full_name for bp in self.boarding_passes],
            "status": self.status,
            "notes": self.notes.copy()
        }
