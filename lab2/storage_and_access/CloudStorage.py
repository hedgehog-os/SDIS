from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from storage_and_access.Backup import Backup


class CloudStorage:
    def __init__(self, provider: str, bucket_name: str, access_key: str) -> None:
        self.provider: str = provider
        self.bucket_name: str = bucket_name
        self.access_key: str = access_key

    def update_access_key(self, new_key: str) -> None:
        """Обновляет ключ доступа к облачному хранилищу."""
        if new_key:
            self.access_key = new_key

    def rename_bucket(self, new_name: str) -> None:
        """Переименовывает хранилище."""
        if new_name:
            self.bucket_name = new_name

    def is_valid_key(self, test_key: str) -> bool:
        """Проверяет, совпадает ли тестовый ключ с текущим."""
        return self.access_key == test_key

    def belongs_to_provider(self, provider_name: str) -> bool:
        """Проверяет, соответствует ли провайдер заданному имени."""
        return self.provider.lower() == provider_name.lower()

    def summarize(self) -> str:
        """Форматирует краткую информацию об облачном хранилище."""
        return (
            f"Облако: {self.provider}\n"
            f"Бакет: {self.bucket_name}\n"
            f"Ключ доступа: {'*** скрыт ***'}"
        )

    def to_dict(self) -> dict:
        """Сериализует хранилище в словарь."""
        return {
            "provider": self.provider,
            "bucket_name": self.bucket_name,
            "access_key": self.access_key
        }

    def link_backup(self, backup: "Backup") -> None:
        """Привязывает резервную копию к облачному хранилищу."""
        backup.location = f"{self.provider}/{self.bucket_name}/backup_{backup.backup_id}"

    def upload_file(self, file_name: str, file_size_mb: float) -> str:
        """Симулирует загрузку файла в облачное хранилище."""
        return f"Файл '{file_name}' ({file_size_mb} MB) загружен в бакет '{self.bucket_name}' провайдера '{self.provider}'."

    def download_file(self, file_name: str) -> str:
        """Симулирует скачивание файла из облачного хранилища."""
        return f"Файл '{file_name}' загружен из бакета '{self.bucket_name}' провайдера '{self.provider}'."

    def check_quota(self, used_mb: float, quota_mb: float) -> str:
        """Проверяет, превышает ли использование лимит квоты."""
        if used_mb > quota_mb:
            return f"Превышена квота: использовано {used_mb} MB из {quota_mb} MB."
        return f"Использовано {used_mb} MB из {quota_mb} MB — в пределах лимита."

    def is_bucket_active(self) -> bool:
        """Проверяет, активен ли бакет (условно — по наличию ключа)."""
        return bool(self.access_key)

    def generate_monitoring_entry(self, action: str, file_name: Optional[str] = None) -> dict:
        """Создаёт запись для системы мониторинга."""
        from datetime import datetime
        return {
            "timestamp": datetime.now().isoformat(),
            "provider": self.provider,
            "bucket": self.bucket_name,
            "action": action,
            "file": file_name,
            "status": "success"
        }
