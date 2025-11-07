import pytest
from models.operations.check_in_desk import CheckInDesk

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

class DummyTerminal:
    def __init__(self, name):
        self.name = name

@pytest.fixture
def desk():
    terminal = DummyTerminal("A")
    return CheckInDesk("D1", terminal)

def test_initialization(desk):
    assert desk.desk_id == "D1"
    assert desk.terminal.name == "A"
    assert desk.queue == []
    assert desk.is_operational is True
    assert desk.maintenance_required is False
    assert desk.processed_log == []

def test_add_to_queue_operational(desk):
    p = DummyPassenger("Alice")
    desk.add_to_queue(p)
    assert desk.queue == [p]

def test_add_to_queue_when_shutdown(desk):
    desk.shutdown()
    p = DummyPassenger("Bob")
    desk.add_to_queue(p)
    assert desk.queue == []

def test_add_to_queue_when_under_maintenance(desk):
    desk.mark_for_maintenance()
    p = DummyPassenger("Charlie")
    desk.add_to_queue(p)
    assert desk.queue == []

def test_process_next_success(desk):
    p = DummyPassenger("Dana")
    desk.add_to_queue(p)
    processed = desk.process_next()
    assert processed == p
    assert desk.processed_log == ["Dana"]
    assert desk.queue == []

def test_process_next_empty_queue(desk):
    assert desk.process_next() is None

def test_process_next_when_shutdown(desk):
    desk.shutdown()
    desk.add_to_queue(DummyPassenger("Eve"))
    assert desk.process_next() is None

def test_process_next_when_under_maintenance(desk):
    desk.mark_for_maintenance()
    desk.add_to_queue(DummyPassenger("Frank"))
    assert desk.process_next() is None

def test_is_busy_false(desk):
    for i in range(5):
        desk.add_to_queue(DummyPassenger(f"P{i}"))
    assert desk.is_busy() is False

def test_is_busy_true(desk):
    for i in range(6):
        desk.add_to_queue(DummyPassenger(f"P{i}"))
    assert desk.is_busy() is True

def test_mark_and_clear_maintenance(desk):
    desk.mark_for_maintenance()
    assert desk.maintenance_required is True
    desk.clear_maintenance()
    assert desk.maintenance_required is False

def test_shutdown_and_restart(desk):
    desk.shutdown()
    assert desk.is_operational is False
    desk.restart()
    assert desk.is_operational is True

def test_reset(desk):
    desk.add_to_queue(DummyPassenger("Gina"))
    desk.process_next()
    desk.mark_for_maintenance()
    desk.shutdown()
    desk.reset()
    assert desk.queue == []
    assert desk.processed_log == []
    assert desk.is_operational is True
    assert desk.maintenance_required is False

def test_get_queue_size(desk):
    desk.add_to_queue(DummyPassenger("Henry"))
    desk.add_to_queue(DummyPassenger("Ivy"))
    assert desk.get_queue_size() == 2

def test_get_processed_count(desk):
    desk.add_to_queue(DummyPassenger("Jack"))
    desk.process_next()
    assert desk.get_processed_count() == 1

def test_summary(desk):
    desk.terminal.name = "B"
    desk.add_to_queue(DummyPassenger("Kate"))
    assert desk.summary() == "Desk D1 in Terminal B (active, 1 in queue)"
    desk.shutdown()
    assert desk.summary() == "Desk D1 in Terminal B (offline, 1 in queue)"
