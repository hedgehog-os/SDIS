from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Report import Report
    from metadata_and_analitics.Comment import Comment


class Insight:
    def __init__(self, insight_id: int, description: str, related_documents: List[int]) -> None:
        self.insight_id: int = insight_id
        self.description: str = description
        self.related_documents: List[int] = related_documents

    def add_related_document(self, document_id: int) -> None:
        """Добавляет документ к списку связанных, если он ещё не включён."""
        if document_id not in self.related_documents:
            self.related_documents.append(document_id)

    def remove_related_document(self, document_id: int) -> None:
        """Удаляет документ из списка связанных."""
        if document_id in self.related_documents:
            self.related_documents.remove(document_id)

    def is_related_to(self, document_id: int) -> bool:
        """Проверяет, связан ли инсайт с указанным документом."""
        return document_id in self.related_documents

    def summarize(self, max_length: int = 100) -> str:
        """Возвращает краткое описание инсайта."""
        return self.description[:max_length] + ("..." if len(self.description) > max_length else "")

    def format_for_display(self) -> str:
        """Форматирует инсайт для отображения."""
        return (
            f"Insight #{self.insight_id}\n"
            f"Описание: {self.description}\n"
            f"Связанные документы: {', '.join(map(str, self.related_documents)) or '—'}"
        )

    def get_related_count(self) -> int:
        """Возвращает количество связанных документов."""
        return len(self.related_documents)

    def to_dict(self) -> dict:
        """Сериализует инсайт в словарь."""
        return {
            "insight_id": self.insight_id,
            "description": self.description,
            "related_documents": self.related_documents
        }

    def contains_keyword(self, keyword: str) -> bool:
        """Проверяет, содержит ли описание инсайта заданное слово."""
        return keyword.lower() in self.description.lower()

    def attach_to_report(self, report: "Report") -> None:
        """Добавляет ID всех связанных документов в комментарий отчёта."""
        if self.related_documents:
            from metadata_and_analitics.Comment import Comment  # локальный импорт
            comment_text = (
                f"Инсайт #{self.insight_id} связан с документами: "
                f"{', '.join(map(str, self.related_documents))}"
            )
            report.comments.append(Comment(
                comment_id=len(report.comments) + 1,
                document_id=report.report_id,
                user_id=report.author_id,
                content=comment_text,
                posted_at=datetime.now()
            ))



    def visualize_links(self) -> str:
        """Генерирует текстовую карту связей инсайта с документами."""
        if not self.related_documents:
            return "Нет связанных документов."
        lines = [f"Insight #{self.insight_id} связан с:"]
        for doc_id in self.related_documents:
            lines.append(f"Документ ID: {doc_id}")
        return "\n".join(lines)
