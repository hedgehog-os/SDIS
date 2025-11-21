from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
from datetime import datetime

if TYPE_CHECKING:
    from models.passenger.Passenger import Passenger

class SecurityOfficer:
    def __init__(self, name: str, badge_id: str) -> None:
        self.name: str = name
        self.badge_id: str = badge_id
        self.inspected_passengers: List[str] = []
        self.flagged_passengers: Dict[str, str] = {}
        self.notes: List[str] = []
        self.inspection_log: List[Dict[str, str]] = []
        self.flag_archive: List[Dict[str, str]] = []

    def inspect_passenger(self, passenger: Passenger) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.inspected_passengers.append(passenger.full_name)
        self.inspection_log.append({
            "passenger": passenger.full_name,
            "passport": passenger.passport.number,
            "time": timestamp
        })
        self.notes.append(f"Inspected {passenger.full_name} at {timestamp}")
        return f"Security check completed for {passenger.full_name}"

    def flag_passenger(self, passenger: Passenger, reason: str) -> None:
        self.flagged_passengers[passenger.full_name] = reason
        self.notes.append(f"Flagged {passenger.full_name}: {reason}")

    def is_flagged(self, passenger: Passenger) -> bool:
        return passenger.full_name in self.flagged_passengers

    def get_flag_reason(self, passenger: Passenger) -> str | None:
        return self.flagged_passengers.get(passenger.full_name)

    def generate_flag_report(self) -> str:
        if not self.flagged_passengers:
            return f"No flagged passengers for Officer {self.name} (ID: {self.badge_id})"
        lines = [f"Flagged Passengers Report — Officer {self.name} (ID: {self.badge_id})"]
        for name, reason in self.flagged_passengers.items():
            lines.append(f"• {name}: {reason}")
        return "\n".join(lines)

    def archive_flags(self) -> None:
        snapshot = self.flagged_passengers.copy()
        self.flag_archive.append(snapshot)
        self.notes.append(f"Archived {len(snapshot)} flagged passenger(s)")
        self.flagged_passengers.clear()

    def get_flag_archive(self) -> List[Dict[str, str]]:
        return self.flag_archive.copy()

    def reset_inspections(self) -> None:
        cleared = len(self.inspection_log)
        self.inspected_passengers.clear()
        self.inspection_log.clear()
        self.notes.append(f"Reset {cleared} inspection(s) for new shift")

    def summary(self) -> str:
        return (
            f"{self.name} — Badge: {self.badge_id}, "
            f"Inspections: {len(self.inspection_log)}, "
            f"Flags: {len(self.flagged_passengers)}, "
            f"Archived snapshots: {len(self.flag_archive)}"
        )

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "badge_id": self.badge_id,
            "inspected_passengers": self.inspected_passengers.copy(),
            "flagged_passengers": self.flagged_passengers.copy(),
            "inspection_log": self.inspection_log.copy(),
            "notes": self.notes.copy(),
            "flag_archive": self.flag_archive.copy()
        }
