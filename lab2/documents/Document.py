from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from metadata_and_analitics.Metadata import Metadata
from metadata_and_analitics.Comment import Comment
from metadata_and_analitics.Keyword import Keyword
from documents.Template import Template
from Exceptions import DocumentNotReadyError, DocumentAlreadyArchivedError, DocumentRestoreError

if TYPE_CHECKING:
    from Attachment import Attachment
    from Revision import Revision
    from Form import Form
    from Protocol import Protocol
    from Report import Report

class Document:

    statuses = {
        'draft', 'final', 'archived', 'restricted'
    }

    def __init__(self,
                 document_id: int,
                 title: str,
                 author_id: int,
                 created_at: Optional[datetime] = None,
                 tags: Optional[List[str]] = None,
                 status: str = "draft",
                 metadata: Optional["Metadata"] = None,
                 attachments: Optional[List["Attachment"]] = None,
                 revisions: Optional[List["Revision"]] = None,
                 comments: Optional[List["Comment"]] = None,
                 template: Optional["Template"] = None,
                 keywords: Optional[List["Keyword"]] = None,
                 form: "Form" = None,
                 protocol: "Protocol" = None,
                 report: "Report" = None) -> None:
        self.document_id: int = document_id
        self.title: str = title
        self.author_id: int = author_id
        self.created_at: datetime = created_at or datetime.now()
        self.tags: List[str] = tags or []
        self.status: str = status

        # Ассоциации
        self.attachments: List["Attachment"] = attachments or []
        self.revisions: List["Revision"] = revisions or []
        self.comments: List["Comment"] = comments or []
        self.template: Optional["Template"] = template
        self.keywords: Optional[List["Keyword"]] = keywords
        self.form: "Form" = form
        self.protocol: "Protocol" = protocol
        self.report: "Report" = report
        self.metadata: "Metadata" = metadata


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.statuses:
            raise ValueError(f'Недопустимый статус: {value}')
        self._status = value
        
    def revise(self, revision: "Revision") -> None:
        self.revisions.append(revision)
        self.status = "draft"

    def submit(self) -> None:
        if not self.is_ready_for_submission():
            raise DocumentNotReadyError("Документ не готов к отправке: проверь метаданные, шаблон и ревизии.")
        self.status = "final"

    def archive(self) -> None:
        if self.status == "archived":
            raise DocumentAlreadyArchivedError("Документ уже находится в архиве.")
        self.status = "archived"

    def restore(self) -> None:
        if self.status != "archived":
            raise DocumentRestoreError("Можно восстановить только архивированный документ.")
        self.status = "final"

    
    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)

    def add_keyword(self, keyword: "Keyword") -> None:
        if self.keywords is None:
            self.keywords = []
        self.keywords.append(keyword)

    def remove_keyword(self, keyword: "Keyword") -> None:
        if self.keywords and keyword in self.keywords:
            self.keywords.remove(keyword)

    def approve(self) -> None:
        if self.status != "final":
            raise ValueError("Можно утвердить только финальный документ.")
        if self.metadata:
            self.metadata.approved = True

    def reject(self, reason: str) -> None:
        self.comments.append(Comment(
            comment_id=len(self.comments) + 1,
            document_id=self.document_id,
            user_id=self.author_id,
            content=f"Отклонено: {reason}",
            posted_at=datetime.now()
        ))
        self.status = "draft"

    def encrypt(self, method: str = "AES-256") -> None:
        if self.metadata:
            self.metadata.is_encrypted = True
            self.metadata.encryption_method = method

    def decrypt(self) -> None:
        if self.metadata and self.metadata.is_encrypted:
            self.metadata.is_encrypted = False
            self.metadata.encryption_method = None

    def is_ready_for_submission(self) -> bool:
        """Проверяет, готов ли документ к отправке."""
        has_metadata = self.metadata is not None
        has_template = self.template is not None
        has_content = bool(self.revisions)
        return has_metadata and has_template and has_content and self.status == "draft"

    def export_as_text(self) -> str:
        """Возвращает текстовое представление документа."""
        lines = [
            f"Документ: {self.title}",
            f"Автор ID: {self.author_id}",
            f"Статус: {self.status}",
            f"Создан: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"Теги: {', '.join(self.tags) if self.tags else '—'}",
            f"Ключевые слова: {self.get_keywords_as_text()}",
            f"Шаблон: {self.template.name if self.template else '—'}",
            f"Ревизий: {len(self.revisions)}",
            f"Вложений: {len(self.attachments)}",
            f"Комментариев: {len(self.comments)}"
        ]
        return "\n".join(lines)

    def get_attachment_formats(self) -> dict[str, int]:
        """Возвращает количество вложений по формату."""
        format_count: dict[str, int] = {}
        for attachment in self.attachments:
            ext = attachment.get_file_extension()
            format_count[ext] = format_count.get(ext, 0) + 1
        return format_count

    def find_comments_containing(self, keyword: str) -> List[str]:
        """Возвращает комментарии, содержащие заданное слово."""
        return [c.content for c in self.comments if keyword.lower() in c.content.lower()]

    def summarize_revisions(self) -> str:
        """Возвращает краткую сводку по всем ревизиям."""
        if not self.revisions:
            return "Ревизий нет."
        return "\n".join([r.get_revision_info() for r in self.revisions])

    def link_form(self, form: "Form") -> None:
        """Привязывает форму к документу, если ID совпадают."""
        if form.form_id == self.document_id:
            form.title = self.title
            form.author_id = self.author_id

    def validate_against_protocol(self, protocol: "Protocol") -> bool:
        """Проверяет, соответствует ли документ шагам протокола."""
        if not protocol.steps:
            return False
        return any(tag.lower() in step.lower() for step in protocol.steps for tag in self.tags)

    def contribute_to_report(self, report: "Report") -> None:
        """Добавляет документ как источник в отчёт, если автор совпадает."""
        if report.author_id == self.author_id:
            comment_text = f"Документ '{self.title}' включён в отчёт '{report.title}'."
            report.comments.append(Comment(
                comment_id=len(report.comments) + 1,
                document_id=self.document_id,
                user_id=self.author_id,
                content=comment_text,
                posted_at=datetime.now()
            ))

    def generate_document_summary(self) -> str:
        """Формирует краткий отчёт по документу."""
        lines = [
            f"Документ: {self.title}",
            f"Статус: {self.status}",
            f"Автор: {self.author_id}",
            f"Создан: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"Ключевые слова: {self.get_keywords_as_text()}",
            f"Ревизий: {len(self.revisions)}",
            f"Комментариев: {len(self.comments)}",
            f"Вложений: {len(self.attachments)}",
            f"Шаблон: {self.template.name if self.template else '—'}",
            f"Метаданные: {'есть' if self.metadata else 'нет'}"
        ]
        return "\n".join(lines)

    def get_keywords_as_text(self) -> str:
        if not self.keywords:
            return "—"
        return ", ".join(k.word for k in self.keywords)
