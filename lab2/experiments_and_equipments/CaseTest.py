from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Measurement import Measurement
    from experiments_and_equipments.Procedure import Procedure
    from experiments_and_equipments.Sensor import Sensor


class CaseTest:
    def __init__(self,
                 testcase_id: int,
                 name: str,
                 description: str,
                 created_at: Optional[datetime] = None,
                 procedure: Optional["Procedure"] = None,
                 measurements: Optional[List["Measurement"]] = None) -> None:
        self.testcase_id: int = testcase_id
        self.name: str = name
        self.description: str = description
        self.created_at: datetime = created_at or datetime.now()

        # Ассоциация
        self.procedure: Optional["Procedure"] = procedure
        self.measurements: Optional[List["Measurement"]] = measurements

    def add_measurement(self, measurement: "Measurement") -> None:
        """Добавляет измерение к тест-кейсу."""
        if self.measurements is None:
            self.measurements = []
        self.measurements.append(measurement)

    def remove_measurement(self, measurement: "Measurement") -> None:
        """Удаляет измерение из тест-кейса."""
        if self.measurements and measurement in self.measurements:
            self.measurements.remove(measurement)

    def get_recent_measurements(self, minutes: int = 60) -> List["Measurement"]:
        """Возвращает измерения, сделанные за последние N минут."""
        if not self.measurements:
            return []
        return [m for m in self.measurements if m.is_recent(minutes)]

    def get_measurements_by_unit(self, unit: str) -> List["Measurement"]:
        """Фильтрует измерения по единице измерения."""
        if not self.measurements:
            return []
        return [m for m in self.measurements if m.unit == unit]

    def get_measurements_from_sensor(self, sensor: "Sensor") -> List["Measurement"]:
        """Возвращает измерения, сделанные указанным сенсором."""
        if not self.measurements:
            return []
        return [m for m in self.measurements if m.is_from_sensor(sensor)]

    def summarize(self) -> str:
        """Форматирует краткую информацию о тест-кейсе."""
        return (
            f"Тест-кейс #{self.testcase_id}: {self.name}\n"
            f"Описание: {self.description}\n"
            f"Дата создания: {self.created_at.strftime('%Y-%m-%d')}\n"
            f"Процедура: {self.procedure.name if self.procedure else '—'}\n"
            f"Измерений: {len(self.measurements or [])}"
        )

    def to_dict(self) -> dict:
        """Сериализует тест-кейс в словарь."""
        return {
            "testcase_id": self.testcase_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "procedure_id": self.procedure.procedure_id if self.procedure else None,
            "measurement_count": len(self.measurements or [])
        }
