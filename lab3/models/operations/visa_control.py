from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger
    from models.passenger.visa import Visa

class VisaControl:
    def __init__(self, country: str) -> None:
        self.country: str = country
        self.verified_passengers: List[str] = []
        self.failed_passengers: List[str] = []
        self.audit_log: List[str] = []


    def verify(self, passenger: Passenger, date: str = "2025-11-04") -> bool:
        visas: list[Visa] = getattr(passenger, "visas", [])
        for visa in visas:
            if visa.country == self.country and visa.is_valid(date):
                return True
        return False

    def has_been_verified(self, passenger: Passenger) -> bool:
        return passenger.full_name in self.verified_passengers

    def has_failed_verification(self, passenger: Passenger) -> bool:
        return passenger.full_name in self.failed_passengers

    def reset(self) -> None:
        self.verified_passengers.clear()
        self.failed_passengers.clear()
        self.audit_log.clear()

    def summary(self) -> str:
        return (
            f"VisaControl for {self.country}: "
            f"{len(self.verified_passengers)} verified, "
            f"{len(self.failed_passengers)} denied"
        )

    def get_audit_log(self) -> List[str]:
        return self.audit_log.copy()
