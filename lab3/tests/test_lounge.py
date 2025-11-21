import pytest
from models.infrastructure.Lounge import Lounge

def test_valid_initialization():
    lounge = Lounge("Sky Lounge", 10, is_vip=True)
    assert lounge.name == "Sky Lounge"
    assert lounge.capacity == 10
    assert lounge.is_vip is True
    assert lounge.current_occupancy == 0
    assert lounge.is_open is True
    assert lounge.maintenance_required is False

def test_invalid_capacity():
    with pytest.raises(ValueError, match="Lounge capacity must be positive."):
        Lounge("Invalid", 0)

@pytest.fixture
def lounge():
    return Lounge("Relax Zone", 3)

def test_admit_guest_success(lounge):
    assert lounge.admit_guest("Alice") is True
    assert lounge.current_occupancy == 1
    assert "Alice" in lounge.guest_log

def test_admit_guest_when_full(lounge):
    lounge.admit_guest("A")
    lounge.admit_guest("B")
    lounge.admit_guest("C")
    assert lounge.admit_guest("D") is False

def test_admit_guest_when_closed(lounge):
    lounge.close()
    assert lounge.admit_guest("Ghost") is False

def test_admit_guest_when_under_maintenance(lounge):
    lounge.mark_for_maintenance()
    assert lounge.admit_guest("Ghost") is False

def test_release_guest_success(lounge):
    lounge.admit_guest("Bob")
    assert lounge.release_guest("Bob") is True
    assert "Bob" not in lounge.guest_log
    assert lounge.current_occupancy == 0

def test_release_guest_not_found(lounge):
    assert lounge.release_guest("Unknown") is False

def test_mark_and_clear_maintenance(lounge):
    lounge.mark_for_maintenance()
    assert lounge.maintenance_required is True
    lounge.clear_maintenance()
    assert lounge.maintenance_required is False

def test_close_and_open(lounge):
    lounge.close()
    assert lounge.is_open is False
    lounge.open()
    assert lounge.is_open is True

def test_is_available_true(lounge):
    assert lounge.is_available() is True

def test_is_available_false_due_to_full(lounge):
    lounge.admit_guest("A")
    lounge.admit_guest("B")
    lounge.admit_guest("C")
    assert lounge.is_available() is False

def test_is_available_false_due_to_maintenance(lounge):
    lounge.mark_for_maintenance()
    assert lounge.is_available() is False

def test_is_available_false_due_to_closed(lounge):
    lounge.close()
    assert lounge.is_available() is False

def test_occupancy_rate(lounge):
    lounge.admit_guest("A")
    lounge.admit_guest("B")
    assert lounge.occupancy_rate() == 0.67

def test_reset(lounge):
    lounge.admit_guest("X")
    lounge.mark_for_maintenance()
    lounge.close()
    lounge.reset()
    assert lounge.current_occupancy == 0
    assert lounge.guest_log == []
    assert lounge.maintenance_required is False
    assert lounge.is_open is True

def test_get_guest_list(lounge):
    lounge.admit_guest("Anna")
    lounge.admit_guest("Leo")
    guests = lounge.get_guest_list()
    assert guests == ["Anna", "Leo"]
    assert guests is not lounge.guest_log  # ensure copy

def test_is_guest_present(lounge):
    lounge.admit_guest("Mira")
    assert lounge.is_guest_present("Mira") is True
    assert lounge.is_guest_present("Ghost") is False
