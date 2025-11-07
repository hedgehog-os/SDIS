from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.flight.flight import Flight
    from models.passenger.passenger import Passenger

class BoardingProcedure:
    def __init__(self, flight: Flight) -> None:
        self.flight: Flight = flight
        self.boarded_passengers: list[Passenger] = []
        self.rejected_passengers: list[str] = []
        self.is_locked: bool = False

    def board(self, passenger: Passenger) -> bool:
        if self.is_locked:
            return False
        if passenger not in self.flight.passengers:
            self.rejected_passengers.append(passenger.full_name)
            return False
        if passenger in self.boarded_passengers:
            return False
        self.boarded_passengers.append(passenger)
        return True

    def is_complete(self) -> bool:
        return len(self.boarded_passengers) >= len(self.flight.passengers)

    def lock(self) -> None:
        self.is_locked = True

    def unlock(self) -> None:
        self.is_locked = False

    def reset(self) -> None:
        self.boarded_passengers.clear()
        self.rejected_passengers.clear()
        self.is_locked = False

    def get_boarded_names(self) -> list[str]:
        return [p.full_name for p in self.boarded_passengers]

    def get_missing_passengers(self) -> list[Passenger]:
        return [p for p in self.flight.passengers if p not in self.boarded_passengers]

    def get_rejected_names(self) -> list[str]:
        return self.rejected_passengers.copy()

    def summary(self) -> str:
        return (
            f"Boarding for flight {self.flight.flight_number}: "
            f"{len(self.boarded_passengers)}/{len(self.flight.passengers)} boarded, "
            f"{len(self.rejected_passengers)} rejected"
        )
