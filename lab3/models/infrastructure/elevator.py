from __future__ import annotations
from typing import List

class Elevator:
    def __init__(self, elevator_id: str, max_floor: int) -> None:
        self.elevator_id: str = elevator_id
        self.max_floor: int = max_floor
        self.current_floor: int = 0
        self.is_operational: bool = True
        self.passengers: List[str] = []
        self.maintenance_required: bool = False
        self.floor_history: List[int] = []

    def move_to_floor(self, floor: int) -> bool:
        if not self.is_operational or self.maintenance_required:
            return False
        if 0 <= floor <= self.max_floor:
            self.current_floor = floor
            self.floor_history.append(floor)
            return True
        return False

    def shutdown(self) -> None:
        self.is_operational = False

    def restart(self) -> None:
        self.is_operational = True

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def board_passenger(self, name: str) -> None:
        self.passengers.append(name)

    def disembark_passenger(self, name: str) -> bool:
        if name in self.passengers:
            self.passengers.remove(name)
            return True
        return False

    def is_empty(self) -> bool:
        return len(self.passengers) == 0

    def get_passenger_count(self) -> int:
        return len(self.passengers)

    def last_floor_visited(self) -> int | None:
        return self.floor_history[-1] if self.floor_history else None

    def reset(self) -> None:
        self.current_floor = 0
        self.floor_history.clear()
        self.passengers.clear()
        self.is_operational = True
        self.maintenance_required = False
