from __future__ import annotations
from typing import List

class ShuttleBus:
    VALID_ROUTES = {
        "terminal loop",
        "parking shuttle",
        "hotel transfer",
        "inter-terminal",
        "remote gate",
        "staff only"
    }

    def __init__(self, bus_id: str, route_name: str, capacity: int) -> None:
        if route_name.lower() not in self.VALID_ROUTES:
            raise ValueError(f"Invalid route name: {route_name}")
        if capacity <= 0:
            raise ValueError("Bus capacity must be positive.")
        self.bus_id: str = bus_id
        self.route_name: str = route_name.lower()
        self.capacity: int = capacity
        self.passengers_onboard: int = 0
        self.is_operational: bool = True
        self.maintenance_required: bool = False
        self.passenger_log: List[str] = []

    def board_passenger(self, passenger_id: str = "anonymous") -> bool:
        if not self.is_operational or self.maintenance_required:
            return False
        if self.passengers_onboard < self.capacity:
            self.passengers_onboard += 1
            self.passenger_log.append(passenger_id)
            return True
        return False

    def disembark_passenger(self, passenger_id: str = "anonymous") -> bool:
        if passenger_id in self.passenger_log:
            self.passenger_log.remove(passenger_id)
            self.passengers_onboard = max(0, self.passengers_onboard - 1)
            return True
        return False

    def mark_for_maintenance(self) -> None:
        self.maintenance_required = True

    def clear_maintenance(self) -> None:
        self.maintenance_required = False

    def shutdown(self) -> None:
        self.is_operational = False

    def restart(self) -> None:
        self.is_operational = True

    def is_available(self) -> bool:
        return self.is_operational and not self.maintenance_required and self.passengers_onboard < self.capacity

    def occupancy_rate(self) -> float:
        return round(self.passengers_onboard / self.capacity, 2)

    def reset(self) -> None:
        self.passengers_onboard = 0
        self.passenger_log.clear()
        self.is_operational = True
        self.maintenance_required = False

    def get_passenger_list(self) -> List[str]:
        return self.passenger_log.copy()

    def summary(self) -> str:
        status = "active" if self.is_operational else "offline"
        return f"Bus {self.bus_id} on '{self.route_name}' route ({self.passengers_onboard}/{self.capacity}, {status})"
