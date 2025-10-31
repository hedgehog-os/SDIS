from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from storage_and_access.Encryption import Encryption
    from experiments_and_equipments.StorageDevice import StorageDevice


class Backup:
    def __init__(self,
                 backup_id: int,
                 location: str,
                 timestamp: Optional[datetime] = None,
                 size_mb: Optional[float] = None,
                 encrypted_with: Optional["Encryption"] = None,
                 storage_device: Optional["StorageDevice"] = None) -> None:
        self.backup_id: int = backup_id
        self.location: str = location
        self.timestamp: datetime = timestamp or datetime.now()
        self.size_mb: Optional[float] = size_mb

        # Ассоциации
        self.encrypted_with: Optional["Encryption"] = encrypted_with
        self.storage_device: Optional["StorageDevice"] = storage_device

    def encrypt(self, method: Optional["Encryption"]) -> None:
        """Применяет шифрование к резервной копии."""
        if method:
            self.encrypted_with = method

    def decrypt(self) -> None:
        """Снимает шифрование с резервной копии."""
        self.encrypted_with = None

    def is_encrypted(self) -> bool:
        """Проверяет, зашифрована ли резервная копия."""
        return self.encrypted_with is not None

    def assign_to_device(self, device: "StorageDevice") -> None:
        """Привязывает резервную копию к устройству хранения."""
        self.storage_device = device

    def is_stored_on(self, device: "StorageDevice") -> bool:
        """Проверяет, находится ли резервная копия на указанном устройстве."""
        return self.storage_device == device

    def is_recent(self, days: int = 30) -> bool:
        """Проверяет, была ли резервная копия создана в последние N дней."""
        return self.timestamp >= datetime.now() - timedelta(days=days)

    def is_large(self, threshold_mb: float = 100.0) -> bool:
        """Проверяет, превышает ли размер резервной копии заданный порог."""
        return self.size_mb is not None and self.size_mb > threshold_mb

    def summarize(self) -> str:
        """Форматирует краткую информацию о резервной копии."""
        return (
            f"Резервная копия #{self.backup_id}\n"
            f"Местоположение: {self.location}\n"
            f"Дата: {self.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
            f"Размер: {self.size_mb or '—'} MB\n"
            f"Шифрование: {self.encrypted_with.method if self.encrypted_with else 'нет'}\n"
            f"Устройство: {self.storage_device.name if self.storage_device else 'не указано'}"
        )

    def to_dict(self) -> dict:
        """Сериализует резервную копию в словарь."""
        return {
            "backup_id": self.backup_id,
            "location": self.location,
            "timestamp": self.timestamp.isoformat(),
            "size_mb": self.size_mb,
            "encrypted_with": self.encrypted_with.method if self.encrypted_with else None,
            "storage_device": self.storage_device.name if self.storage_device else None
        }
