from __future__ import annotations
from typing import List

class Kiosk:
    VALID_LOCATIONS = {
        "arrival hall",
        "departure hall",
        "security zone",
        "baggage claim",
        "main lobby",
        "gate area"
    }

    def __init__(self, kiosk_id: str, location: str) -> None:
        if location not in self.VALID_LOCATIONS:
            raise ValueError(f"Invalid location: {location}")
        self.kiosk_id: str = kiosk_id
        self.location: str = location
        self.is_active: bool = True
        self.maintenance_required: bool = False
        self.usage_log: List[str] = []
        self.error_log: List[str] = []

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def log_usage(self, user_id: str) -> None:
        self.usage_log.append(user_id)

    def log_error(self, message: str) -> None:
        self.error_log.append(message)
        self.mark_for_maintenance()

    def reset(self) -> None:
        self.is_active = True
        self.maintenance_required = False
        self.usage_log.clear()
        self.error_log.clear()

    def is_operational(self) -> bool:
        return self.is_active and not self.maintenance_required

    def usage_count(self) -> int:
        return len(self.usage_log)

    def error_count(self) -> int:
        return len(self.error_log)

    def get_location_zone(self) -> str:
        return self.location.replace(" ", "_").upper()
