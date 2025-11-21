from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    
    from infrastructure.terminal import Terminal
class RetailShop:
    VALID_CATEGORIES = {
        "electronics", "clothing", "books", "souvenirs", "cosmetics",
        "toys", "food", "jewelry", "accessories", "pharmacy"
    }

    def __init__(self, name: str, category: str, terminal: Terminal) -> None:
        if category.lower() not in self.VALID_CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        self.name: str = name
        self.category: str = category.lower()
        self.terminal: Terminal = terminal
        self.is_open: bool = True
        self.maintenance_required: bool = False
        self.customer_log: List[str] = []
        self.inventory: List[str] = []

    def close(self) -> None:
        self.is_open = False

    def open(self) -> None:
        self.is_open = True

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def is_operational(self) -> bool:
        return self.is_open and not self.maintenance_required

    def log_customer(self, name: str) -> None:
        self.customer_log.append(name)

    def get_customer_count(self) -> int:
        return len(self.customer_log)

    def add_item(self, item: str) -> None:
        self.inventory.append(item)

    def remove_item(self, item: str) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def get_inventory(self) -> List[str]:
        return self.inventory.copy()

    def reset(self) -> None:
        self.is_open = True
        self.maintenance_required = False
        self.customer_log.clear()
        self.inventory.clear()

    def summary(self) -> str:
        return f"{self.name} ({self.category}) in Terminal {self.terminal_name}"
