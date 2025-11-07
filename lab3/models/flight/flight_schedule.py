from __future__ import annotations
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.flight.flight import Flight

class FlightSchedule:
    def __init__(self, departure_time: str, arrival_time: str, is_recurring: bool = False) -> None:
        self.departure_time: str = departure_time
        self.arrival_time: str = arrival_time
        self.is_recurring: bool = is_recurring
        self.associated_flight: Flight | None = None

    def duration_minutes(self) -> int:
        fmt = "%Y-%m-%d %H:%M"
        dep = datetime.strptime(self.departure_time, fmt)
        arr = datetime.strptime(self.arrival_time, fmt)
        return int((arr - dep).total_seconds() // 60)

    def overlaps_with(self, other: FlightSchedule) -> bool:
        fmt = "%Y-%m-%d %H:%M"
        dep1 = datetime.strptime(self.departure_time, fmt)
        arr1 = datetime.strptime(self.arrival_time, fmt)
        dep2 = datetime.strptime(other.departure_time, fmt)
        arr2 = datetime.strptime(other.arrival_time, fmt)
        return max(dep1, dep2) < min(arr1, arr2)

    def assign_flight(self, flight: Flight) -> None:
        self.associated_flight = flight

    def is_night_flight(self) -> bool:
        fmt = "%Y-%m-%d %H:%M"
        dep = datetime.strptime(self.departure_time, fmt).hour
        return dep >= 22 or dep < 6

    def is_long_haul(self) -> bool:
        return self.duration_minutes() > 360

    def shift_by_minutes(self, minutes: int) -> None:
        fmt = "%Y-%m-%d %H:%M"
        dep = datetime.strptime(self.departure_time, fmt) + timedelta(minutes=minutes)
        arr = datetime.strptime(self.arrival_time, fmt) + timedelta(minutes=minutes)
        self.departure_time = dep.strftime(fmt)
        self.arrival_time = arr.strftime(fmt)

    def is_departing_today(self) -> bool:
        fmt = "%Y-%m-%d %H:%M"
        dep_date = datetime.strptime(self.departure_time, fmt).date()
        return dep_date == datetime.today().date()

    def get_day_of_week(self) -> str:
        fmt = "%Y-%m-%d %H:%M"
        dep = datetime.strptime(self.departure_time, fmt)
        return dep.strftime("%A")

    def is_valid_range(self) -> bool:
        fmt = "%Y-%m-%d %H:%M"
        dep = datetime.strptime(self.departure_time, fmt)
        arr = datetime.strptime(self.arrival_time, fmt)
        return arr > dep
