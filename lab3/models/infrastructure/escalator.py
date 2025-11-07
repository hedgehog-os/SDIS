from __future__ import annotations
from typing import List

class Escalator:
    VALID_DIRECTIONS = {"up", "down"}

    def __init__(self, escalator_id: str, direction: str) -> None:
        if direction not in self.VALID_DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")
        self.escalator_id: str = escalator_id
        self.direction: str = direction
        self.is_operational: bool = True
        self.maintenance_required: bool = False
        self.passenger_log: List[str] = []
        self.direction_history: List[str] = [direction]

    def stop(self) -> None:
        self.is_operational = False

    def start(self) -> None:
        self.is_operational = True

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def reverse_direction(self) -> None:
        self.direction = "down" if self.direction == "up" else "up"
        self.direction_history.append(self.direction)

    def board_passenger(self, name: str) -> None:
        self.passenger_log.append(name)

    def get_passenger_count(self) -> int:
        return len(self.passenger_log)

    def reset(self) -> None:
        self.is_operational = True
        self.maintenance_required = False
        self.passenger_log.clear()
        self.direction_history = [self.direction]

    def is_safe_to_use(self) -> bool:
        return self.is_operational and not self.maintenance_required

    def get_direction_changes(self) -> int:
        return len(self.direction_history) - 1

    def last_direction(self) -> str:
        return self.direction_history[-1]
