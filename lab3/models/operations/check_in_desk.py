from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models.passenger.passenger import Passenger
    from models.infrastructure.terminal import Terminal

class CheckInDesk:
    def __init__(self, desk_id: str, terminal: Terminal) -> None:
        self.desk_id: str = desk_id
        self.terminal: Terminal = terminal
        self.queue: list[Passenger] = []

        self.is_operational: bool = True
        self.maintenance_required: bool = False
        self.processed_log: List[str] = []

    def add_to_queue(self, passenger: Passenger) -> None:
        if self.is_operational and not self.maintenance_required:
            self.queue.append(passenger)

    def process_next(self) -> Passenger | None:
        if not self.queue or not self.is_operational or self.maintenance_required:
            return None
        passenger = self.queue.pop(0)
        self.processed_log.append(passenger.full_name)
        return passenger

    def is_busy(self) -> bool:
        return len(self.queue) > 5

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def shutdown(self) -> None:
        self.is_operational = False

    def restart(self) -> None:
        self.is_operational = True

    def reset(self) -> None:
        self.queue.clear()
        self.processed_log.clear()
        self.is_operational = True
        self.maintenance_required = False

    def get_queue_size(self) -> int:
        return len(self.queue)

    def get_processed_count(self) -> int:
        return len(self.processed_log)

    def summary(self) -> str:
        status = "active" if self.is_operational else "offline"
        return f"Desk {self.desk_id} in Terminal {self.terminal.name} ({status}, {len(self.queue)} in queue)"

