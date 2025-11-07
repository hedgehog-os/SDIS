import pytest
from models.operations.security_check import SecurityCheck

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

@pytest.fixture
def checkpoint():
    return SecurityCheck("CP-01")

def test_initialization(checkpoint):
    assert checkpoint.checkpoint_id == "CP-01"
    assert checkpoint.checked_passengers == []
    assert checkpoint.flagged_passengers == []
    assert checkpoint.blocked_passengers == []
    assert checkpoint.notes == []
    assert checkpoint.is_operational is True

def test_perform_check_success(checkpoint):
    p = DummyPassenger("Alice")
    result = checkpoint.perform_check(p)
    assert result == "Passenger Alice cleared at checkpoint CP-01"
    assert checkpoint.checked_passengers == ["Alice"]

def test_perform_check_already_checked(checkpoint):
    p = DummyPassenger("Bob")
    checkpoint.perform_check(p)
    result = checkpoint.perform_check(p)
    assert result == "Passenger Bob has already been checked."

def test_perform_check_blocked(checkpoint):
    p = DummyPassenger("Charlie")
    checkpoint.block_passenger(p, "Suspicious behavior")
    result = checkpoint.perform_check(p)
    assert result == "Passenger Charlie is blocked from passing checkpoint CP-01."

def test_perform_check_offline(checkpoint):
    p = DummyPassenger("Dana")
    checkpoint.shutdown()
    result = checkpoint.perform_check(p)
    assert result == "Checkpoint CP-01 is currently offline."

def test_has_been_checked_true(checkpoint):
    p = DummyPassenger("Eve")
    checkpoint.perform_check(p)
    assert checkpoint.has_been_checked(p) is True

def test_has_been_checked_false(checkpoint):
    p = DummyPassenger("Frank")
    assert checkpoint.has_been_checked(p) is False

def test_flag_passenger(checkpoint):
    p = DummyPassenger("Grace")
    checkpoint.flag_passenger(p, "Unusual luggage")
    assert "Grace" in checkpoint.flagged_passengers
    assert checkpoint.notes == ["Flagged Grace: Unusual luggage"]

def test_block_passenger(checkpoint):
    p = DummyPassenger("Heidi")
    checkpoint.block_passenger(p, "No valid ID")
    assert "Heidi" in checkpoint.blocked_passengers
    assert checkpoint.notes == ["Blocked Heidi: No valid ID"]

def test_reset(checkpoint):
    p = DummyPassenger("Ivan")
    checkpoint.perform_check(p)
    checkpoint.flag_passenger(p, "Late arrival")
    checkpoint.block_passenger(p, "Aggressive behavior")
    checkpoint.shutdown()
    checkpoint.reset()
    assert checkpoint.checked_passengers == []
    assert checkpoint.flagged_passengers == []
    assert checkpoint.blocked_passengers == []
    assert checkpoint.notes == []
    assert checkpoint.is_operational is True

def test_shutdown_and_restart(checkpoint):
    checkpoint.shutdown()
    assert checkpoint.is_operational is False
    checkpoint.restart()
    assert checkpoint.is_operational is True

def test_summary_active(checkpoint):
    p = DummyPassenger("Jack")
    checkpoint.perform_check(p)
    checkpoint.flag_passenger(p, "Extra screening")
    summary = checkpoint.summary()
    assert summary == "Checkpoint CP-01: 1 checked, 1 flagged, 0 blocked — ACTIVE"

def test_summary_offline(checkpoint):
    checkpoint.shutdown()
    summary = checkpoint.summary()
    assert summary == "Checkpoint CP-01: 0 checked, 0 flagged, 0 blocked — OFFLINE"
