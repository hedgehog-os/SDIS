from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from persons.Supervisor import Supervisor

class Protocol:
    def __init__(self,
                 protocol_id: int,
                 title: str,
                 author_id: int,
                 created_at: Optional[datetime] = None,
                 steps: Optional[List[str]] = None,
                 reviewed_by: Optional[List["Supervisor"]] = None) -> None:
        self.protocol_id: int = protocol_id
        self.title: str = title
        self.author_id: int = author_id
        self.created_at: datetime = created_at or datetime.now()
        self.steps: List[str] = steps or []

        # Ассоциации
        self.reviewed_by: Optional[List["Supervisor"]] = reviewed_by

    def add_step(self, step: str) -> None:
        """Добавляет новый шаг в протокол."""
        if step and isinstance(step, str):
            self.steps.append(step)

    def remove_step(self, step: str) -> None:
        """Удаляет указанный шаг из протокола."""
        if step in self.steps:
            self.steps.remove(step)

    def get_step_count(self) -> int:
        """Возвращает количество шагов в протоколе."""
        return len(self.steps)

    def assign_supervisor(self, supervisor: "Supervisor") -> None:
        """Назначает супервизора для рецензирования протокола."""
        if self.reviewed_by is None:
            self.reviewed_by = []
        if supervisor not in self.reviewed_by:
            self.reviewed_by.append(supervisor)
            supervisor.reviewed_documents.append(self)

    def remove_supervisor(self, supervisor: "Supervisor") -> None:
        """Удаляет супервизора из списка рецензентов."""
        if self.reviewed_by and supervisor in self.reviewed_by:
            self.reviewed_by.remove(supervisor)
        if self in supervisor.reviewed_documents:
            supervisor.reviewed_documents.remove(self)

    def get_supervisor_names(self) -> List[str]:
        """Возвращает список имён всех супервизоров, назначенных на протокол."""
        return [s.fullname for s in self.reviewed_by] if self.reviewed_by else []

    def is_reviewed(self) -> bool:
        """Проверяет, есть ли хотя бы один супервизор."""
        return bool(self.reviewed_by)