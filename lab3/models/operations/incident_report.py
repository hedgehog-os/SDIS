from __future__ import annotations
from typing import List

class IncidentReport:
    VALID_SEVERITY_LEVELS = {"low", "moderate", "high", "critical"}

    def __init__(self, report_id: str, description: str, severity: str, timestamp: str) -> None:
        if severity.lower() not in self.VALID_SEVERITY_LEVELS:
            raise ValueError(f"Invalid severity level: {severity}")
        self.report_id: str = report_id
        self.description: str = description
        self.severity: str = severity.lower()
        self.timestamp: str = timestamp
        self.is_resolved: bool = False
        self.resolution_notes: List[str] = []
        self.associated_zones: List[str] = []
        self.reviewed: bool = False

    def resolve(self, note: str = "Resolved") -> None:
        self.is_resolved = True
        self.resolution_notes.append(note)

    def reopen(self, reason: str = "Reopened for review") -> None:
        self.is_resolved = False
        self.resolution_notes.append(reason)

    def mark_reviewed(self) -> None:
        self.reviewed = True

    def add_zone(self, zone_name: str) -> None:
        if zone_name not in self.associated_zones:
            self.associated_zones.append(zone_name)

    def remove_zone(self, zone_name: str) -> bool:
        if zone_name in self.associated_zones:
            self.associated_zones.remove(zone_name)
            return True
        return False

    def get_zone_list(self) -> List[str]:
        return self.associated_zones.copy()

    def reset(self) -> None:
        self.is_resolved = False
        self.resolution_notes.clear()
        self.associated_zones.clear()
        self.reviewed = False

    def summary(self) -> str:
        status = "RESOLVED" if self.is_resolved else "OPEN"
        return (
            f"Incident {self.report_id} [{self.severity.upper()}] at {self.timestamp}: "
            f"{status}, Zones: {len(self.associated_zones)}, Reviewed: {self.reviewed}"
        )
