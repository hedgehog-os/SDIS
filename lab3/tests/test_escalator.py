import pytest
from models.infrastructure.escalator import Escalator

def test_valid_initialization():
    e = Escalator("E1", "up")
    assert e.escalator_id == "E1"
    assert e.direction == "up"
    assert e.is_operational is True
    assert e.maintenance_required is False
    assert e.passenger_log == []
    assert e.direction_history == ["up"]

def test_invalid_direction():
    with pytest.raises(ValueError, match="Invalid direction: sideways"):
        Escalator("E2", "sideways")

@pytest.fixture
def escalator():
    return Escalator("E3", "down")

def test_stop_and_start(escalator):
    escalator.stop()
    assert escalator.is_operational is False
    escalator.start()
    assert escalator.is_operational is True

def test_mark_and_clear_maintenance(escalator):
    escalator.mark_for_maintenance()
    assert escalator.maintenance_required is True
    escalator.clear_maintenance()
    assert escalator.maintenance_required is False

def test_reverse_direction(escalator):
    original = escalator.direction
    escalator.reverse_direction()
    assert escalator.direction != original
    assert escalator.direction_history[-1] == escalator.direction
    assert escalator.get_direction_changes() == 1

def test_board_passenger(escalator):
    escalator.board_passenger("Alice")
    escalator.board_passenger("Bob")
    assert escalator.passenger_log == ["Alice", "Bob"]
    assert escalator.get_passenger_count() == 2

def test_is_safe_to_use(escalator):
    assert escalator.is_safe_to_use() is True
    escalator.mark_for_maintenance()
    assert escalator.is_safe_to_use() is False
    escalator.clear_maintenance()
    escalator.stop()
    assert escalator.is_safe_to_use() is False

def test_reset(escalator):
    escalator.board_passenger("X")
    escalator.reverse_direction()
    escalator.mark_for_maintenance()
    escalator.stop()
    escalator.reset()
    assert escalator.is_operational is True
    assert escalator.maintenance_required is False
    assert escalator.passenger_log == []
    assert escalator.direction_history == [escalator.direction]

def test_get_direction_changes(escalator):
    assert escalator.get_direction_changes() == 0
    escalator.reverse_direction()
    escalator.reverse_direction()
    assert escalator.get_direction_changes() == 2

def test_last_direction(escalator):
    escalator.reverse_direction()
    escalator.reverse_direction()
    assert escalator.last_direction() == escalator.direction
