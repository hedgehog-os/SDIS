from datetime import datetime, timedelta
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Report import Report


class CommitteeMember:

    roles = {
        'chair', 'reviewer', 'observer', 'secretary'
    }

    def __init__(self,
                 member_id: int,
                 full_name: str,
                 role: Optional[str] = None,
                 evaluated_reports: Optional[List["Report"]] = None,
                 evaluation_notes: Optional[List[str]] = None,
                 last_evaluation_date: Optional[datetime] = None) -> None:
        self.member_id: int = member_id
        self.full_name: str = full_name
        self.role: Optional[str] = role
        self.evaluated_reports: List["Report"] = evaluated_reports or []
        self.evaluation_notes: List[str] = evaluation_notes or []
        self.last_evaluation_date: Optional[datetime] = last_evaluation_date

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if value not in self.roles:
            raise ValueError(f'Недопустимый статус: {value}')
        self._role = value

    def evaluate_report(self, report: "Report", note: Optional[str] = None) -> None:
        """Добавляет отчёт в список оценённых и при необходимости комментарий."""
        if report not in self.evaluated_reports:
            self.evaluated_reports.append(report)
        if report.reviewed_by is None:
            report.reviewed_by = []
        if self not in report.reviewed_by:
            report.reviewed_by.append(self)
        if note:
            self.evaluation_notes.append(note)
        self.last_evaluation_date = datetime.now()

    def remove_report(self, report: "Report") -> None:
        """Удаляет отчёт из списка оценённых и из отчёта."""
        if report in self.evaluated_reports:
            self.evaluated_reports.remove(report)
        if report.reviewed_by and self in report.reviewed_by:
            report.reviewed_by.remove(self)

    def count_evaluated_reports(self) -> int:
        """Возвращает количество отчётов, оценённых членом комиссии."""
        return len(self.evaluated_reports)

    def get_recent_reports(self, days: int = 30) -> List["Report"]:
        """Возвращает отчёты, оценённые за последние N дней."""
        threshold = datetime.now() - timedelta(days=days)
        return [r for r in self.evaluated_reports if r.created_at >= threshold]

    def get_notes_for_report(self, report: "Report") -> List[str]:
        """Возвращает комментарии, относящиеся к конкретному отчёту."""
        if report in self.evaluated_reports:
            return self.evaluation_notes
        return []

    def summarize(self) -> str:
        """Форматирует краткую информацию о члене комиссии."""
        return (
            f"Комиссия #{self.member_id}: {self.full_name}\n"
            f"Роль: {self.role}\n"
            f"Оценено отчётов: {self.count_evaluated_reports()}\n"
            f"Последняя оценка: {self.last_evaluation_date.strftime('%Y-%m-%d') if self.last_evaluation_date else '—'}"
        )

    def to_dict(self) -> dict:
        """Сериализует члена комиссии в словарь."""
        return {
            "member_id": self.member_id,
            "full_name": self.full_name,
            "role": self.role,
            "evaluated_report_ids": [r.report_id for r in self.evaluated_reports],
            "evaluation_notes": self.evaluation_notes,
            "last_evaluation_date": self.last_evaluation_date.isoformat() if self.last_evaluation_date else None
        }
