from __future__ import annotations
from typing import List

class Lounge:
    def __init__(self, name: str, capacity: int, is_vip: bool = False) -> None:
        if capacity <= 0:
            raise ValueError("Lounge capacity must be positive.")
        self.name: str = name
        self.capacity: int = capacity
        self.is_vip: bool = is_vip
        self.current_occupancy: int = 0
        self.guest_log: List[str] = []
        self.maintenance_required: bool = False
        self.is_open: bool = True

    def admit_guest(self, guest_name: str = "anonymous") -> bool:
        if not self.is_open or self.maintenance_required:
            return False
        if self.current_occupancy < self.capacity:
            self.current_occupancy += 1
            self.guest_log.append(guest_name)
            return True
        return False

    def release_guest(self, guest_name: str = "anonymous") -> bool:
        if guest_name in self.guest_log:
            self.guest_log.remove(guest_name)
            self.current_occupancy = max(0, self.current_occupancy - 1)
            return True
        return False

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def close(self) -> None:
        self.is_open = False

    def open(self) -> None:
        self.is_open = True

    def is_available(self) -> bool:
        return self.is_open and not self.maintenance_required and self.current_occupancy < self.capacity

    def occupancy_rate(self) -> float:
        return round(self.current_occupancy / self.capacity, 2)

    def reset(self) -> None:
        self.current_occupancy = 0
        self.guest_log.clear()
        self.maintenance_required = False
        self.is_open = True

    def get_guest_list(self) -> List[str]:
        return self.guest_log.copy()

    def is_guest_present(self, guest_name: str) -> bool:
        return guest_name in self.guest_log
