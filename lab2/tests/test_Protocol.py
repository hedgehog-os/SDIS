class DummySupervisor:
    def __init__(self, fullname="Иван Петров"):
        self.fullname = fullname
        self.reviewed_documents = []

import pytest
from datetime import datetime
from documents.Protocol import Protocol

@pytest.fixture
def protocol():
    return Protocol(
        protocol_id=1,
        title="Протокол эксперимента",
        author_id=42,
        steps=["Подготовка", "Измерение", "Анализ"]
    )

def test_initial_state(protocol):
    assert protocol.title == "Протокол эксперимента"
    assert protocol.author_id == 42
    assert protocol.get_step_count() == 3
    assert protocol.reviewed_by is None

def test_add_step(protocol):
    protocol.add_step("Отчёт")
    assert "Отчёт" in protocol.steps
    assert protocol.get_step_count() == 4

def test_add_step_invalid(protocol):
    protocol.add_step("")
    protocol.add_step(None)
    assert protocol.get_step_count() == 3  # ничего не добавилось

def test_remove_step(protocol):
    protocol.remove_step("Измерение")
    assert "Измерение" not in protocol.steps
    assert protocol.get_step_count() == 2

def test_remove_step_nonexistent(protocol):
    protocol.remove_step("Не существует")
    assert protocol.get_step_count() == 3  # ничего не удалилось

def test_assign_supervisor(protocol):
    supervisor = DummySupervisor("Анна Смирнова")
    protocol.assign_supervisor(supervisor)
    assert supervisor in protocol.reviewed_by
    assert protocol in supervisor.reviewed_documents

def test_assign_supervisor_no_duplicates(protocol):
    supervisor = DummySupervisor("Анна Смирнова")
    protocol.assign_supervisor(supervisor)
    protocol.assign_supervisor(supervisor)
    assert protocol.reviewed_by.count(supervisor) == 1
    assert supervisor.reviewed_documents.count(protocol) == 1

def test_remove_supervisor(protocol):
    supervisor = DummySupervisor("Анна Смирнова")
    protocol.assign_supervisor(supervisor)
    protocol.remove_supervisor(supervisor)
    assert supervisor not in protocol.reviewed_by
    assert protocol not in supervisor.reviewed_documents

def test_get_supervisor_names(protocol):
    s1 = DummySupervisor("Анна")
    s2 = DummySupervisor("Павел")
    protocol.assign_supervisor(s1)
    protocol.assign_supervisor(s2)
    names = protocol.get_supervisor_names()
    assert names == ["Анна", "Павел"]

def test_is_reviewed_true(protocol):
    supervisor = DummySupervisor()
    protocol.assign_supervisor(supervisor)
    assert protocol.is_reviewed() is True

def test_is_reviewed_false(protocol):
    assert protocol.is_reviewed() is False
