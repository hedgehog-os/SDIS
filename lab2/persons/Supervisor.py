from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document
    from metadata_and_analitics.Comment import Comment


class Supervisor:
    def __init__(self,
                 supervisor_id: int,
                 fullname: str,
                 email: str,
                 reviewed_documents: List["Document"]) -> None:
        self.supervisor_id: int = supervisor_id
        self.fullname: str = fullname
        self.email: str = email
        self.reviewed_documents: List["Document"] = reviewed_documents

    def review_document(self, document: "Document", comment: Optional[str] = None) -> None:
        """Добавляет документ в список рецензированных и оставляет комментарий, если указан."""
        if document not in self.reviewed_documents:
            self.reviewed_documents.append(document)
        if comment:
            from metadata_and_analitics.Comment import Comment  # локальный импорт
            document.comments.append(Comment(
                comment_id=len(document.comments) + 1,
                document_id=document.document_id,
                user_id=self.supervisor_id,
                content=comment,
                posted_at=datetime.now()
            ))


    def remove_document(self, document: "Document") -> None:
        """Удаляет документ из списка рецензированных."""
        if document in self.reviewed_documents:
            self.reviewed_documents.remove(document)

    def count_reviewed_documents(self) -> int:
        """Возвращает количество рецензированных документов."""
        return len(self.reviewed_documents)

    def get_documents_by_status(self, status: str) -> List["Document"]:
        """Фильтрует документы по статусу ('draft', 'final', 'archived')."""
        return [doc for doc in self.reviewed_documents if doc.status == status]

    def get_recent_documents(self, days: int = 30) -> List["Document"]:
        """Возвращает документы, созданные за последние N дней."""
        from datetime import timedelta
        threshold = datetime.now() - timedelta(days=days)
        return [doc for doc in self.reviewed_documents if doc.created_at >= threshold]

    def get_comments_containing(self, keyword: str) -> List[str]:
        """Возвращает комментарии, содержащие заданное слово, из всех документов."""
        return [
            comment.content
            for doc in self.reviewed_documents
            for comment in doc.comments
            if keyword.lower() in comment.content.lower()
        ]

    def summarize(self) -> str:
        """Форматирует краткую информацию о руководителе."""
        return (
            f"Руководитель #{self.supervisor_id}: {self.fullname}\n"
            f"Email: {self.email}\n"
            f"Рецензировано документов: {self.count_reviewed_documents()}"
        )

    def to_dict(self) -> dict:
        """Сериализует руководителя в словарь."""
        return {
            "supervisor_id": self.supervisor_id,
            "fullname": self.fullname,
            "email": self.email,
            "reviewed_document_ids": [doc.document_id for doc in self.reviewed_documents]
        }
