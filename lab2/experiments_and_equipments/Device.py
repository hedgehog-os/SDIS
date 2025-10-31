from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Calibration import Calibration


class Device:
    def __init__(self, device_id: int, name: str, calibration: Optional["Calibration"] = None) -> None:
        self.device_id: int = device_id
        self.name: str = name
        self.calibration: Optional["Calibration"] = calibration

    def assign_calibration(self, calibration: "Calibration") -> None:
        """Привязывает калибровку к устройству."""
        self.calibration = calibration

    def clear_calibration(self) -> None:
        """Удаляет текущую калибровку."""
        self.calibration = None

    def is_calibrated(self) -> bool:
        """Проверяет, есть ли у устройства действующая калибровка."""
        return self.calibration is not None

    def was_calibrated_recently(self, days: int = 30) -> bool:
        """Проверяет, была ли калибровка проведена в последние N дней."""
        from datetime import datetime, timedelta
        if not self.calibration:
            return False
        return self.calibration.date >= datetime.now() - timedelta(days=days)

    def get_calibration_summary(self) -> str:
        """Возвращает краткую информацию о калибровке."""
        if not self.calibration:
            return "Нет данных о калибровке."
        return (
            f"Калибровка #{self.calibration.calibration_id} от {self.calibration.date.strftime('%Y-%m-%d')}, "
        )

    def to_dict(self) -> dict:
        """Сериализует устройство в словарь."""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "calibration_id": self.calibration.calibration_id if self.calibration else None
        }

    def format_for_display(self) -> str:
        """Форматирует устройство для отображения."""
        return (
            f"Устройство #{self.device_id}: {self.name}\n"
            f"{self.get_calibration_summary()}"
        )
