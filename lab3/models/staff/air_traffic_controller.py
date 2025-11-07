from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.flight.flight import Flight

class AirTrafficController:
    def __init__(self, name: str, control_tower_id: str) -> None:
        self.name: str = name
        self.control_tower_id: str = control_tower_id
        self.active_flights: list[Flight] = []
        self.log: list[str] = []

    def authorize_takeoff(self, flight: Flight) -> str:
        self.active_flights.append(flight)
        message = f"Flight {flight.flight_number} authorized for takeoff by {self.name}"
        self.log.append(message)
        return message

    def release_flight(self, flight: Flight) -> None:
        self.active_flights = [f for f in self.active_flights if f != flight]
        self.log.append(f"Flight {flight.flight_number} released from control by {self.name}")

    def is_controlling(self, flight: Flight) -> bool:
        return flight in self.active_flights

    def get_active_flight_numbers(self) -> list[str]:
        return [f.flight_number for f in self.active_flights]

    def summary(self) -> str:
        return (
            f"Controller {self.name} (Tower {self.control_tower_id}) — "
            f"{len(self.active_flights)} active flight(s)"
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "control_tower_id": self.control_tower_id,
            "active_flights": self.get_active_flight_numbers(),
            "log": self.log.copy()
        }

    def handover_to(self, flight: Flight, other: AirTrafficController) -> str:
        if flight not in self.active_flights:
            message = f"Flight {flight.flight_number} is not under control of {self.name}"
            self.log.append(message)
            return message

        self.release_flight(flight)
        other.authorize_takeoff(flight)
        message = (
            f"Flight {flight.flight_number} handed over from {self.name} "
            f"(Tower {self.control_tower_id}) to {other.name} (Tower {other.control_tower_id})"
        )
        self.log.append(message)
        other.log.append(message)
        return message

    def get_flight_log(self, flight: Flight) -> list[str]:
        return [entry for entry in self.log if flight.flight_number in entry]


    def get_handover_history(self) -> list[str]:
        return [entry for entry in self.log if "handed over" in entry]
