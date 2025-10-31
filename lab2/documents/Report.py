from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from Exceptions import ReportReviewerNotAssignedError, ReportChartNotFoundError

if TYPE_CHECKING:
    from persons.CommitteeMember import CommitteeMember
    from metadata_and_analitics.Chart import Chart
    from metadata_and_analitics.Summary import Summary
    from metadata_and_analitics.Comment import Comment


class Report:
    def __init__(self,
                 report_id: int,
                 title: str,
                 author_id: int,
                 created_at: Optional[datetime] = None,
                 charts: Optional[List["Chart"]] = None,
                 summary: Optional["Summary"] = None,
                 reviewed_by: Optional[List["CommitteeMember"]] = None,
                 comments: List["Comment"] = None) -> None:
        self.report_id: int = report_id
        self.title: str = title
        self.author_id: int = author_id
        self.created_at: datetime = created_at or datetime.now()

        # Ассоциации
        self.charts: List["Chart"] = charts or []
        self.summary: Optional["Summary"] = summary
        self.reviewed_by: Optional[List["CommitteeMember"]] = reviewed_by
        self.comments: List["Comment"] = comments

    def add_chart(self, chart: "Chart") -> None:
        """Добавляет диаграмму в отчёт."""
        self.charts.append(chart)

    def remove_chart(self, chart: "Chart") -> None:
        if chart not in self.charts:
            raise ReportChartNotFoundError("Диаграмма не найдена в отчёте.")
        self.charts.remove(chart)

    def assign_summary(self, summary: "Summary") -> None:
        """Привязывает резюме к отчёту и обновляет обратную ссылку."""
        self.summary = summary
        summary.report = self

    def clear_summary(self) -> None:
        """Удаляет связанное резюме."""
        if self.summary:
            self.summary.report = None
        self.summary = None

    def assign_committee_member(self, member: "CommitteeMember") -> None:
        """Назначает члена комиссии для рецензирования отчёта."""
        if self.reviewed_by is None:
            self.reviewed_by = []
        if member not in self.reviewed_by:
            self.reviewed_by.append(member)
            member.evaluated_reports.append(self)
            member.last_evaluation_date = datetime.now()

    def remove_committee_member(self, member: "CommitteeMember") -> None:
        """Удаляет члена комиссии из списка рецензентов."""
        if self.reviewed_by and member in self.reviewed_by:
            self.reviewed_by.remove(member)
        if self in member.evaluated_reports:
            member.evaluated_reports.remove(self)

    def add_evaluation_note(self, member: "CommitteeMember", note: str) -> None:
        """Добавляет комментарий от члена комиссии, если он связан с отчётом."""
        if self.reviewed_by and member in self.reviewed_by:
            member.evaluation_notes.append(note)
            member.last_evaluation_date = datetime.now()
        else:
            raise ReportReviewerNotAssignedError("Член комиссии не назначен на этот отчёт.")

    def get_committee_roles(self) -> List[str]:
        """Возвращает список ролей всех рецензентов отчёта."""
        return [m.role for m in self.reviewed_by if m.role] if self.reviewed_by else []

    def is_reviewed(self) -> bool:
        """Проверяет, есть ли хотя бы один рецензент."""
        return bool(self.reviewed_by)

    def export_as_text(self) -> str:
        """Возвращает текстовое представление отчёта."""
        lines = [
            f"Отчёт: {self.title}",
            f"Автор ID: {self.author_id}",
            f"Создан: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"Диаграмм: {len(self.charts)}",
            f"Резюме: {'есть' if self.summary else 'отсутствует'}",
            f"Рецензентов: {len(self.reviewed_by) if self.reviewed_by else 0}"
        ]
        return "\n".join(lines)

    def count_charts_by_type(self) -> dict[str, int]:
        """Возвращает количество диаграмм по типу."""
        chart_count: dict[str, int] = {}
        for chart in self.charts:
            chart_type = chart.chart_type
            chart_count[chart_type] = chart_count.get(chart_type, 0) + 1
        return chart_count

    def get_reviewers_by_role(self, role: str) -> List[str]:
        """Возвращает имена рецензентов с заданной ролью."""
        if not self.reviewed_by:
            return []
        return [m.full_name for m in self.reviewed_by if m.role == role]
