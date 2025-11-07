from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.staff.maintenance_technician import MaintenanceTechnician
    from models.operations.maintenance_log import MaintenanceLog
    from models.operations.fuel_record import FuelRecord
    from models.flight.flight import Flight

class Aircraft:
    def __init__(self, model: str, registration_number: str, capacity: int) -> None:
        self.model: str = model
        self.registration_number: str = registration_number
        self.capacity: int = capacity
        self.maintenance_logs: list[MaintenanceLog] = []
        self.fuel_records: list[FuelRecord] = []
        self.assigned_flights: list[Flight] = []

    # Проверка регистрации
    def is_valid_registration(self) -> bool:
        return self.registration_number.startswith("N") or self.registration_number[:2].isalpha()

    # Назначение рейса
    def assign_flight(self, flight: Flight) -> None:
        self.assigned_flights.append(flight)

    # Получение последнего рейса
    def get_last_flight(self) -> Flight | None:
        return self.assigned_flights[-1] if self.assigned_flights else None

    # Добавление записи о техобслуживании
    def log_maintenance(self, log: MaintenanceLog) -> None:
        self.maintenance_logs.append(log)

    # Получение последней проверки
    def last_maintenance(self) -> MaintenanceLog | None:
        return self.maintenance_logs[-1] if self.maintenance_logs else None

    # Проверка, обслуживался ли техник
    def was_inspected_by(self, technician: MaintenanceTechnician) -> bool:
        return any(log.technician == technician for log in self.maintenance_logs)

    # Заправка
    def refuel(self, record: FuelRecord) -> None:
        self.fuel_records.append(record)

    # Получение общего объема топлива
    def total_fuel_loaded(self) -> float:
        return sum(r.fuel_liters for r in self.fuel_records)

    # Проверка перегрузки
    def is_overbooked(self, passenger_count: int) -> bool:
        return passenger_count > self.capacity

    # Получение модели и регистрации
    def summary(self) -> str:
        return f"{self.model} ({self.registration_number})"
