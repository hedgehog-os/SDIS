from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Device import Device


class Sensor:
    def __init__(self, sensor_id: int, type: str, device: "Device") -> None:
        self.sensor_id: int = sensor_id
        self.type: str = type
        self.device: "Device" = device

    def is_attached_to(self, device: "Device") -> bool:
        """Проверяет, прикреплён ли сенсор к указанному устройству."""
        return self.device == device

    def get_device_name(self) -> str:
        """Возвращает имя устройства, к которому прикреплён сенсор."""
        return self.device.name if self.device else "—"

    def describe(self) -> str:
        """Форматирует краткое описание сенсора."""
        return (
            f"Сенсор #{self.sensor_id}\n"
            f"Тип: {self.type}\n"
            f"Устройство: {self.get_device_name()}"
        )

    def to_dict(self) -> dict:
        """Сериализует сенсор в словарь."""
        return {
            "sensor_id": self.sensor_id,
            "type": self.type,
            "device_id": self.device.device_id,
            "device_name": self.device.name
        }

    def annotate_device(self) -> None:
        """Добавляет сенсор в список сенсоров устройства, если поддерживается."""
        if hasattr(self.device, "sensors"):
            if self not in self.device.sensors:
                self.device.sensors.append(self)
