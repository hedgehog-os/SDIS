from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
from datetime import datetime

if TYPE_CHECKING:
    from models.flight.flight import Flight

class Dispatcher:
    def __init__(self, name: str, dispatch_id: str) -> None:
        self.name: str = name
        self.dispatch_id: str = dispatch_id
        self.dispatched_flights: List[str] = []
        self.dispatch_log: List[Dict[str, str]] = []
        self.notes: List[str] = []
        self.archive: List[List[Dict[str, str]]] = []

    def dispatch_flight(self, flight: Flight) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.dispatched_flights.append(flight.flight_number)
        self.dispatch_log.append({
            "flight": flight.flight_number,
            "destination": flight.destination,
            "time": timestamp
        })
        self.notes.append(f"Dispatched flight {flight.flight_number} to {flight.destination} at {timestamp}")
        return f"Dispatcher {self.name} dispatched flight {flight.flight_number}"

    def has_dispatched(self, flight: Flight) -> bool:
        return flight.flight_number in self.dispatched_flights

    def total_dispatched(self) -> int:
        return len(self.dispatched_flights)

    def get_last_dispatch(self) -> str:
        return self.dispatched_flights[-1] if self.dispatched_flights else "None"

    def get_dispatches_by_destination(self, destination: str) -> List[str]:
        return [entry["flight"] for entry in self.dispatch_log if entry["destination"] == destination]

    def generate_dispatch_report(self) -> str:
        lines = [f"Dispatch Report — {self.name} (ID: {self.dispatch_id})"]
        lines.append(f"Total dispatched: {self.total_dispatched()}")
        for entry in self.dispatch_log:
            lines.append(f"• {entry['flight']} → {entry['destination']} at {entry['time']}")
        return "\n".join(lines)

    def reset_log(self) -> None:
        self.notes.append(f"Reset log with {len(self.dispatch_log)} entries")
        self.dispatched_flights.clear()
        self.dispatch_log.clear()

    def archive_log(self) -> None:
        self.archive.append(self.dispatch_log.copy())
        self.notes.append(f"Archived {len(self.dispatch_log)} dispatch entries")

    def get_archive(self) -> List[List[Dict[str, str]]]:
        return self.archive.copy()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "dispatch_id": self.dispatch_id,
            "dispatched_flights": self.dispatched_flights.copy(),
            "dispatch_log": self.dispatch_log.copy(),
            "notes": self.notes.copy(),
            "archive_count": len(self.archive)
        }

    def summary(self) -> str:
        return (
            f"Dispatcher {self.name} (ID: {self.dispatch_id})\n"
            f"- Total flights dispatched: {self.total_dispatched()}\n"
            f"- Last dispatched: {self.get_last_dispatch()}\n"
            f"- Archive snapshots: {len(self.archive)}"
        )
