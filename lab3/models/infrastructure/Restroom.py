from __future__ import annotations
from typing import List

class Restroom:
    VALID_LOCATIONS = {
        "arrival hall",
        "departure hall",
        "security zone",
        "baggage claim",
        "main lobby",
        "gate area",
        "vip lounge"
    }

    def __init__(self, location: str, is_accessible: bool) -> None:
        if location not in self.VALID_LOCATIONS:
            raise ValueError(f"Invalid restroom location: {location}")
        self.location: str = location
        self.is_accessible: bool = is_accessible
        self.is_clean: bool = True
        self.maintenance_required: bool = False
        self.cleaning_log: List[str] = []
        self.access_log: List[str] = []

    def mark_dirty(self) -> None:
        self.is_clean = False

    def clean(self, staff_name: str = "anonymous") -> None:
        self.is_clean = True
        self.maintenance_required = False
        self.cleaning_log.append(staff_name)

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def log_access(self, user_id: str) -> None:
        self.access_log.append(user_id)

    def access_count(self) -> int:
        return len(self.access_log)

    def cleaning_count(self) -> int:
        return len(self.cleaning_log)

    def is_operational(self) -> bool:
        return not self.maintenance_required

    def reset(self) -> None:
        self.is_clean = True
        self.maintenance_required = False
        self.cleaning_log.clear()
        self.access_log.clear()

    def summary(self) -> str:
        status = "accessible" if self.is_accessible else "standard"
        return f"{self.location} restroom ({status})"
