from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger

class CustomsDeclaration:
    THRESHOLD_USD = 1000.0
    PROHIBITED_ITEMS = {"firearms", "explosives", "narcotics", "radioactive", "endangered species"}

    def __init__(self, passenger: Passenger, declared_items: list[str], total_value_usd: float) -> None:
        if total_value_usd < 0:
            raise ValueError("Total value cannot be negative.")
        self.passenger: Passenger = passenger
        self.declared_items: List[str] = declared_items
        self.total_value_usd: float = total_value_usd
        self.flagged_items: List[str] = []
        self.reviewed: bool = False

    def is_required(self) -> bool:
        return self.total_value_usd > self.THRESHOLD_USD or bool(self.declared_items)

    def add_item(self, item: str, value: float) -> None:
        if value <= 0:
            raise ValueError("Item value must be positive.")
        self.declared_items.append(item)
        self.total_value_usd += value
        if item.lower() in self.PROHIBITED_ITEMS:
            self.flagged_items.append(item)

    def remove_item(self, item: str, value: float) -> bool:
        if item in self.declared_items:
            self.declared_items.remove(item)
            self.total_value_usd = max(0.0, self.total_value_usd - value)
            if item in self.flagged_items:
                self.flagged_items.remove(item)
            return True
        return False

    def has_prohibited_items(self) -> bool:
        return bool(self.flagged_items)

    def mark_reviewed(self) -> None:
        self.reviewed = True

    def reset(self) -> None:
        self.declared_items.clear()
        self.total_value_usd = 0.0
        self.flagged_items.clear()
        self.reviewed = False

    def summary(self) -> str:
        status = "REVIEWED" if self.reviewed else "PENDING"
        return (
            f"Customs for {self.passenger.full_name}: "
            f"{len(self.declared_items)} items, ${self.total_value_usd:.2f}, {status}"
        )
