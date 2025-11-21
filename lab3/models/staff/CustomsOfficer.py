from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from models.passenger.Passenger import Passenger

class CustomsOfficer:
    def __init__(self, name: str, officer_id: str) -> None:
        self.name: str = name
        self.officer_id: str = officer_id
        self.inspected_passengers: List[str] = []
        self.flagged_passengers: Dict[str, str] = {}
        self.notes: List[str] = []

    def inspect_passenger(self, passenger: Passenger) -> str:
        self.inspected_passengers.append(passenger.full_name)
        self.notes.append(f"Inspected {passenger.full_name}")
        return f"Customs inspection completed for {passenger.full_name}"

    def flag_passenger(self, passenger: Passenger, reason: str) -> None:
        self.flagged_passengers[passenger.full_name] = reason
        self.notes.append(f"Flagged {passenger.full_name}: {reason}")

    def has_inspected(self, passenger: Passenger) -> bool:
        return passenger.full_name in self.inspected_passengers

    def is_flagged(self, passenger: Passenger) -> bool:
        return passenger.full_name in self.flagged_passengers

    def summary(self) -> str:
        return (
            f"Officer {self.name} (ID: {self.officer_id})\n"
            f"- Total inspections: {len(self.inspected_passengers)}\n"
            f"- Flagged passengers: {len(self.flagged_passengers)}"
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "officer_id": self.officer_id,
            "inspected_passengers": self.inspected_passengers.copy(),
            "flagged_passengers": self.flagged_passengers.copy(),
            "notes": self.notes.copy()
        }

    def generate_flag_report(self) -> str:
        if not self.flagged_passengers:
            return f"No flagged passengers for Officer {self.name} (ID: {self.officer_id})"

        lines = [f"Flagged Passengers Report — Officer {self.name} (ID: {self.officer_id})"]
        for name, reason in self.flagged_passengers.items():
            lines.append(f"• {name}: {reason}")
        return "\n".join(lines)

    def reset_flags(self) -> None:
        count = len(self.flagged_passengers)
        self.flagged_passengers.clear()
        self.notes.append(f"Reset {count} flagged passenger(s) for new shift.")

    def archive_flags(self) -> dict[str, str]:
        if not hasattr(self, "flag_archive"):
            self.flag_archive: List[dict[str, str]] = []

        snapshot = self.flagged_passengers.copy()
        self.flag_archive.append(snapshot)
        self.notes.append(f"Archived {len(snapshot)} flagged passenger(s)")
        return snapshot

    def get_flag_archive(self) -> List[dict[str, str]]:
        if not hasattr(self, "flag_archive"):
            self.flag_archive: List[dict[str, str]] = []
        return self.flag_archive.copy()
