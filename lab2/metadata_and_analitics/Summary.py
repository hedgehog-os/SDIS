from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Report import Report
    from metadata_and_analitics.Insight import Insight
    from metadata_and_analitics.Keyword import Keyword
    from metadata_and_analitics.Chart import Chart
    from documents.Document import Document


class Summary:
    def __init__(self,
                 summary_id: int,
                 content: str,
                 generated_at: Optional[datetime] = None,
                 report: Optional["Report"] = None) -> None:
        self.summary_id: int = summary_id
        self.content: str = content
        self.generated_at: datetime = generated_at or datetime.now()

        # Ассоциация
        self.report: Optional["Report"] = report

    def update_content(self, new_content: str) -> None:
        """Обновляет текст сводки и фиксирует время генерации."""
        if new_content and isinstance(new_content, str):
            self.content = new_content
            self.generated_at = datetime.now()

    def get_summary_excerpt(self, max_length: int = 120) -> str:
        """Возвращает краткий фрагмент сводки."""
        return self.content[:max_length] + ("..." if len(self.content) > max_length else "")

    def is_recent(self, threshold_minutes: int = 60) -> bool:
        """Проверяет, была ли сводка создана недавно."""
        delta = datetime.now() - self.generated_at
        return delta.total_seconds() < threshold_minutes * 60

    def format_for_display(self) -> str:
        """Форматирует сводку для отображения."""
        return (
            f"Сводка #{self.summary_id}\n"
            f"Дата генерации: {self.generated_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Связанный отчёт: {self.report.title if self.report else '—'}\n"
            f"Содержание:\n{self.get_summary_excerpt(200)}"
        )

    def link_to_report(self, report: "Report") -> None:
        """Привязывает сводку к отчёту, если ещё не связана."""
        self.report = report
        if not hasattr(report, "summaries"):
            report.summaries = []
        if self not in report.summaries:
            report.summaries.append(self)

    def to_dict(self) -> dict:
        """Сериализует сводку в словарь."""
        return {
            "summary_id": self.summary_id,
            "content": self.content,
            "generated_at": self.generated_at.isoformat(),
            "report_id": self.report.report_id if self.report else None
        }

    def extract_insights(self, insights: List["Insight"]) -> List["Insight"]:
        """Возвращает инсайты, упомянутые в содержании сводки."""
        return [
            insight for insight in insights
            if str(insight.insight_id) in self.content or
               insight.description.lower() in self.content.lower()
        ]

    def extract_keywords(self, keywords: List["Keyword"]) -> List["Keyword"]:
        """Возвращает ключевые слова, найденные в содержании сводки."""
        return [
            keyword for keyword in keywords
            if keyword.word.lower() in self.content.lower()
        ]

    def referenced_charts(self, charts: List["Chart"]) -> List["Chart"]:
        """Определяет, какие диаграммы упомянуты в сводке по названию или ID."""
        return [
            chart for chart in charts
            if chart.title.lower() in self.content.lower() or
               str(chart.chart_id) in self.content
        ]

    def referenced_documents(self, documents: List["Document"]) -> List["Document"]:
        """Возвращает документы, упомянутые в содержании сводки по ID или заголовку."""
        return [
            doc for doc in documents
            if str(doc.document_id) in self.content or
               doc.title.lower() in self.content.lower()
        ]

    def semantic_map(self,
                     insights: List["Insight"],
                     keywords: List["Keyword"],
                     charts: List["Chart"],
                     documents: List["Document"]) -> dict:
        """Возвращает словарь всех сущностей, упомянутых в сводке."""
        return {
            "insights": [i.insight_id for i in self.extract_insights(insights)],
            "keywords": [k.word for k in self.extract_keywords(keywords)],
            "charts": [c.chart_id for c in self.referenced_charts(charts)],
            "documents": [d.document_id for d in self.referenced_documents(documents)]
        }
