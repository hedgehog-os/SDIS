from datetime import datetime
from typing import List, TYPE_CHECKING
from Exceptions import ArchiveAlreadyContainsDocumentError, ArchiveDocumentNotFoundError

if TYPE_CHECKING:
    from documents.Document import Document
    from storage_and_access.Backup import Backup
    from experiments_and_equipments.StorageDevice import StorageDevice
    from documents.Report import Report
    from documents.Form import Form
    from metadata_and_analitics.Comment import Comment


class Archive:
    def __init__(self, archive_id: int, name: str, documents: List[int], archived_at: datetime) -> None:
        self.archive_id: int = archive_id
        self.name: str = name
        self.documents: List[int] = documents
        self.archived_at: datetime = archived_at

    def add_document(self, document_id: int) -> None:
        if document_id in self.documents:
            raise ArchiveAlreadyContainsDocumentError(f"Документ #{document_id} уже в архиве.")
        self.documents.append(document_id)

    
    def remove_document(self, document_id: int) -> None:
        if document_id not in self.documents:
            raise ArchiveDocumentNotFoundError(f"Документ #{document_id} не найден в архиве.")
        self.documents.remove(document_id)

    def has_document(self, document_id: int) -> bool:
        """Проверяет, содержится ли документ в архиве."""
        return document_id in self.documents

    def count_documents(self) -> int:
        """Возвращает количество документов в архиве."""
        return len(self.documents)

    def get_documents_by_prefix(self, prefix: str) -> List[int]:
        """Фильтрует документы по началу ID (если ID — строковые)."""
        return [doc_id for doc_id in self.documents if str(doc_id).startswith(prefix)]

    def summarize(self) -> str:
        """Форматирует краткую информацию об архиве."""
        return (
            f"Архив #{self.archive_id}: {self.name}\n"
            f"Дата архивации: {self.archived_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Документов: {len(self.documents)}"
        )

    def to_dict(self) -> dict:
        """Сериализует архив в словарь."""
        return {
            "archive_id": self.archive_id,
            "name": self.name,
            "documents": self.documents,
            "archived_at": self.archived_at.isoformat()
        }

    def get_documents(self, all_documents: List["Document"]) -> List["Document"]:
        """Возвращает объекты документов, входящих в архив."""
        return [doc for doc in all_documents if doc.document_id in self.documents]

    def get_documents_by_status(self, all_documents: List["Document"], status: str) -> List["Document"]:
        """Фильтрует документы в архиве по статусу ('draft', 'final', 'archived')."""
        return [doc for doc in self.get_documents(all_documents) if doc.status == status]

    def get_document_titles(self, all_documents: List["Document"]) -> List[str]:
        """Возвращает названия всех документов в архиве."""
        return [doc.title for doc in self.get_documents(all_documents)]

    def export_summary(self, all_documents: List["Document"]) -> str:
        """Формирует текстовый отчёт по архиву и его содержимому."""
        lines = [
            f"Архив #{self.archive_id}: {self.name}",
            f"Дата архивации: {self.archived_at.strftime('%Y-%m-%d %H:%M')}",
            f"Документов: {len(self.documents)}"
        ]
        for doc in self.get_documents(all_documents):
            lines.append(f"— {doc.title} [{doc.status}]")
        return "\n".join(lines)

    def restore_all_documents(self, all_documents: List["Document"]) -> None:
        """Восстанавливает все архивированные документы в статус 'final'."""
        for doc in self.get_documents(all_documents):
            if doc.status == "archived":
                doc.restore()

    def link_to_backup(self, backup: "Backup") -> bool:
        """Проверяет, содержит ли резервная копия все документы архива."""
        if not backup.size_mb or not backup.storage_device:
            return False
        return all(doc_id in backup.storage_device.backups for doc_id in self.documents)

    def generate_backup_summary(self, backup: "Backup") -> str:
        """Формирует краткое описание связи архива с резервной копией."""
        return (
            f"Архив '{self.name}' связан с резервной копией #{backup.backup_id} "
            f"на устройстве '{backup.storage_device.name}' от {backup.timestamp.strftime('%Y-%m-%d')}."
        )

    def store_on_device(self, device: "StorageDevice") -> None:
        """Добавляет архив как логическую единицу хранения."""
        from storage_and_access.Backup import Backup  # локальный импорт
        note = f"Архив '{self.name}' содержит {len(self.documents)} документов, сохранён {self.archived_at.strftime('%Y-%m-%d')}."
        print(note)
        device.add_backup(Backup(
            backup_id=len(device.backups) + 1,
            location=device.location or "не указано",
            timestamp=self.archived_at,
            size_mb=len(self.documents) * 0.5,
            encrypted_with=None,
            storage_device=device
        ))

    def contribute_to_report(self, report: "Report") -> None:
        """Добавляет архив как источник в отчёт, если автор совпадает."""
        from metadata_and_analitics.Comment import Comment  # локальный импорт
        if report.author_id in self.documents:
            report.comments.append(Comment(
                comment_id=len(report.comments) + 1,
                document_id=None,
                user_id=report.author_id,
                content=f"Архив '{self.name}' включён в отчёт '{report.title}'.",
                posted_at=datetime.now()
            ))


    def validate_forms(self, forms: List["Form"]) -> List["Form"]:
        """Возвращает формы, связанные с документами архива."""
        return [form for form in forms if form.form_id in self.documents]
