from __future__ import annotations
from typing import List

class CargoManifest:
    VALID_ITEM_TYPES = {
        "luggage", "mail", "equipment", "food", "medical", "electronics",
        "documents", "tools", "spare parts", "hazardous"
    }

    MAX_TOTAL_WEIGHT_KG = 50000.0

    def __init__(self, manifest_id: str, items: list[str], total_weight_kg: float) -> None:
        if total_weight_kg < 0 or total_weight_kg > self.MAX_TOTAL_WEIGHT_KG:
            raise ValueError(f"Invalid total weight: {total_weight_kg} kg")
        for item in items:
            if item.lower() not in self.VALID_ITEM_TYPES:
                raise ValueError(f"Invalid item type: {item}")
        self.manifest_id: str = manifest_id
        self.items: List[str] = [item.lower() for item in items]
        self.total_weight_kg: float = total_weight_kg
        self.weight_log: List[float] = []

    def add_item(self, item: str, weight: float) -> None:
        if item.lower() not in self.VALID_ITEM_TYPES:
            raise ValueError(f"Invalid item type: {item}")
        if weight <= 0:
            raise ValueError("Weight must be positive.")
        if self.total_weight_kg + weight > self.MAX_TOTAL_WEIGHT_KG:
            raise ValueError("Exceeds maximum cargo weight limit.")
        self.items.append(item.lower())
        self.total_weight_kg += weight
        self.weight_log.append(weight)

    def remove_item(self, item: str) -> bool:
        item = item.lower()
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def reset(self) -> None:
        self.items.clear()
        self.total_weight_kg = 0.0
        self.weight_log.clear()

    def get_item_count(self) -> int:
        return len(self.items)

    def get_weight_log(self) -> List[float]:
        return self.weight_log.copy()

    def is_overloaded(self) -> bool:
        return self.total_weight_kg > self.MAX_TOTAL_WEIGHT_KG

    def summary(self) -> str:
        return f"Manifest {self.manifest_id}: {len(self.items)} items, {self.total_weight_kg:.2f} kg"
