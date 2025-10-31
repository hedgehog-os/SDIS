import pytest
from datetime import datetime
from documents.ExperimentLog import ExperimentLog

@pytest.fixture
def log():
    return ExperimentLog(
        log_id=101,
        experiment_id=202,
        author_id=42,
        entries=["Температура: 37.5", "Давление: 120", "PH: 7.2"]
    )

class DummyExpert:
    def __init__(self, full_name="Др. Смирнов"):
        self.full_name = full_name
        self.comments = []
        self.commented_logs = []
        self.last_commented_at = None

def test_initial_state(log):
    assert log.log_id == 101
    assert log.experiment_id == 202
    assert log.author_id == 42
    assert len(log.entries) == 3
    assert log.comments is None

def test_log_measurement_adds_entry(log):
    log.log_measurement("Скорость: 5.2 м/с")
    assert "Скорость: 5.2 м/с" in log.entries
    assert len(log.entries) == 4

def test_summarize_log_output(log):
    summary = log.summarize_log()
    assert "Журнал #101 содержит 3 записей" in summary
    assert "Температура: 37.5" in summary

def test_export_raw_data(log):
    raw = log.export_raw_data()
    assert "Температура: 37.5" in raw
    assert raw.count("\n") == 2

def test_add_expert_comment_initializes_comments(log):
    expert = DummyExpert("Доктор А")
    log.add_expert_comment(expert, "Комментарий по температуре")
    assert expert in log.comments
    assert "Комментарий по температуре" in expert.comments
    assert log in expert.commented_logs
    assert expert.last_commented_at is not None

def test_add_expert_comment_does_not_duplicate(log):
    expert = DummyExpert("Доктор Б")
    log.add_expert_comment(expert, "Первый комментарий")
    log.add_expert_comment(expert, "Второй комментарий")
    assert log.comments.count(expert) == 1
    assert expert.comments == ["Первый комментарий", "Второй комментарий"]

def test_get_expert_names(log):
    expert1 = DummyExpert("Алексей")
    expert2 = DummyExpert("Мария")
    log.add_expert_comment(expert1, "Комментарий 1")
    log.add_expert_comment(expert2, "Комментарий 2")
    names = log.get_expert_names()
    assert names == ["Алексей", "Мария"]

def test_is_commented_true(log):
    expert = DummyExpert()
    log.add_expert_comment(expert, "Комментарий")
    assert log.is_commented() is True

def test_is_commented_false(log):
    assert log.is_commented() is False
