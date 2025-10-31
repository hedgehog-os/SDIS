from datetime import datetime, timedelta

class DummyMeasurement:
    def __init__(self, value: float, recent: bool = True):
        self.value = value
        self._recent = recent

    def is_recent(self, threshold_minutes: int = 60) -> bool:
        return self._recent

class DummyTestCase:
    def __init__(self, testcase_id: int, measurements=None):
        self.testcase_id = testcase_id
        self.measurements = measurements or []
        self.procedure = None

import pytest
from experiments_and_equipments.Procedure import Procedure

@pytest.fixture
def procedure():
    return Procedure(
        procedure_id=1,
        name="Проверка давления",
        steps=["Включить насос", "Измерить давление"],
        expected_outcome="Давление в норме"
    )
def test_initial_state(procedure):
    assert procedure.procedure_id == 1
    assert procedure.name == "Проверка давления"
    assert procedure.steps == ["Включить насос", "Измерить давление"]
    assert procedure.expected_outcome == "Давление в норме"
    assert procedure.used_in == []

def test_add_test_case(procedure):
    tc = DummyTestCase(101)
    procedure.add_test_case(tc)
    assert tc in procedure.used_in
    assert tc.procedure == procedure

def test_add_test_case_no_duplicate(procedure):
    tc = DummyTestCase(102)
    procedure.add_test_case(tc)
    procedure.add_test_case(tc)
    assert procedure.used_in.count(tc) == 1

def test_remove_test_case(procedure):
    tc = DummyTestCase(103)
    procedure.add_test_case(tc)
    procedure.remove_test_case(tc)
    assert tc not in procedure.used_in
    assert tc.procedure is None

def test_get_test_case_ids(procedure):
    tc1 = DummyTestCase(201)
    tc2 = DummyTestCase(202)
    procedure.used_in = [tc1, tc2]
    assert procedure.get_test_case_ids() == [201, 202]

def test_count_measurements(procedure):
    m1 = DummyMeasurement(1.0)
    m2 = DummyMeasurement(2.0)
    tc1 = DummyTestCase(301, measurements=[m1])
    tc2 = DummyTestCase(302, measurements=[m2])
    procedure.used_in = [tc1, tc2]
    assert procedure.count_measurements() == 2

def test_get_recent_measurements(procedure):
    recent = DummyMeasurement(1.0, recent=True)
    old = DummyMeasurement(2.0, recent=False)
    tc = DummyTestCase(401, measurements=[recent, old])
    procedure.used_in = [tc]
    result = procedure.get_recent_measurements(minutes=60)
    assert result == [recent]

def test_summarize_output(procedure):
    tc = DummyTestCase(501, measurements=[DummyMeasurement(1.0)])
    procedure.used_in = [tc]
    summary = procedure.summarize()
    assert "Процедура #1: Проверка давления" in summary
    assert "Шагов: 2" in summary
    assert "Ожидаемый результат: Давление в норме" in summary
    assert "Тест-кейсы: 1 | Измерений: 1" in summary

def test_to_dict(procedure):
    tc = DummyTestCase(601)
    procedure.used_in = [tc]
    data = procedure.to_dict()
    assert data["procedure_id"] == 1
    assert data["name"] == "Проверка давления"
    assert data["steps"] == ["Включить насос", "Измерить давление"]
    assert data["expected_outcome"] == "Давление в норме"
    assert data["test_case_ids"] == [601]
