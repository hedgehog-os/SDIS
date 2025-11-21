from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.passenger.Baggage import Baggage

class BaggageHandler:
    def __init__(self, name: str, shift: str) -> None:
        self.name: str = name
        self.shift: str = shift
        self.handled_baggage: list[Baggage] = []
        self.notes: list[str] = []

    def load_baggage(self, baggage: Baggage) -> None:
        self.handled_baggage.append(baggage)
        self.notes.append(f"Loaded baggage {baggage.tag_number}")

    def unload_baggage(self, baggage: Baggage) -> None:
        if baggage in self.handled_baggage:
            self.handled_baggage.remove(baggage)
            self.notes.append(f"Unloaded baggage {baggage.tag_number}")

    def total_weight(self) -> float:
        return sum(b.weight_kg for b in self.handled_baggage)

    def fragile_items(self) -> list[Baggage]:
        return [b for b in self.handled_baggage if b.is_fragile]

    def baggage_by_owner(self, owner_name: str) -> list[Baggage]:
        return [b for b in self.handled_baggage if b.owner and b.owner.full_name == owner_name]

    def summary(self) -> str:
        return (
            f"Handler: {self.name} (Shift: {self.shift})\n"
            f"Handled baggage: {len(self.handled_baggage)} items\n"
            f"Total weight: {self.total_weight():.1f} kg\n"
            f"Fragile items: {len(self.fragile_items())}"
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "shift": self.shift,
            "handled_baggage_tags": [b.tag_number for b in self.handled_baggage],
            "notes": self.notes.copy()
        }

    def flag_overweight_items(self, limit: float) -> list[str]:
        flagged = []
        for baggage in self.handled_baggage:
            if baggage.weight_kg > limit:
                flagged.append(f"{baggage.tag_number} — {baggage.weight_kg:.1f} kg")
                self.notes.append(f"Flagged overweight baggage {baggage.tag_number} ({baggage.weight_kg:.1f} kg)")
        return flagged

    def generate_report(self) -> str:
        total = len(self.handled_baggage)
        fragile = len(self.fragile_items())
        overweight = len(self.flag_overweight_items(limit=23))  # стандартный лимит
        return (
            f"Report for {self.name} (Shift: {self.shift})\n"
            f"- Total baggage handled: {total}\n"
            f"- Total weight: {self.total_weight():.1f} kg\n"
            f"- Fragile items: {fragile}\n"
            f"- Overweight items (>23kg): {overweight}"
        )

    def assign_to_flight(self, flight_id: str) -> None:
        for baggage in self.handled_baggage:
            baggage.add_note(f"Assigned to flight {flight_id}")
        self.notes.append(f"All baggage assigned to flight {flight_id}")

    def group_by_owner(self) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = {}
        for baggage in self.handled_baggage:
            if baggage.owner:
                name = baggage.owner.full_name
                grouped.setdefault(name, []).append(baggage.tag_number)
            else:
                grouped.setdefault("Unassigned", []).append(baggage.tag_number)
        return grouped

    def generate_manifest(self) -> str:
        grouped = self.group_by_owner()
        lines = [f"Manifest for {self.name} (Shift: {self.shift})"]

        for owner, tags in grouped.items():
            lines.append(f"- {owner}: {len(tags)} item(s)")
            for tag in tags:
                lines.append(f"    • {tag}")
        
        return "\n".join(lines)
