from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document
    from documents.Report import Report
    from documents.Revision import Revision
    from Metadata import Metadata
    from Comment import Comment


class Statistics:
    def __init__(self, document_id: int, views: int, edits: int, comments: int) -> None:
        self.document_id: int = document_id
        self.views: int = views
        self.edits: int = edits
        self.comments: int = comments

    def increment_views(self, count: int = 1) -> None:
        """Увеличивает количество просмотров на заданное число."""
        if count > 0:
            self.views += count

    def increment_edits(self, count: int = 1) -> None:
        """Увеличивает количество правок на заданное число."""
        if count > 0:
            self.edits += count

    def increment_comments(self, count: int = 1) -> None:
        """Увеличивает количество комментариев на заданное число."""
        if count > 0:
            self.comments += count

    def reset_statistics(self) -> None:
        """Сбрасывает все статистические показатели до нуля."""
        self.views = 0
        self.edits = 0
        self.comments = 0

    def get_summary(self) -> str:
        """Возвращает краткую сводку статистики."""
        return (
            f"Статистика по документу #{self.document_id}:\n"
            f"Просмотры: {self.views}\n"
            f"Правки: {self.edits}\n"
            f"Комментарии: {self.comments}"
        )

    def to_dict(self) -> dict:
        """Сериализует статистику в словарь."""
        return {
            "document_id": self.document_id,
            "views": self.views,
            "edits": self.edits,
            "comments": self.comments
        }

    def is_active(self, view_threshold: int = 10, edit_threshold: int = 5, comment_threshold: int = 3) -> bool:
        """Определяет, считается ли документ активным по заданным порогам."""
        return (
            self.views >= view_threshold or
            self.edits >= edit_threshold or
            self.comments >= comment_threshold
        )

    def link_to_document(self, document: "Document") -> None:
        """Привязывает статистику к документу, если ID совпадают."""
        if document.document_id == self.document_id:
            document.statistics = self

    def update_from_revision(self, revision: "Revision") -> None:
        """Увеличивает счётчик правок, если ревизия относится к тому же документу."""
        if revision.document_id == self.document_id:
            self.increment_edits()

    def reflect_metadata_activity(self, metadata: "Metadata") -> None:
        """Увеличивает просмотры, если метаданные были обновлены."""
        if metadata.document_id == self.document_id:
            self.increment_views()

    def contribute_to_report(self, report: "Report") -> None:
        """Добавляет статистику в отчёт как текстовую сводку."""
        from Comment import Comment  # локальный импорт
        summary = self.get_summary()
        report.comments.append(Comment(
            comment_id=len(report.comments) + 1,
            document_id=self.document_id,
            user_id=report.author_id,
            content=f"Статистика документа:\n{summary}",
            posted_at=datetime.now()
        ))

    
    def compare_to(self, other: "Statistics") -> dict[str, int]:
        """Сравнивает текущую статистику с другой и возвращает разницу по каждому показателю."""
        return {
            "views_diff": self.views - other.views,
            "edits_diff": self.edits - other.edits,
            "comments_diff": self.comments - other.comments
        }

    def visualize_activity(self) -> str:
        """Генерирует текстовую диаграмму активности."""
        return (
            f"Активность документа #{self.document_id}\n"
            f"Просмотры: {'|' * min(self.views, 20)} ({self.views})\n"
            f"Правки: {'|' * min(self.edits, 20)} ({self.edits})\n"
            f"Комментарии: {'|' * min(self.comments, 20)} ({self.comments})"
        )

