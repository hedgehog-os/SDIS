from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document
    from documents.Revision import Revision
    from documents.Report import Report
    from metadata_and_analitics.Comment import Comment

class Author:
    def __init__(self,
                 author_id: int,
                 fullname: str,
                 email: str,
                 document_id: int,
                 created_at: datetime) -> None:
        self.author_id: int = author_id
        self.fullname: str = fullname
        self.email: str = email
        self.document_id: int = document_id
        self.created_at: datetime = created_at

    def update_email(self, new_email: str) -> None:
        """Обновляет адрес электронной почты автора."""
        if new_email and "@" in new_email:
            self.email = new_email

    def is_associated_with(self, document_id: int) -> bool:
        """Проверяет, связан ли автор с указанным документом."""
        return self.document_id == document_id

    def get_initials(self) -> str:
        """Возвращает инициалы автора."""
        parts = self.fullname.strip().split()
        return "".join(p[0].upper() for p in parts if p)

    def is_recent(self, days: int = 30) -> bool:
        """Проверяет, был ли автор добавлен недавно."""
        from datetime import datetime, timedelta
        return self.created_at >= datetime.now() - timedelta(days=days)

    def format_for_display(self) -> str:
        """Форматирует краткую информацию об авторе."""
        return (
            f"Автор #{self.author_id}: {self.fullname}\n"
            f"Email: {self.email}\n"
            f"Документ: {self.document_id}\n"
            f"Дата регистрации: {self.created_at.strftime('%Y-%m-%d')}"
        )

    def to_dict(self) -> dict:
        """Сериализует автора в словарь."""
        return {
            "author_id": self.author_id,
            "fullname": self.fullname,
            "email": self.email,
            "document_id": self.document_id,
            "created_at": self.created_at.isoformat()
        }

    def is_author_of(self, document: "Document") -> bool:
        """Проверяет, связан ли автор с указанным документом."""
        return self.document_id == document.document_id

    def create_revision(self, document: "Document", notes: str) -> "Revision":
        """Создаёт новую ревизию документа от имени автора."""
        return Revision(
            revision_id=len(document.revisions) + 1,
            document_id=document.document_id,
            author_id=self.author_id,
            timestamp=datetime.now(),
            notes=notes,
            change_history=[]
        )
    
    def submit_report(self, report: "Report", content: str) -> None:
        """Добавляет комментарий в отчёт от имени автора."""
        from metadata_and_analitics.Comment import Comment
        report.comments.append(Comment(
            comment_id=len(report.comments) + 1,
            document_id=report.report_id,
            user_id=self.author_id,
            content=content,
            posted_at=datetime.now()
        ))

    def write_comment(self, target_id: int, content: str) -> "Comment":
        """Создаёт комментарий от имени автора к указанному объекту."""
        from metadata_and_analitics.Comment import Comment
        return Comment(
            comment_id=target_id * 1000 + self.author_id,
            document_id=target_id,
            user_id=self.author_id,
            content=content,
            posted_at=datetime.now()
        )


