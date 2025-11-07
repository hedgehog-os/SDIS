from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.passenger.ticket import Ticket
    from models.passenger.passenger import Passenger

class BoardingPass:
    VALID_GATE_PREFIXES = {"A", "B", "C", "D", "E", "F"}

    def __init__(self, ticket: Ticket, passenger: Passenger, gate_number: str) -> None:
        if not self._is_valid_gate_number(gate_number):
            raise ValueError(f"Invalid gate number format: {gate_number}")
        self.ticket: Ticket = ticket
        self.passenger: Passenger = passenger
        self.gate_number: str = gate_number
        self.is_scanned: bool = False
        self.scan_log: List[str] = []

    def scan(self, timestamp: str = "unknown") -> None:
        self.is_scanned = True
        self.scan_log.append(timestamp)

    def reset_scan(self) -> None:
        self.is_scanned = False
        self.scan_log.clear()

    def scanned_times(self) -> int:
        return len(self.scan_log)

    def get_passenger_name(self) -> str:
        return self.passenger.full_name

    def get_ticket_info(self) -> str:
        return f"{self.ticket.ticket_number} ({self.ticket.seat_number})"

    def is_valid(self) -> bool:
        return not self.is_scanned and self.ticket.is_active

    def summary(self) -> str:
        return f"{self.get_passenger_name()} → Gate {self.gate_number}, Seat {self.ticket.seat_number}"

    @classmethod
    def _is_valid_gate_number(cls, gate_number: str) -> bool:
        if len(gate_number) < 2:
            return False
        prefix = gate_number[0].upper()
        return prefix in cls.VALID_GATE_PREFIXES and gate_number[1:].isdigit()
