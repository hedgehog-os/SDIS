from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.infrastructure.Restroom import Restroom
    from models.infrastructure.Lounge import Lounge

class CleaningCrew:
    def __init__(self, crew_id: str, shift: str) -> None:
        self.crew_id: str = crew_id
        self.shift: str = shift
        self.cleaned_restrooms: List[str] = []
        self.cleaned_lounges: List[str] = []
        self.notes: List[str] = []

    def clean_restroom(self, restroom: Restroom) -> None:
        restroom.clean()
        self.cleaned_restrooms.append(restroom.location_id)
        self.notes.append(f"Cleaned restroom {restroom.location_id}")

    def clean_lounge(self, lounge: Lounge) -> None:
        lounge.is_clean = True
        self.cleaned_lounges.append(lounge.name)
        self.notes.append(f"Cleaned lounge {lounge.name}")

    def total_cleaned(self) -> int:
        return len(self.cleaned_restrooms) + len(self.cleaned_lounges)

    def summary(self) -> str:
        return (
            f"Crew {self.crew_id} (Shift: {self.shift})\n"
            f"- Restrooms cleaned: {len(self.cleaned_restrooms)}\n"
            f"- Lounges cleaned: {len(self.cleaned_lounges)}\n"
            f"- Total tasks: {self.total_cleaned()}"
        )

    def to_dict(self) -> dict:
        return {
            "crew_id": self.crew_id,
            "shift": self.shift,
            "restrooms_cleaned": self.cleaned_restrooms.copy(),
            "lounges_cleaned": self.cleaned_lounges.copy(),
            "notes": self.notes.copy()
        }

    def generate_cleaning_report(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [f"Cleaning Report — Crew {self.crew_id} (Shift: {self.shift})", f"Generated at: {timestamp}"]

        if self.cleaned_restrooms:
            lines.append(f"\nRestrooms cleaned ({len(self.cleaned_restrooms)}):")
            for loc in self.cleaned_restrooms:
                lines.append(f"  • Restroom {loc}")

        if self.cleaned_lounges:
            lines.append(f"\nLounges cleaned ({len(self.cleaned_lounges)}):")
            for name in self.cleaned_lounges:
                lines.append(f"  • Lounge {name}")

        if not self.cleaned_restrooms and not self.cleaned_lounges:
            lines.append("\nNo cleaning tasks recorded.")

        return "\n".join(lines)

    def reset_tasks(self) -> None:
        cleared_restrooms = len(self.cleaned_restrooms)
        cleared_lounges = len(self.cleaned_lounges)
        self.cleaned_restrooms.clear()
        self.cleaned_lounges.clear()
        self.notes.append(
            f"Reset tasks: {cleared_restrooms} restroom(s), {cleared_lounges} lounge(s) cleared for new shift."
        )
