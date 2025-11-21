from __future__ import annotations
from typing import TYPE_CHECKING, List
from exceptions.GateConflictException import GateConflictException

if TYPE_CHECKING:
    from models.infrastructure.Terminal import Terminal
    from models.flight.Flight import Flight
    from models.staff.GroundStaff import GroundStaff

class Gate:
    def __init__(self, gate_number: str, terminal: Terminal) -> None:
        self.gate_number: str = gate_number
        self.terminal: Terminal = terminal
        self.current_flight: Flight | None = None
        self.assigned_staff: List[GroundStaff] = []
        self.is_operational: bool = True
        self.maintenance_required: bool = False
        self.history: List[str] = []

    def assign_flight(self, flight: Flight) -> None:
        if self.current_flight and self.current_flight != flight:
            raise GateConflictException(self.gate_number)
        self.current_flight = flight
        self.history.append(flight.flight_number)

    def release_flight(self) -> None:
        self.current_flight = None

    def is_available(self) -> bool:
        return self.current_flight is None and self.is_operational and not self.maintenance_required

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def shutdown(self) -> None:
        self.is_operational = False

    def restart(self) -> None:
        self.is_operational = True

    def assign_staff(self, staff: GroundStaff) -> None:
        self.assigned_staff.append(staff)

    def get_staff_by_role(self, role: str) -> List[GroundStaff]:
        return [s for s in self.assigned_staff if s.role == role]

    def has_flight(self, flight_number: str) -> bool:
        return self.current_flight is not None and self.current_flight.flight_number == flight_number

    def get_terminal_name(self) -> str:
        return self.terminal.name

    def get_recent_flights(self, limit: int = 5) -> List[str]:
        return self.history[-limit:]
