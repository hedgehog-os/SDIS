from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger

class Visa:
    def __init__(self, country: str, visa_type: str, expiration_date: str) -> None:
        self.country: str = country
        self.visa_type: str = visa_type
        self.expiration_date: str = expiration_date  # format: "YYYY-MM-DD"
        self.holder: Optional[Passenger] = None
        self.notes: list[str] = []

    def is_valid(self, current_date: str) -> bool:
        try:
            current = datetime.strptime(current_date, "%Y-%m-%d")
            expiry = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            return current < expiry
        except ValueError:
            self.notes.append(f"Invalid date format: {current_date}")
            return False

    def assign_holder(self, passenger: Passenger) -> None:
        self.holder = passenger
        self.notes.append(f"Assigned to {passenger.full_name}")

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def get_expiry_status(self, current_date: str, threshold_days: int = 90) -> str:
        try:
            current = datetime.strptime(current_date, "%Y-%m-%d")
            expiry = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            if current >= expiry:
                return "Expired"
            elif (expiry - current).days <= threshold_days:
                return "Expiring Soon"
            else:
                return "Valid"
        except ValueError:
            return "Unknown"

    def to_dict(self) -> dict:
        return {
            "country": self.country,
            "visa_type": self.visa_type,
            "expiration_date": self.expiration_date,
            "holder_name": self.holder.full_name if self.holder else None,
            "notes": self.notes.copy()
        }

    def summary(self) -> str:
        status = self.get_expiry_status(datetime.today().strftime("%Y-%m-%d"))
        holder = self.holder.full_name if self.holder else "Unassigned"
        return (
            f"Visa for {self.country} ({self.visa_type}) — {status}, "
            f"Expires: {self.expiration_date}, Holder: {holder}"
        )
