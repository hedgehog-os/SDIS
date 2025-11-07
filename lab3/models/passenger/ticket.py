from __future__ import annotations
from exceptions.ticket_exceptions import TicketAlreadyCheckedInException
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.flight.flight import Flight
    from models.passenger.passenger import Passenger

class Ticket:
    def __init__(self, ticket_id: str, flight: Flight, seat: str, price: float) -> None:
        self.ticket_id: str = ticket_id
        self.flight: Flight = flight
        self.seat: str = seat
        self.price: float = price
        self.is_checked_in: bool = False
        self.passenger: Optional[Passenger] = None
        self.notes: list[str] = []

    def assign_passenger(self, passenger: Passenger) -> None:
        self.passenger = passenger
        self.notes.append(f"Assigned to {passenger.full_name}")

    def check_in(self) -> None:
        if self.is_checked_in:
            raise TicketAlreadyCheckedInException(self.ticket_id)
        self.is_checked_in = True
        self.notes.append("Checked in")

    def uncheck(self) -> None:
        self.is_checked_in = False
        self.notes.append("Check-in cancelled")

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def summary(self) -> str:
        status = "Checked-in" if self.is_checked_in else "Pending"
        passenger = self.passenger.full_name if self.passenger else "Unassigned"
        return (
            f"Ticket {self.ticket_id} — Seat: {self.seat}, Price: ${self.price:.2f}, "
            f"Status: {status}, Passenger: {passenger}"
        )

    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "seat": self.seat,
            "price": self.price,
            "is_checked_in": self.is_checked_in,
            "passenger_name": self.passenger.full_name if self.passenger else None,
            "notes": self.notes.copy()
        }

    def apply_discount(self) -> None:
        if not self.passenger or not self.passenger.loyalty_program:
            return

        tier = self.passenger.loyalty_program.tier
        discount_map = {
            "Silver": 0.05,
            "Gold": 0.10,
            "Platinum": 0.15
        }

        discount = discount_map.get(tier, 0.0)
        if discount > 0:
            original_price = self.price
            self.price *= (1 - discount)
            self.notes.append(f"{tier} discount applied: {original_price:.2f} → {self.price:.2f}")

    def is_upgrade_eligible(self) -> bool:
        if not self.passenger or not self.passenger.loyalty_program:
            return False
        return self.passenger.loyalty_program.points >= 1000
    