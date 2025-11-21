from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.infrastructure.Gate import Gate
    from models.staff.GroundStaff import GroundStaff

class Terminal:
    VALID_TERMINAL_NAMES = {"A", "B", "C", "D", "E", "International", "Domestic"}

    def __init__(self, name: str) -> None:
        if name not in self.VALID_TERMINAL_NAMES:
            raise ValueError(f"Invalid terminal name: {name}")
        self.name: str = name
        self.gates: List[Gate] = []
        self.assigned_staff: List[GroundStaff] = []
        self.maintenance_required: bool = False

    def add_gate(self, gate: Gate) -> None:
        self.gates.append(gate)

    def get_gate_by_number(self, gate_number: str) -> Gate | None:
        return next((g for g in self.gates if g.gate_number == gate_number), None)

    def total_gate_count(self) -> int:
        return len(self.gates)

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def is_operational(self) -> bool:
        return not self.maintenance_required

    def assign_staff(self, staff: GroundStaff) -> None:
        self.assigned_staff.append(staff)

    def get_staff_by_role(self, role: str) -> List[GroundStaff]:
        return [s for s in self.assigned_staff if s.role == role]

    def summary(self) -> str:
        return f"Terminal {self.name} with {len(self.gates)} gates"
