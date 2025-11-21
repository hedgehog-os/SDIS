from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.infrastructure.Terminal import Terminal
    from models.infrastructure.Gate import Gate
    from models.staff.GroundStaff import GroundStaff
    from models.flight.Flight import Flight

class Airport:
    def __init__(self, code: str, name: str, city: str, country: str) -> None:
        self.code: str = code
        self.name: str = name
        self.city: str = city
        self.country: str = country
        self.terminals: List[Terminal] = []
        self.staff: List[GroundStaff] = []

    def add_terminal(self, terminal: Terminal) -> None:
        self.terminals.append(terminal)

    def assign_staff(self, staff: GroundStaff) -> None:
        self.staff.append(staff)

    def get_terminal_by_name(self, name: str) -> Terminal | None:
        return next((t for t in self.terminals if t.name == name), None)

    def get_all_gates(self) -> List[Gate]:
        return [gate for terminal in self.terminals for gate in terminal.gates]

    def find_gate(self, gate_number: str) -> Gate | None:
        for terminal in self.terminals:
            for gate in terminal.gates:
                if gate.gate_number == gate_number:
                    return gate
        return None

    def get_available_gates(self) -> List[Gate]:
        return [gate for gate in self.get_all_gates() if gate.current_flight is None]

    def get_staff_by_role(self, role: str) -> List[GroundStaff]:
        return [s for s in self.staff if s.role == role]

    def has_terminal(self, name: str) -> bool:
        return any(t.name == name for t in self.terminals)

    def total_gate_count(self) -> int:
        return sum(len(t.gates) for t in self.terminals)

    def get_flights_departing(self) -> List[Flight]:
        return [gate.current_flight for gate in self.get_all_gates() if gate.current_flight]

    def summary(self) -> str:
        return f"{self.name} ({self.code}) in {self.city}, {self.country}"
