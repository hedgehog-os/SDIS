from datetime import datetime, timedelta
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Procedure import Procedure
    from experiments_and_equipments.CaseTest import CaseTest


class Experiment:
    def __init__(self, experiment_id: int, title: str, procedure: "Procedure", start_date: Optional[datetime] = None) -> None:
        self.experiment_id: int = experiment_id
        self.title: str = title
        self.procedure: Procedure = procedure
        self.start_date: datetime = start_date or datetime.now()
        self.test_cases: List["CaseTest"] = []

    def add_test_case(self, test_case: "CaseTest") -> None:
        """Добавляет тест-кейс к эксперименту, если он ещё не включён."""
        if test_case not in self.test_cases:
            self.test_cases.append(test_case)

    def remove_test_case(self, test_case: "CaseTest") -> None:
        """Удаляет тест-кейс из эксперимента."""
        if test_case in self.test_cases:
            self.test_cases.remove(test_case)

    def get_test_case_ids(self) -> List[int]:
        """Возвращает список ID всех тест-кейсов."""
        return [tc.testcase_id for tc in self.test_cases]

    def get_completed_test_cases(self) -> List["CaseTest"]:
        """Возвращает список завершённых тест-кейсов."""
        return [tc for tc in self.test_cases if getattr(tc, "is_completed", False)]

    def get_pending_test_cases(self) -> List["CaseTest"]:
        """Возвращает список незавершённых тест-кейсов."""
        return [tc for tc in self.test_cases if not getattr(tc, "is_completed", False)]

    def is_active(self) -> bool:
        """Проверяет, есть ли незавершённые тест-кейсы."""
        return any(not getattr(tc, "is_completed", False) for tc in self.test_cases)

    def summarize(self) -> str:
        """Форматирует краткую информацию об эксперименте."""
        return (
            f"Experiment #{self.experiment_id}: {self.title}\n"
            f"Процедура: {self.procedure.name if hasattr(self.procedure, 'name') else '—'}\n"
            f"Дата начала: {self.start_date.strftime('%Y-%m-%d')}\n"
            f"Тест-кейсы: {len(self.test_cases)} ({len(self.get_completed_test_cases())}, {len(self.get_pending_test_cases())})"
        )

    def to_dict(self) -> dict:
        """Сериализует эксперимент в словарь."""
        return {
            "experiment_id": self.experiment_id,
            "title": self.title,
            "procedure": getattr(self.procedure, "name", None),
            "start_date": self.start_date.isoformat(),
            "test_case_ids": self.get_test_case_ids()
        }

    def started_recently(self, days: int = 7) -> bool:
        """Проверяет, начался ли эксперимент в последние N дней."""
        return self.start_date >= datetime.now() - timedelta(days=days)
