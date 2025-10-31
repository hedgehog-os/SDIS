from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document
    from documents.Report import Report
    from storage_and_access.Archive import Archive
    from metadata_and_analitics.Comment import Comment
    from Folder import Folder  # если используется в is_child_of


class Folder:
    def __init__(self, folder_id: int, name: str, parent_id: Optional[int], document_ids: List[int]) -> None:
        self.folder_id: int = folder_id
        self.name: str = name
        self.parent_id: Optional[int] = parent_id
        self.document_ids: List[int] = document_ids

    def add_document(self, document_id: int) -> None:
        """Добавляет документ в папку, если он ещё не включён."""
        if document_id not in self.document_ids:
            self.document_ids.append(document_id)

    def remove_document(self, document_id: int) -> None:
        """Удаляет документ из папки."""
        if document_id in self.document_ids:
            self.document_ids.remove(document_id)

    def has_document(self, document_id: int) -> bool:
        """Проверяет, содержится ли документ в папке."""
        return document_id in self.document_ids

    def is_root(self) -> bool:
        """Проверяет, является ли папка корневой (без родителя)."""
        return self.parent_id is None

    def is_child_of(self, other_folder: "Folder") -> bool:
        """Проверяет, вложена ли текущая папка в другую."""
        return self.parent_id == other_folder.folder_id

    def count_documents(self) -> int:
        """Возвращает количество документов в папке."""
        return len(self.document_ids)

    def get_documents_by_prefix(self, prefix: str) -> List[int]:
        """Фильтрует документы по началу ID (если ID — строковые)."""
        return [doc_id for doc_id in self.document_ids if str(doc_id).startswith(prefix)]

    def summarize(self) -> str:
        """Форматирует краткую информацию о папке."""
        parent_info = f"Родительская папка: #{self.parent_id}" if self.parent_id is not None else "Корневая папка"
        return (
            f"Папка #{self.folder_id}: {self.name}\n"
            f"{parent_info}\n"
            f"Документов: {len(self.document_ids)}"
        )

    def to_dict(self) -> dict:
        """Сериализует папку в словарь."""
        return {
            "folder_id": self.folder_id,
            "name": self.name,
            "parent_id": self.parent_id,
            "document_ids": self.document_ids
        }

    def get_documents(self, all_documents: List["Document"]) -> List["Document"]:
        """Возвращает объекты документов, находящихся в папке."""
        return [doc for doc in all_documents if doc.document_id in self.document_ids]

    def get_documents_by_status(self, all_documents: List["Document"], status: str) -> List["Document"]:
        """Фильтрует документы по статусу ('draft', 'final', 'archived')."""
        return [doc for doc in self.get_documents(all_documents) if doc.status == status]

    def get_document_titles(self, all_documents: List["Document"]) -> List[str]:
        """Возвращает названия всех документов в папке."""
        return [doc.title for doc in self.get_documents(all_documents)]

    def archive_contents(self, archive: "Archive") -> None:
        """Добавляет все документы из папки в архив."""
        for doc_id in self.document_ids:
            if doc_id not in archive.documents:
                archive.documents.append(doc_id)

    def contribute_to_report(self, report: "Report") -> None:
        """Добавляет документы из папки в отчёт, если автор совпадает."""
        from metadata_and_analitics.Comment import Comment  # локальный импорт
        for doc_id in self.document_ids:
            if report.author_id == doc_id:
                report.comments.append(Comment(
                    comment_id=len(report.comments) + 1,
                    document_id=doc_id,
                    user_id=report.author_id,
                    content=f"Документ #{doc_id} из папки '{self.name}' включён в отчёт '{report.title}'.",
                    posted_at=datetime.now()
                ))


    def export_summary(self, all_documents: List["Document"]) -> str:
        """Формирует текстовый отчёт по содержимому папки."""
        lines = [
            f"Папка #{self.folder_id}: {self.name}",
            f"Родитель: {self.parent_id if self.parent_id is not None else 'корневая'}",
            f"Документов: {len(self.document_ids)}"
        ]
        for doc in self.get_documents(all_documents):
            lines.append(f"— {doc.title} [{doc.status}]")
        return "\n".join(lines)
