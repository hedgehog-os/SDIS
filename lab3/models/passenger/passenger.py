from __future__ import annotations
from exceptions import InvalidPassportException
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from models.passenger.passport import Passport
    from models.passenger.ticket import Ticket
    from models.passenger.baggage import Baggage
    from models.passenger.visa import Visa
    from models.passenger.loyalty_program import LoyaltyProgram

class Passenger:
    def __init__(self, full_name: str, passport: Passport, ticket: Ticket) -> None:
        self.full_name: str = full_name
        self.passport: Passport = passport
        self.ticket: Ticket = ticket
        self.baggage: List[Baggage] = []
        self.visas: List[Visa] = []
        self.loyalty_program: Optional[LoyaltyProgram] = None
        self.notes: List[str] = []

    def add_baggage(self, item: Baggage) -> None:
        self.baggage.append(item)

    def total_baggage_weight(self) -> float:
        return sum(b.weight_kg for b in self.baggage)

    def overweight_baggage(self, limit_kg: float) -> List[Baggage]:
        return [b for b in self.baggage if b.weight_kg > limit_kg]

    def validate_passport(self, current_date: str) -> None:
        if not self.passport.is_valid(current_date):
            raise InvalidPassportException(self.passport.number)

    def add_visa(self, visa: Visa) -> None:
        self.visas.append(visa)

    def has_valid_visa_for(self, country: str, date: str) -> bool:
        return any(v.country == country and v.is_valid(date) for v in self.visas)

    def get_expired_visas(self, date: str) -> List[Visa]:
        return [v for v in self.visas if not v.is_valid(date)]

    def get_valid_visas(self, date: str) -> List[Visa]:
        return [v for v in self.visas if v.is_valid(date)]

    def enroll_loyalty_program(self, program: LoyaltyProgram) -> None:
        self.loyalty_program = program
        program.assign_owner(self.full_name)

    def add_loyalty_points(self, amount: int, reason: str = "Flight activity") -> None:
        if self.loyalty_program:
            self.loyalty_program.add_points(amount, reason)

    def redeem_loyalty_points(self, amount: int, reason: str = "Upgrade") -> bool:
        if self.loyalty_program:
            return self.loyalty_program.redeem_points(amount, reason)
        return False

    def get_loyalty_status(self) -> str:
        if not self.loyalty_program:
            return "Not enrolled"
        return f"{self.loyalty_program.tier} — {self.loyalty_program.points} points"

    def is_ready_for_boarding(self, destination_country: str, current_date: str, baggage_limit_kg: float) -> bool:
        try:
            self.validate_passport(current_date)
        except InvalidPassportException:
            return False

        if not self.has_valid_visa_for(destination_country, current_date):
            return False

        if self.total_baggage_weight() > baggage_limit_kg:
            return False

        return True

    def boarding_issues(self, destination_country: str, current_date: str, baggage_limit_kg: float) -> List[str]:
        issues: List[str] = []

        if not self.passport.is_valid(current_date):
            issues.append("Passport is invalid or expired.")

        if not self.has_valid_visa_for(destination_country, current_date):
            issues.append(f"No valid visa for {destination_country}.")

        if self.total_baggage_weight() > baggage_limit_kg:
            overweight = self.total_baggage_weight() - baggage_limit_kg
            issues.append(f"Baggage exceeds limit by {overweight:.1f} kg.")

        return issues

    def auto_notify(self, destination_country: str, current_date: str, baggage_limit_kg: float) -> str:
        issues = self.boarding_issues(destination_country, current_date, baggage_limit_kg)
        if not issues:
            return f"{self.full_name} is cleared for boarding to {destination_country}."
        
        issue_list = "; ".join(issues)
        return f"{self.full_name} cannot board: {issue_list}"

    def check_in_summary(self, destination_country: str, current_date: str, baggage_limit_kg: float) -> str:
        return (
            f"Passenger: {self.full_name}\n"
            f"Passport: {'Valid' if self.passport.is_valid(current_date) else 'Invalid'}\n"
            f"Visa for {destination_country}: {'Yes' if self.has_valid_visa_for(destination_country, current_date) else 'No'}\n"
            f"Baggage: {self.total_baggage_weight():.1f} kg (Limit: {baggage_limit_kg:.1f} kg)\n"
            f"Loyalty: {self.get_loyalty_status()}\n"
            f"Ready for boarding: {'Yes' if self.is_ready_for_boarding(destination_country, current_date, baggage_limit_kg) else 'No'}"
        )

    def summary(self) -> str:
        return (
            f"{self.full_name} — Passport: {self.passport.number}, "
            f"Ticket: {self.ticket.code}, "
            f"Baggage: {len(self.baggage)} items ({self.total_baggage_weight():.1f} kg), "
            f"Visas: {len(self.visas)}, Loyalty: {self.get_loyalty_status()}"
        )

    def get_visa_summary(self, current_date: str) -> str:
        if not self.visas:
            return "No visas assigned."

        lines = []
        for visa in self.visas:
            status = visa.get_expiry_status(current_date)
            lines.append(f"- {visa.country} ({visa.visa_type}) — {status}, expires {visa.expiration_date}")
        return "\n".join(lines)

    def get_visa_for_country(self, country: str) -> Optional[Visa]:
        for visa in self.visas:
            if visa.country == country:
                return visa
        return None

    def remove_expired_visas(self, current_date: str) -> None:
        before = len(self.visas)
        self.visas = [v for v in self.visas if v.is_valid(current_date)]
        after = len(self.visas)
        removed = before - after
        if removed > 0:
            print(f"{removed} expired visa(s) removed for {self.full_name}.")

    def to_dict(self) -> dict:
            return {
                "full_name": self.full_name,
                "passport_number": self.passport.number,
                "ticket_code": self.ticket.code,
                "baggage_tags": [b.tag_number for b in self.baggage],
                "total_baggage_weight": self.total_baggage_weight(),
                "valid_visas": [v.country for v in self.visas if v.is_valid("2025-11-06")],
                "loyalty_status": self.get_loyalty_status(),
                "notes": self.notes.copy()
            }