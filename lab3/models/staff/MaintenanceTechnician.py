from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
from datetime import datetime

if TYPE_CHECKING:
    from models.flight.Aircraft import Aircraft

class MaintenanceTechnician:
    def __init__(self, name: str, specialization: str) -> None:
        self.name: str = name
        self.specialization: str = specialization
        self.inspected_aircrafts: List[str] = []
        self.maintenance_log: List[Dict[str, str]] = []
        self.notes: List[str] = []

    def inspect_aircraft(self, aircraft: Aircraft) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {
            "action": "Inspection",
            "aircraft": aircraft.registration_number,
            "model": aircraft.model,
            "time": timestamp
        }
        self.inspected_aircrafts.append(aircraft.registration_number)
        self.maintenance_log.append(entry)
        self.notes.append(f"Inspected {aircraft.registration_number} ({aircraft.model}) at {timestamp}")
        aircraft.last_inspection_by = self.name  # optional association
        return f"{self.name} inspected aircraft {aircraft.registration_number} ({aircraft.model})"

    def perform_maintenance(self, aircraft: Aircraft, task: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {
            "action": f"Maintenance: {task}",
            "aircraft": aircraft.registration_number,
            "model": aircraft.model,
            "time": timestamp
        }
        self.maintenance_log.append(entry)
        self.notes.append(f"Performed '{task}' on {aircraft.registration_number} at {timestamp}")
        aircraft.mark_maintenance(task, self.name, timestamp)  # optional domain hook

    def get_aircrafts_serviced(self) -> List[str]:
        return list({entry["aircraft"] for entry in self.maintenance_log})

    def get_log_summary(self) -> str:
        if not self.maintenance_log:
            return f"{self.name} has no recorded maintenance activity."
        lines = [f"Maintenance log for {self.name}:"]
        for entry in self.maintenance_log:
            lines.append(f"• {entry['action']} on {entry['aircraft']} ({entry['model']}) at {entry['time']}")
        return "\n".join(lines)

    def reset_log(self) -> None:
        cleared = len(self.maintenance_log)
        self.maintenance_log.clear()
        self.inspected_aircrafts.clear()
        self.notes.append(f"Reset log with {cleared} entries")

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "specialization": self.specialization,
            "inspected_aircrafts": self.inspected_aircrafts.copy(),
            "maintenance_log": self.maintenance_log.copy(),
            "notes": self.notes.copy()
        }

    def summary(self) -> str:
        return (
            f"{self.name} — Specialization: {self.specialization}, "
            f"Aircrafts serviced: {len(self.get_aircrafts_serviced())}, "
            f"Total tasks: {len(self.maintenance_log)}"
        )
