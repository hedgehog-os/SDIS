import pytest
from models.operations.boarding_procedure import BoardingProcedure

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

class DummyFlight:
    def __init__(self, flight_number, passengers):
        self.flight_number = flight_number
        self.passengers = passengers

@pytest.fixture
def flight():
    return DummyFlight("FL123", [DummyPassenger("Alice"), DummyPassenger("Bob")])

@pytest.fixture
def procedure(flight):
    return BoardingProcedure(flight)

def test_valid_boarding(procedure, flight):
    result = procedure.board(flight.passengers[0])
    assert result is True
    assert procedure.boarded_passengers == [flight.passengers[0]]

def test_boarding_locked(procedure, flight):
    procedure.lock()
    result = procedure.board(flight.passengers[0])
    assert result is False

def test_boarding_not_in_manifest(procedure):
    outsider = DummyPassenger("Charlie")
    result = procedure.board(outsider)
    assert result is False
    assert procedure.get_rejected_names() == ["Charlie"]

def test_boarding_duplicate(procedure, flight):
    procedure.board(flight.passengers[0])
    result = procedure.board(flight.passengers[0])
    assert result is False

def test_is_complete(procedure, flight):
    assert procedure.is_complete() is False
    for p in flight.passengers:
        procedure.board(p)
    assert procedure.is_complete() is True

def test_lock_and_unlock(procedure):
    procedure.lock()
    assert procedure.is_locked is True
    procedure.unlock()
    assert procedure.is_locked is False

def test_reset(procedure, flight):
    procedure.board(flight.passengers[0])
    procedure.board(DummyPassenger("Ghost"))  # rejected
    procedure.lock()
    procedure.reset()
    assert procedure.boarded_passengers == []
    assert procedure.rejected_passengers == []
    assert procedure.is_locked is False

def test_get_boarded_names(procedure, flight):
    procedure.board(flight.passengers[0])
    assert procedure.get_boarded_names() == ["Alice"]

def test_get_missing_passengers(procedure, flight):
    procedure.board(flight.passengers[0])
    missing = procedure.get_missing_passengers()
    assert missing == [flight.passengers[1]]

def test_get_rejected_names(procedure):
    outsider = DummyPassenger("Ghost")
    procedure.board(outsider)
    assert procedure.get_rejected_names() == ["Ghost"]

def test_summary(procedure, flight):
    procedure.board(flight.passengers[0])
    procedure.board(DummyPassenger("Ghost"))
    summary = procedure.summary()
    assert summary == "Boarding for flight FL123: 1/2 boarded, 1 rejected"
