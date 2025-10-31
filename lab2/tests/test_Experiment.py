from datetime import datetime

class DummyProcedure:
    def __init__(self, name="Стандартная процедура"):
        self.name = name

class DummyTestCase:
    def __init__(self, testcase_id: int, is_completed: bool = False):
        self.testcase_id = testcase_id
        self.is_completed = is_completed
import pytest
from experiments_and_equipments.Experiment import Experiment

@pytest.fixture
def experiment():
    return Experiment(
        experiment_id=1,
        title="Изучение термостойкости",
        procedure=DummyProcedure(),
        start_date=datetime(2024, 1, 1)
    )
def test_initial_state(experiment):
    assert experiment.experiment_id == 1
    assert experiment.title == "Изучение термостойкости"
    assert experiment.procedure.name == "Стандартная процедура"
    assert experiment.test_cases == []

def test_add_test_case(experiment):
    tc = DummyTestCase(101)
    experiment.add_test_case(tc)
    assert tc in experiment.test_cases

def test_add_test_case_no_duplicate(experiment):
    tc = DummyTestCase(102)
    experiment.add_test_case(tc)
    experiment.add_test_case(tc)
    assert experiment.test_cases.count(tc) == 1

def test_remove_test_case(experiment):
    tc = DummyTestCase(103)
    experiment.add_test_case(tc)
    experiment.remove_test_case(tc)
    assert tc not in experiment.test_cases

def test_get_test_case_ids(experiment):
    tc1 = DummyTestCase(201)
    tc2 = DummyTestCase(202)
    experiment.test_cases = [tc1, tc2]
    assert experiment.get_test_case_ids() == [201, 202]

def test_get_completed_test_cases(experiment):
    tc1 = DummyTestCase(301, is_completed=True)
    tc2 = DummyTestCase(302, is_completed=False)
    experiment.test_cases = [tc1, tc2]
    completed = experiment.get_completed_test_cases()
    assert completed == [tc1]

def test_get_pending_test_cases(experiment):
    tc1 = DummyTestCase(401, is_completed=True)
    tc2 = DummyTestCase(402, is_completed=False)
    experiment.test_cases = [tc1, tc2]
    pending = experiment.get_pending_test_cases()
    assert pending == [tc2]

def test_is_active_true(experiment):
    tc = DummyTestCase(501, is_completed=False)
    experiment.test_cases = [tc]
    assert experiment.is_active() is True

def test_is_active_false(experiment):
    tc = DummyTestCase(502, is_completed=True)
    experiment.test_cases = [tc]
    assert experiment.is_active() is False

def test_summarize_output(experiment):
    tc1 = DummyTestCase(601, is_completed=True)
    tc2 = DummyTestCase(602, is_completed=False)
    experiment.test_cases = [tc1, tc2]
    summary = experiment.summarize()
    assert "Experiment #1: Изучение термостойкости" in summary
    assert "Тест-кейсы: 2 (1, 1)" in summary

def test_to_dict(experiment):
    tc1 = DummyTestCase(701)
    experiment.test_cases = [tc1]
    data = experiment.to_dict()
    assert data["experiment_id"] == 1
    assert data["title"] == "Изучение термостойкости"
    assert data["procedure"] == "Стандартная процедура"
    assert data["test_case_ids"] == [701]

def test_started_recently_true():
    recent = Experiment(2, "Недавний", DummyProcedure(), start_date=datetime.now())
    assert recent.started_recently(days=7) is True

def test_started_recently_false():
    old = Experiment(3, "Старый", DummyProcedure(), start_date=datetime(2020, 1, 1))
    assert old.started_recently(days=7) is False
