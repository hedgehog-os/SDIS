from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from models.flight.Aircraft import Aircraft
    from models.staff.MaintenanceTechnician import MaintenanceTechnician

class MaintenanceLog:
    def __init__(self, aircraft: Aircraft, technician: MaintenanceTechnician, notes: str, timestamp: str) -> None:
        if not notes.strip():
            raise ValueError("Maintenance notes cannot be empty.")
        self.aircraft: Aircraft = aircraft
        self.technician: MaintenanceTechnician = technician
        self.notes: str = notes
        self.timestamp: str = timestamp
        self.is_resolved: bool = False
        self.resolution_notes: List[str] = []
        self.resolved_by: Optional[str] = None

    def mark_resolved(self, resolver_name: str = "anonymous", resolution_note: str = "Resolved") -> None:
        self.is_resolved = True
        self.resolved_by = resolver_name
        self.resolution_notes.append(resolution_note)

    def reopen(self, reason: str = "Reopened for further inspection") -> None:
        self.is_resolved = False
        self.resolved_by = None
        self.resolution_notes.append(reason)

    def add_resolution_note(self, note: str) -> None:
        self.resolution_notes.append(note)

    def reset(self) -> None:
        self.is_resolved = False
        self.resolved_by = None
        self.resolution_notes.clear()

    def summary(self) -> str:
        status = "RESOLVED" if self.is_resolved else "OPEN"
        who = f" by {self.resolved_by}" if self.resolved_by else ""
        return (
            f"MaintenanceLog for {self.aircraft.registration} at {self.timestamp} — {status}{who}, "
            f"Technician: {self.technician.full_name}"
        )
