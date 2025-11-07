from __future__ import annotations
from typing import Optional, List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infrastructure.restroom import Restroom
class LostAndFoundReport:

    def __init__(self, item_description: str, location: Restroom, timestamp: str) -> None:
        self.location: Restroom = location
        self.item_description: str = item_description
        self.location: str = location.lower()
        self.timestamp: str = timestamp
        self.is_claimed: bool = False
        self.claimed_by: Optional[str] = None
        self.notes: List[str] = []

    def claim(self, claimant_name: str = "anonymous") -> None:
        self.is_claimed = True
        self.claimed_by = claimant_name

    def unclaim(self) -> None:
        self.is_claimed = False
        self.claimed_by = None

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def reset(self) -> None:
        self.is_claimed = False
        self.claimed_by = None
        self.notes.clear()

    def summary(self) -> str:
        status = "CLAIMED" if self.is_claimed else "UNCLAIMED"
        who = f" by {self.claimed_by}" if self.claimed_by else ""
        return (
            f"Item: '{self.item_description}' at {self.location} on {self.timestamp} — {status}{who}"
        )
