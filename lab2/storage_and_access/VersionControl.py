from typing import List

class VersionControl:
    def __init__(self, document_id: int, versions: List[str], current_version: str) -> None:
        self.document_id: int = document_id
        self.versions: List[str] = versions
        self.current_version: str = current_version

    def add_version(self, version: str) -> None:
        """Добавляет новую версию документа и делает её текущей."""
        if version not in self.versions:
            self.versions.append(version)
        self.current_version = version

    def rollback_to(self, version: str) -> bool:
        """Откатывает текущую версию к указанной, если она существует."""
        if version in self.versions:
            self.current_version = version
            return True
        return False

    def remove_version(self, version: str) -> bool:
        """Удаляет указанную версию, если она не является текущей."""
        if version == self.current_version:
            return False
        if version in self.versions:
            self.versions.remove(version)
            return True
        return False

    def is_latest(self, version: str) -> bool:
        """Проверяет, является ли версия текущей."""
        return self.current_version == version

    def has_version(self, version: str) -> bool:
        """Проверяет, существует ли указанная версия."""
        return version in self.versions

    def version_count(self) -> int:
        """Возвращает количество сохранённых версий."""
        return len(self.versions)

    def summarize(self) -> str:
        """Форматирует краткую информацию о версиях документа."""
        return (
            f"Контроль версий для документа #{self.document_id}\n"
            f"Текущая версия: {self.current_version}\n"
            f"Всего версий: {len(self.versions)}\n"
            f"История: {', '.join(self.versions)}"
        )

    def to_dict(self) -> dict:
        """Сериализует объект контроля версий в словарь."""
        return {
            "document_id": self.document_id,
            "versions": self.versions,
            "current_version": self.current_version
        }
