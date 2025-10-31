from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from storage_and_access.Backup import Backup


class StorageDevice:

    device_types = {
        "HDD", "SSD", "Cloud"
    }

    def __init__(self,
                 device_id: int,
                 name: str,
                 device_type: str,
                 capacity_mb: float,
                 location: Optional[str] = None,
                 backups: Optional[List["Backup"]] = None) -> None:
        
        self.device_id: int = device_id
        self.name: str = name
        self.device_type: str = device_type
        self.capacity_mb: float = capacity_mb
        self.location: Optional[str] = location

        # Ассоциация
        self.backups: List["Backup"] = backups or []

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        if value not in self.device_types:
            raise ValueError(f'Недопустимый формат: {value}')
        self._device_type = value

    def add_backup(self, backup: "Backup") -> None:
        """Добавляет резервную копию к устройству, если она ещё не включена."""
        if backup not in self.backups:
            self.backups.append(backup)
            backup.storage_device = self

    def remove_backup(self, backup: "Backup") -> None:
        """Удаляет резервную копию из устройства."""
        if backup in self.backups:
            self.backups.remove(backup)
            if backup.storage_device == self:
                backup.storage_device = None

    def total_backup_size(self) -> float:
        """Возвращает общий объём всех резервных копий."""
        return sum(b.size_mb or 0 for b in self.backups)

    def available_space(self) -> float:
        """Вычисляет оставшееся свободное место на устройстве."""
        return self.capacity_mb - self.total_backup_size()

    def is_over_capacity(self) -> bool:
        """Проверяет, превышен ли лимит хранения."""
        return self.total_backup_size() > self.capacity_mb

    def get_recent_backups(self, days: int = 30) -> List["Backup"]:
        """Возвращает резервные копии, созданные за последние N дней."""
        from datetime import datetime, timedelta
        threshold = datetime.now() - timedelta(days=days)
        return [b for b in self.backups if b.timestamp >= threshold]

    def get_encrypted_backups(self) -> List["Backup"]:
        """Возвращает список зашифрованных резервных копий."""
        return [b for b in self.backups if b.encrypted_with is not None]

    def summarize(self) -> str:
        """Форматирует краткую информацию об устройстве хранения."""
        return (
            f"Устройство #{self.device_id}: {self.name} ({self.device_type})\n"
            f"Расположение: {self.location or '—'}\n"
            f"Ёмкость: {self.capacity_mb:.2f} MB\n"
            f"Использовано: {self.total_backup_size():.2f} MB\n"
            f"Свободно: {self.available_space():.2f} MB\n"
            f"Резервных копий: {len(self.backups)} ({len(self.get_encrypted_backups())})"
        )

    def to_dict(self) -> dict:
        """Сериализует устройство хранения в словарь."""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "device_type": self.device_type,
            "capacity_mb": self.capacity_mb,
            "location": self.location,
            "backup_ids": [b.backup_id for b in self.backups],
            "used_space_mb": self.total_backup_size(),
            "free_space_mb": self.available_space()
        }
