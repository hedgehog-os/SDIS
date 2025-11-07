from __future__ import annotations
from datetime import datetime
from typing import Optional

class Passport:
    def __init__(self, number: str, nationality: str, expiration_date: str) -> None:
        self.number: str = number
        self.nationality: str = nationality
        self.expiration_date: str = expiration_date
        self.owner_name: Optional[str] = None
        self.notes: list[str] = []

    def is_valid(self, current_date: str) -> bool:
        try:
            current = datetime.strptime(current_date, "%Y-%m-%d")
            expiry = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            return current < expiry
        except ValueError:
            self.notes.append(f"Invalid date format: {current_date}")
            return False

    def days_until_expiry(self, current_date: str) -> int:
        try:
            current = datetime.strptime(current_date, "%Y-%m-%d")
            expiry = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            return max((expiry - current).days, 0)
        except ValueError:
            return 0

    def assign_owner(self, full_name: str) -> None:
        self.owner_name = full_name
        self.notes.append(f"Assigned to {full_name}")

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def summary(self) -> str:
        status = "Valid" if self.is_valid(datetime.today().strftime("%Y-%m-%d")) else "Expired"
        owner = self.owner_name or "Unassigned"
        return (
            f"Passport {self.number} ({self.nationality}) — {status}, "
            f"Expires: {self.expiration_date}, Owner: {owner}"
        )

    def requires_renewal_notice(self, current_date: str, threshold_days: int = 90) -> bool:
        try:
            current = datetime.strptime(current_date, "%Y-%m-%d")
            expiry = datetime.strptime(self.expiration_date, "%Y-%m-%d")
            remaining_days = (expiry - current).days
            return 0 < remaining_days <= threshold_days
        except ValueError:
            self.notes.append(f"Invalid date format: {current_date}")
            return False

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
            self.notes.append(f"Invalid date format: {current_date}")
            return "Unknown"

    def flag_if_expired(self, current_date: str) -> bool:
        if not self.is_valid(current_date):
            self.notes.append("Passport flagged as expired.")
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "nationality": self.nationality,
            "expiration_date": self.expiration_date,
            "owner_name": self.owner_name,
            "notes": self.notes.copy()
        }
