from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from persons.ExternalExpert import ExternalExpert  # только для type hints


class ExperimentLog:
    def __init__(self,
                 log_id: int,
                 experiment_id: int,
                 author_id: int,
                 entries: List[str],
                 created_at: Optional[datetime] = None,
                 comments: Optional[List["ExternalExpert"]] = None) -> None:
        self.log_id: int = log_id
        self.experiment_id: int = experiment_id
        self.author_id: int = author_id
        self.entries: List[str] = entries
        self.created_at: datetime = created_at or datetime.now()

        # Ассоциации
        self.comments: Optional[List["ExternalExpert"]] = comments

    def log_measurement(self, entry: str) -> None:
        """Добавляет новую запись измерения в журнал."""
        self.entries.append(entry)

    def summarize_log(self) -> str:
        """Возвращает краткое текстовое описание журнала эксперимента."""
        summary = f"Журнал #{self.log_id} содержит {len(self.entries)} записей.\n"
        preview = "\n".join(self.entries[:3])  # первые 3 записи
        return summary + "Пример записей:\n" + preview

    def flag_anomaly(self, keyword: str) -> List[str]:
        """Выделяет записи, содержащие указанный признак аномалии."""
        return [entry for entry in self.entries if keyword.lower() in entry.lower()]

    def export_raw_data(self) -> str:
        """Экспортирует все записи как текст."""
        return "\n".join(self.entries)

    def add_expert_comment(self, expert: "ExternalExpert", comment: str) -> None:
        """Добавляет комментарий от внешнего эксперта и обновляет ассоциацию."""
        if self.comments is None:
            self.comments = []
        if expert not in self.comments:
            self.comments.append(expert)
        expert.comments.append(comment)
        expert.commented_logs.append(self)
        expert.last_commented_at = datetime.now()

    def get_expert_names(self) -> List[str]:
        """Возвращает список имён всех экспертов, прокомментировавших журнал."""
        return [e.full_name for e in self.comments] if self.comments else []

    def is_commented(self) -> bool:
        """Проверяет, есть ли хотя бы один экспертный комментарий."""
        return bool(self.comments)
