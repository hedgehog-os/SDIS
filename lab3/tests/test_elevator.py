import pytest
from models.infrastructure.elevator import Elevator

@pytest.fixture
def elevator():
    return Elevator(elevator_id="E1", max_floor=10)

def test_initial_state(elevator):
    assert elevator.current_floor == 0
    assert elevator.is_operational is True
    assert elevator.maintenance_required is False
    assert elevator.passengers == []
    assert elevator.floor_history == []

def test_move_to_valid_floor(elevator):
    result = elevator.move_to_floor(5)
    assert result is True
    assert elevator.current_floor == 5
    assert elevator.floor_history == [5]

def test_move_to_invalid_floor_negative(elevator):
    result = elevator.move_to_floor(-1)
    assert result is False
    assert elevator.current_floor == 0

def test_move_to_invalid_floor_above_max(elevator):
    result = elevator.move_to_floor(11)
    assert result is False
    assert elevator.current_floor == 0

def test_move_when_shutdown(elevator):
    elevator.shutdown()
    result = elevator.move_to_floor(3)
    assert result is False

def test_move_when_under_maintenance(elevator):
    elevator.mark_for_maintenance()
    result = elevator.move_to_floor(2)
    assert result is False

def test_shutdown_and_restart(elevator):
    elevator.shutdown()
    assert elevator.is_operational is False
    elevator.restart()
    assert elevator.is_operational is True

def test_mark_and_clear_maintenance(elevator):
    elevator.mark_for_maintenance()
    assert elevator.maintenance_required is True
    elevator.clear_maintenance()
    assert elevator.maintenance_required is False

def test_board_passenger(elevator):
    elevator.board_passenger("Alice")
    assert elevator.passengers == ["Alice"]

def test_disembark_passenger_success(elevator):
    elevator.board_passenger("Bob")
    result = elevator.disembark_passenger("Bob")
    assert result is True
    assert "Bob" not in elevator.passengers

def test_disembark_passenger_not_found(elevator):
    result = elevator.disembark_passenger("Ghost")
    assert result is False

def test_is_empty_true(elevator):
    assert elevator.is_empty() is True

def test_is_empty_false(elevator):
    elevator.board_passenger("Charlie")
    assert elevator.is_empty() is False

def test_get_passenger_count(elevator):
    elevator.board_passenger("A")
    elevator.board_passenger("B")
    assert elevator.get_passenger_count() == 2

def test_last_floor_visited_none(elevator):
    assert elevator.last_floor_visited() is None

def test_last_floor_visited_value(elevator):
    elevator.move_to_floor(4)
    elevator.move_to_floor(7)
    assert elevator.last_floor_visited() == 7

def test_reset(elevator):
    elevator.board_passenger("X")
    elevator.move_to_floor(5)
    elevator.mark_for_maintenance()
    elevator.shutdown()
    elevator.reset()
    assert elevator.current_floor == 0
    assert elevator.passengers == []
    assert elevator.floor_history == []
    assert elevator.is_operational is True
    assert elevator.maintenance_required is False
