from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger

class SecurityCheck:
    def __init__(self, checkpoint_id: str) -> None:
        self.checkpoint_id: str = checkpoint_id
        self.checked_passengers: List[str] = []
        self.flagged_passengers: List[str] = []
        self.blocked_passengers: List[str] = []
        self.notes: List[str] = []
        self.is_operational: bool = True

    def perform_check(self, passenger: Passenger) -> str:
        if not self.is_operational:
            return f"Checkpoint {self.checkpoint_id} is currently offline."
        if passenger.full_name in self.blocked_passengers:
            return f"Passenger {passenger.full_name} is blocked from passing checkpoint {self.checkpoint_id}."
        if passenger.full_name in self.checked_passengers:
            return f"Passenger {passenger.full_name} has already been checked."
        self.checked_passengers.append(passenger.full_name)
        return f"Passenger {passenger.full_name} cleared at checkpoint {self.checkpoint_id}"

    def has_been_checked(self, passenger: Passenger) -> bool:
        return passenger.full_name in self.checked_passengers

    def flag_passenger(self, passenger: Passenger, reason: str) -> None:
        if passenger.full_name not in self.flagged_passengers:
            self.flagged_passengers.append(passenger.full_name)
            self.notes.append(f"Flagged {passenger.full_name}: {reason}")

    def block_passenger(self, passenger: Passenger, reason: str) -> None:
        if passenger.full_name not in self.blocked_passengers:
            self.blocked_passengers.append(passenger.full_name)
            self.notes.append(f"Blocked {passenger.full_name}: {reason}")

    def reset(self) -> None:
        self.checked_passengers.clear()
        self.flagged_passengers.clear()
        self.blocked_passengers.clear()
        self.notes.clear()
        self.is_operational = True

    def shutdown(self) -> None:
        self.is_operational = False

    def restart(self) -> None:
        self.is_operational = True

    def summary(self) -> str:
        status = "ACTIVE" if self.is_operational else "OFFLINE"
        return (
            f"Checkpoint {self.checkpoint_id}: {len(self.checked_passengers)} checked, "
            f"{len(self.flagged_passengers)} flagged, {len(self.blocked_passengers)} blocked — {status}"
        )
