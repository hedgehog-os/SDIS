from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
from datetime import datetime

if TYPE_CHECKING:
    from models.infrastructure.Airport import Airport
    from models.infrastructure.Gate import Gate
    from models.infrastructure.Lounge import Lounge
    from models.infrastructure.Restroom import Restroom
    from models.flight.Flight import Flight

class GroundStaff:
    def __init__(self, name: str, role: str, airport: Airport) -> None:
        self.name: str = name
        self.role: str = role
        self.airport: Airport = airport
        self.assigned_gates: List[Gate] = []
        self.assigned_tasks: List[str] = []
        self.notes: List[str] = []
        self.task_log: List[Dict[str, str]] = []

    def assign_gate(self, gate: Gate) -> None:
        if gate not in self.assigned_gates:
            self.assigned_gates.append(gate)
            self.notes.append(f"Assigned to gate {gate.gate_number}")

    def perform_task(self, task: str, location: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {
            "task": task,
            "location": location,
            "time": timestamp
        }
        self.assigned_tasks.append(task)
        self.task_log.append(entry)
        self.notes.append(f"Performed '{task}' at {location} on {timestamp}")

    def assist_flight(self, flight: Flight) -> None:
        self.perform_task("Flight assistance", flight.flight_number)

    def clean_area(self, area: Restroom | Lounge) -> None:
        area.is_clean = True
        self.perform_task("Cleaning", getattr(area, "location_id", getattr(area, "name", "Unknown")))

    def get_gate_numbers(self) -> List[str]:
        return [g.gate_number for g in self.assigned_gates]

    def get_task_summary(self) -> str:
        if not self.task_log:
            return f"{self.name} has no recorded tasks."
        lines = [f"Task log for {self.name}:"]
        for entry in self.task_log:
            lines.append(f"• {entry['task']} at {entry['location']} on {entry['time']}")
        return "\n".join(lines)

    def reset_tasks(self) -> None:
        cleared = len(self.task_log)
        self.assigned_tasks.clear()
        self.task_log.clear()
        self.notes.append(f"Reset {cleared} task(s) for new shift")

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "airport": self.airport.code,
            "assigned_gates": self.get_gate_numbers(),
            "tasks": self.assigned_tasks.copy(),
            "notes": self.notes.copy(),
            "task_log": self.task_log.copy()
        }

    def summary(self) -> str:
        return (
            f"{self.name} — Role: {self.role}, Airport: {self.airport.code}, "
            f"Gates: {len(self.assigned_gates)}, Tasks: {len(self.task_log)}"
        )
