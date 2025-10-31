from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Device import Device


class LabRoom:
    def __init__(self, room_number: str, equipment: Optional[List["Device"]] = None) -> None:
        self.room_number: str = room_number
        self.equipment: List["Device"] = equipment or []

    def add_device(self, device: "Device") -> None:
        """Добавляет устройство в лабораторию, если оно ещё не включено."""
        if device not in self.equipment:
            self.equipment.append(device)

    def remove_device(self, device: "Device") -> None:
        """Удаляет устройство из лаборатории."""
        if device in self.equipment:
            self.equipment.remove(device)

    def has_device(self, device: "Device") -> bool:
        """Проверяет, находится ли устройство в лаборатории."""
        return device in self.equipment

    def get_device_ids(self) -> List[int]:
        """Возвращает список ID всех устройств в лаборатории."""
        return [d.device_id for d in self.equipment]

    def get_uncalibrated_devices(self) -> List["Device"]:
        """Возвращает список устройств без калибровки."""
        return [d for d in self.equipment if not d.is_calibrated()]

    def get_recently_calibrated_devices(self, days: int = 30) -> List["Device"]:
        """Возвращает устройства, откалиброванные за последние N дней."""
        return [d for d in self.equipment if d.was_calibrated_recently(days)]

    def summarize(self) -> str:
        """Форматирует краткую информацию о лаборатории."""
        return (
            f"Лаборатория {self.room_number}\n"
            f"Оборудование: {len(self.equipment)} устройств\n"
            f"Без калибровки: {len(self.get_uncalibrated_devices())}\n"
            f"Недавно откалибровано: {len(self.get_recently_calibrated_devices())}"
        )

    def to_dict(self) -> dict:
        """Сериализует лабораторию в словарь."""
        return {
            "room_number": self.room_number,
            "device_ids": self.get_device_ids()
        }
