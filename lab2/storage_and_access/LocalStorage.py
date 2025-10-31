from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from storage_and_access.Backup import Backup
    from Folder import Folder
    from documents.Document import Document


class LocalStorage:
    def __init__(self, path: str, capacity_gb: float) -> None:
        self.path: str = path
        self.capacity_gb: float = capacity_gb

    def update_path(self, new_path: str) -> None:
        """Обновляет путь к хранилищу."""
        if new_path:
            self.path = new_path

    def resize(self, new_capacity_gb: float) -> None:
        """Изменяет доступный объём хранилища."""
        if new_capacity_gb > 0:
            self.capacity_gb = new_capacity_gb

    def is_path_valid(self) -> bool:
        """Проверяет, корректен ли путь (условно — начинается с '/')."""
        return self.path.startswith("/")

    def has_enough_space(self, required_gb: float) -> bool:
        """Проверяет, достаточно ли места для хранения данных."""
        return self.capacity_gb >= required_gb
    
    def summarize(self) -> str:
        """Форматирует краткую информацию о хранилище."""
        return (
            f"Локальное хранилище\n"
            f"Путь: {self.path}\n"
            f"Объём: {self.capacity_gb} GB"
        )

    def to_dict(self) -> dict:
        """Сериализует хранилище в словарь."""
        return {
            "path": self.path,
            "capacity_gb": self.capacity_gb
        }

    def store_backup(self, backup: "Backup") -> None:
        """Привязывает резервную копию к локальному хранилищу."""
        backup.location = self.path

    def get_backup_summary(self, backup: "Backup") -> str:
        """Формирует краткое описание хранения резервной копии."""
        return (
            f"Резервная копия #{backup.backup_id} размещена в '{self.path}' "
            f"объёмом {backup.size_mb or '—'} MB, создана {backup.timestamp.strftime('%Y-%m-%d')}."
        )

    def store_folder(self, folder: "Folder") -> str:
        """Формирует запись о размещении папки в локальном хранилище."""
        return f"Папка '{folder.name}' (#{folder.folder_id}) размещена в '{self.path}' с {len(folder.document_ids)} документами."

    def store_documents(self, documents: List["Document"]) -> List[str]:
        """Формирует список записей о размещении документов в хранилище."""
        return [
            f"Документ '{doc.title}' (#{doc.document_id}) сохранён в '{self.path}'"
            for doc in documents
        ]

    def export_storage_report(self, backups: List["Backup"]) -> str:
        """Формирует текстовый отчёт по резервным копиям, размещённым в хранилище."""
        lines = [f"Хранилище: {self.path} | Объём: {self.capacity_gb} GB"]
        for b in backups:
            if b.location == self.path:
                lines.append(f"— Backup #{b.backup_id} | {b.size_mb or '—'} MB | {b.timestamp.strftime('%Y-%m-%d')}")
        return "\n".join(lines)
