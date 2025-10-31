from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.CaseTest import CaseTest
    from experiments_and_equipments.Measurement import Measurement



class Procedure:
    def __init__(self,
                 procedure_id: int,
                 name: str,
                 steps: List[str],
                 expected_outcome: Optional[str] = None,
                 used_in: Optional[List["CaseTest"]] = None) -> None:
        self.procedure_id: int = procedure_id
        self.name: str = name
        self.steps: List[str] = steps
        self.expected_outcome: Optional[str] = expected_outcome

        # Ассоциация
        self.used_in: List["CaseTest"] = used_in or []

    def add_test_case(self, test_case: "CaseTest") -> None:
        """Привязывает тест-кейс к процедуре, если он ещё не связан."""
        if test_case not in self.used_in:
            self.used_in.append(test_case)
            test_case.procedure = self

    def remove_test_case(self, test_case: "CaseTest") -> None:
        """Удаляет тест-кейс из процедуры."""
        if test_case in self.used_in:
            self.used_in.remove(test_case)
            if test_case.procedure == self:
                test_case.procedure = None

    def get_test_case_ids(self) -> List[int]:
        """Возвращает список ID всех тест-кейсов, использующих эту процедуру."""
        return [tc.testcase_id for tc in self.used_in]

    def count_measurements(self) -> int:
        """Подсчитывает общее количество измерений во всех тест-кейсах."""
        return sum(len(tc.measurements or []) for tc in self.used_in)

    def get_recent_measurements(self, minutes: int = 60) -> List["Measurement"]:
        """Возвращает все недавние измерения из связанных тест-кейсов."""
        recent = []
        for tc in self.used_in:
            if tc.measurements:
                recent.extend([m for m in tc.measurements if m.is_recent(minutes)])
        return recent

    def summarize(self) -> str:
        """Форматирует краткую информацию о процедуре."""
        return (
            f"Процедура #{self.procedure_id}: {self.name}\n"
            f"Шагов: {len(self.steps)}\n"
            f"Ожидаемый результат: {self.expected_outcome or '—'}\n"
            f"Тест-кейсы: {len(self.used_in)} | Измерений: {self.count_measurements()}"
        )

    def to_dict(self) -> dict:
        """Сериализует процедуру в словарь."""
        return {
            "procedure_id": self.procedure_id,
            "name": self.name,
            "steps": self.steps,
            "expected_outcome": self.expected_outcome,
            "test_case_ids": self.get_test_case_ids()
        }
