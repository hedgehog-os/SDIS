from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from documents.Document import Document
    from Metadata import Metadata
    from Insight import Insight
    from documents.Report import Report
    from Comment import Comment

class Tag:

    categories = {
        'topic', 'status', 'priority', 'department', 'confidentiality', 'workflow'
    }

    def __init__(self,
                 tag_id: int,
                 name: str,
                 category: Optional[str] = None,
                 applied_to: Optional[List["Document"]] = None) -> None:
        self.tag_id: int = tag_id
        self.name: str = name
        self.category: Optional[str] = category

        # Ассоциация
        self.applied_to: List["Document"] = applied_to or []

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in self.categories:
            raise ValueError(f'Недопустимый статус: {value}')
        self._category = value

    def apply_to_document(self, document: "Document") -> None:
        """Применяет тег к документу, если он ещё не связан."""
        if document not in self.applied_to:
            self.applied_to.append(document)
            if not hasattr(document, "tags"):
                document.tags = []
            if self.name not in document.tags:
                document.tags.append(self.name)

    def remove_from_document(self, document: "Document") -> None:
        """Удаляет тег из документа и из списка связанных."""
        if document in self.applied_to:
            self.applied_to.remove(document)
            if hasattr(document, "tags") and self.name in document.tags:
                document.tags.remove(self.name)

    def is_applied_to(self, document: "Document") -> bool:
        """Проверяет, применён ли тег к указанному документу."""
        return document in self.applied_to

    def get_document_ids(self) -> List[int]:
        """Возвращает список ID документов, к которым применён тег."""
        return [doc.document_id for doc in self.applied_to]

    def to_dict(self) -> dict:
        """Сериализует тег в словарь."""
        return {
            "tag_id": self.tag_id,
            "name": self.name,
            "category": self.category,
            "applied_to": self.get_document_ids()
        }

    def format_for_display(self) -> str:
        """Форматирует тег для отображения."""
        return (
            f"Тег #{self.tag_id}: {self.name} "
            f"({self.category or 'без категории'}) — "
            f"{len(self.applied_to)} документов"
        )

    def matches_category(self, category: str) -> bool:
        """Проверяет, принадлежит ли тег указанной категории."""
        return self.category == category

    def apply_to_documents(self, documents: List["Document"]) -> None:
        """Применяет тег ко всем переданным документам."""
        for doc in documents:
            self.apply_to_document(doc)

    def filter_documents_by_category(self, category: str) -> List["Document"]:
        """Возвращает документы, к которым применён тег указанной категории."""
        if self.category == category:
            return self.applied_to
        return []

    def visualize_distribution(self) -> str:
        """Генерирует текстовую диаграмму распределения тега по документам."""
        count = len(self.applied_to)
        bar = "|" * min(count, 20)
        return f"{self.name} ({self.category or '—'}): {bar} ({count} документов)"

    def apply_to_metadata(self, metadata: "Metadata") -> None:
        """Добавляет имя тега в список тегов метаданных, если ещё не включён."""
        if self.name not in metadata.tags:
            metadata.tags.append(self.name)

    def is_relevant_to_insight(self, insight: "Insight") -> bool:
        """Проверяет, упоминается ли имя тега в описании инсайта."""
        return self.name.lower() in insight.description.lower()

    def annotate_report(self, report: "Report") -> None:
        """Добавляет комментарий в отчёт о применении тега."""
        from Comment import Comment  # локальный импорт
        comment_text = f"Тег '{self.name}' ({self.category or '—'}) применён к {len(self.applied_to)} документам."
        report.comments.append(Comment(
            comment_id=len(report.comments) + 1,
            document_id=report.report_id,
            user_id=report.author_id,
            content=comment_text,
            posted_at=datetime.now()
        ))

