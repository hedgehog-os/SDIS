from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Sensor import Sensor


class Measurement:
    def __init__(self, value: float, unit: str, timestamp: Optional[datetime] = None, sensor: Optional["Sensor"] = None) -> None:
        self.value: float = value
        self.unit: str = unit
        self.timestamp: datetime = timestamp or datetime.now()
        self.sensor: Optional["Sensor"] = sensor

    def is_recent(self, threshold_minutes: int = 60) -> bool:
        """Проверяет, было ли измерение выполнено недавно."""
        from datetime import datetime, timedelta
        return self.timestamp >= datetime.now() - timedelta(minutes=threshold_minutes)

    def format_for_display(self) -> str:
        """Форматирует измерение для отображения."""
        sensor_info = f"Сенсор: {self.sensor.name}" if self.sensor else "Сенсор: —"
        return (
            f"Измерение: {self.value:.2f} {self.unit}\n"
            f"Дата: {self.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
            f"{sensor_info}"
        )

    def to_dict(self) -> dict:
        """Сериализует измерение в словарь."""
        return {
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "sensor_id": self.sensor.sensor_id if self.sensor else None
        }

    def is_from_sensor(self, sensor: "Sensor") -> bool:
        """Проверяет, связано ли измерение с указанным сенсором."""
        return self.sensor == sensor

