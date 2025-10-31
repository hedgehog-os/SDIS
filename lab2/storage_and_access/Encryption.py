from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from storage_and_access.Backup import Backup

class Encryption:

    methods = {
        "AES", "RSA", "ChaCha20"
    }

    algorithms = {
        "CBC", "GCM", "OAEP"
    }

    def __init__(self,
                 encryption_id: int,
                 method: str,
                 key_length: int,
                 algorithm: str,
                 applied_to: Optional[List["Backup"]] = None) -> None:
        self.encryption_id: int = encryption_id
        self.method: str = method
        self.key_length: int = key_length
        self.algorithm: str = algorithm

        # Ассоциация
        self.applied_to: List["Backup"] = applied_to or []

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        if value not in self.methods:
            raise ValueError(f'Недопустимый формат: {value}')
        self._method = value

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        if value not in self.algorithms:
            raise ValueError(f'Недопустимый формат: {value}')
        self._algorithm = value

    def apply_to_backup(self, backup: "Backup") -> None:
        """Применяет шифрование к резервной копии и добавляет её в список связанных."""
        if backup not in self.applied_to:
            self.applied_to.append(backup)
            backup.encrypted_with = self

    def remove_from_backup(self, backup: "Backup") -> None:
        """Удаляет связь шифрования с резервной копией."""
        if backup in self.applied_to:
            self.applied_to.remove(backup)
        if backup.encrypted_with == self:
            backup.encrypted_with = None

    def is_strong_encryption(self) -> bool:
        """Проверяет, считается ли шифрование надёжным по длине ключа."""
        return self.key_length >= 256

    def is_applied_to(self, backup: "Backup") -> bool:
        """Проверяет, применено ли это шифрование к указанной резервной копии."""
        return backup in self.applied_to

    def summarize(self) -> str:
        """Форматирует краткую информацию о шифровании."""
        return (
            f"Шифрование #{self.encryption_id}\n"
            f"Метод: {self.method} | Алгоритм: {self.algorithm}\n"
            f"Длина ключа: {self.key_length} бит\n"
            f"Применено к {len(self.applied_to)} резервным копиям"
        )

    def to_dict(self) -> dict:
        """Сериализует объект шифрования в словарь."""
        return {
            "encryption_id": self.encryption_id,
            "method": self.method,
            "key_length": self.key_length,
            "algorithm": self.algorithm,
            "applied_to": [b.backup_id for b in self.applied_to]
        }
