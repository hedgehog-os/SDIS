from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger

class SpecialAssistanceRequest:
    VALID_TYPES = {
        "wheelchair", "visual aid", "language support", "hearing aid", "escort", "medical"
    }

    def __init__(
        self,
        passenger: Passenger,
        request_type: str,
        description: str,
        is_confirmed: bool = False
    ) -> None:
        if request_type.lower() not in self.VALID_TYPES:
            raise ValueError(f"Invalid request type: {request_type}")
        self.passenger: Passenger = passenger
        self.request_type: str = request_type.lower()
        self.description: str = description.strip()
        self.is_confirmed: bool = is_confirmed
        self.assigned_staff: Optional[str] = None
        self.notes: list[str] = []

    def confirm(self) -> None:
        self.is_confirmed = True

    def cancel(self, reason: str = "Cancelled by passenger") -> None:
        self.is_confirmed = False
        self.notes.append(f"Cancelled: {reason}")

    def assign_staff(self, staff_name: str) -> None:
        self.assigned_staff = staff_name
        self.notes.append(f"Assigned to {staff_name}")

    def unassign_staff(self) -> None:
        if self.assigned_staff:
            self.notes.append(f"Unassigned from {self.assigned_staff}")
        self.assigned_staff = None

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def reset(self) -> None:
        self.is_confirmed = False
        self.assigned_staff = None
        self.notes.clear()

    def summary(self) -> str:
        status = "CONFIRMED" if self.is_confirmed else "PENDING"
        staff = f", Staff: {self.assigned_staff}" if self.assigned_staff else ""
        return (
            f"Assistance for {self.passenger.full_name} [{self.request_type}] — {status}{staff}. "
            f"Description: {self.description}"
        )
