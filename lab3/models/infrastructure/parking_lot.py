from __future__ import annotations
from typing import List

class ParkingLot:
    def __init__(self, lot_id: str, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Parking lot capacity must be positive.")
        self.lot_id: str = lot_id
        self.capacity: int = capacity
        self.occupied: int = 0
        self.is_open: bool = True
        self.maintenance_required: bool = False
        self.vehicle_log: List[str] = []

    def park_vehicle(self, vehicle_id: str = "anonymous") -> bool:
        if not self.is_open or self.maintenance_required:
            return False
        if self.occupied < self.capacity:
            self.occupied += 1
            self.vehicle_log.append(vehicle_id)
            return True
        return False

    def release_vehicle(self, vehicle_id: str = "anonymous") -> bool:
        if vehicle_id in self.vehicle_log:
            self.vehicle_log.remove(vehicle_id)
            self.occupied = max(0, self.occupied - 1)
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
        return self.is_open and not self.maintenance_required and self.occupied < self.capacity

    def occupancy_rate(self) -> float:
        return round(self.occupied / self.capacity, 2)

    def reset(self) -> None:
        self.occupied = 0
        self.vehicle_log.clear()
        self.is_open = True
        self.maintenance_required = False

    def get_vehicle_list(self) -> List[str]:
        return self.vehicle_log.copy()

    def is_vehicle_present(self, vehicle_id: str) -> bool:
        return vehicle_id in self.vehicle_log
