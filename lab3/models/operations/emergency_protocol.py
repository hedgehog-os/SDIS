from __future__ import annotations
from typing import List

class EmergencyProtocol:
    VALID_SEVERITY_LEVELS = {"low", "moderate", "high", "critical"}

    def __init__(self, protocol_id: str, description: str, severity_level: str) -> None:
        if severity_level.lower() not in self.VALID_SEVERITY_LEVELS:
            raise ValueError(f"Invalid severity level: {severity_level}")
        self.protocol_id: str = protocol_id
        self.description: str = description
        self.severity_level: str = severity_level.lower()
        self.is_active: bool = False
        self.activation_log: List[str] = []
        self.deactivation_log: List[str] = []
        self.associated_zones: List[str] = []
        self.reviewed: bool = False

    def activate(self, timestamp: str = "unknown") -> None:
        self.is_active = True
        self.activation_log.append(timestamp)

    def deactivate(self, timestamp: str = "unknown") -> None:
        self.is_active = False
        self.deactivation_log.append(timestamp)

    def mark_reviewed(self) -> None:
        self.reviewed = True

    def reset(self) -> None:
        self.is_active = False
        self.activation_log.clear()
        self.deactivation_log.clear()
        self.associated_zones.clear()
        self.reviewed = False

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

    def summary(self) -> str:
        status = "ACTIVE" if self.is_active else "INACTIVE"
        return (
            f"Protocol {self.protocol_id} [{self.severity_level.upper()}]: "
            f"{status}, Zones: {len(self.associated_zones)}, Reviewed: {self.reviewed}"
        )
