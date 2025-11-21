from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.passenger.Passenger import Passenger

class Baggage:
    def __init__(self, tag_number: str, weight_kg: float, is_fragile: bool) -> None:
        self.tag_number: str = tag_number
        self.weight_kg: float = weight_kg
        self.is_fragile: bool = is_fragile
        self.owner: Passenger | None = None
        self.notes: list[str] = []
        self.is_checked_in: bool = False

    def assign_owner(self, passenger: Passenger) -> None:
        self.owner = passenger
        self.notes.append(f"Assigned to {passenger.full_name}")

    def exceeds_limit(self, limit: float) -> bool:
        return self.weight_kg > limit

    def mark_fragile(self) -> None:
        self.is_fragile = True
        self.notes.append("Marked as fragile")

    def unmark_fragile(self) -> None:
        self.is_fragile = False
        self.notes.append("Unmarked as fragile")

    def check_in(self) -> None:
        self.is_checked_in = True
        self.notes.append("Checked in")

    def uncheck(self) -> None:
        self.is_checked_in = False
        self.notes.append("Unchecked")

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def summary(self) -> str:
        status = "Checked-in" if self.is_checked_in else "Pending"
        fragility = "Fragile" if self.is_fragile else "Standard"
        owner = self.owner.full_name if self.owner else "Unassigned"
        return (
            f"Baggage {self.tag_number}: {self.weight_kg:.1f} kg, {fragility}, "
            f"{status}, Owner: {owner}"
        )
