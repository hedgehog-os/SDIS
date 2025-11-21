import pytest
from models.operations.BoardingPass import BoardingPass

class DummyTicket:
    def __init__(self, ticket_number, seat_number, is_active=True):
        self.ticket_number = ticket_number
        self.seat_number = seat_number
        self.is_active = is_active

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

def test_valid_initialization():
    ticket = DummyTicket("TK123", "12A")
    passenger = DummyPassenger("Alice Smith")
    bp = BoardingPass(ticket, passenger, "B12")
    assert bp.ticket == ticket
    assert bp.passenger == passenger
    assert bp.gate_number == "B12"
    assert bp.is_scanned is False
    assert bp.scan_log == []

def test_invalid_gate_number_format():
    ticket = DummyTicket("TK123", "12A")
    passenger = DummyPassenger("Bob")
    with pytest.raises(ValueError, match="Invalid gate number format: Z9"):
        BoardingPass(ticket, passenger, "Z9")

def test_scan_and_log(bp):
    bp.scan("2025-11-06T10:00")
    bp.scan("2025-11-06T10:05")
    assert bp.is_scanned is True
    assert bp.scan_log == ["2025-11-06T10:00", "2025-11-06T10:05"]
    assert bp.scanned_times() == 2

def test_reset_scan(bp):
    bp.scan("T1")
    bp.reset_scan()
    assert bp.is_scanned is False
    assert bp.scan_log == []

def test_get_passenger_name(bp):
    assert bp.get_passenger_name() == "Alice Smith"

def test_get_ticket_info(bp):
    assert bp.get_ticket_info() == "TK123 (12A)"

def test_is_valid_true(bp):
    assert bp.is_valid() is True

def test_is_valid_false_if_scanned(bp):
    bp.scan()
    assert bp.is_valid() is False

def test_is_valid_false_if_ticket_inactive():
    ticket = DummyTicket("TK999", "1C", is_active=False)
    passenger = DummyPassenger("Charlie")
    bp = BoardingPass(ticket, passenger, "C1")
    assert bp.is_valid() is False

def test_summary(bp):
    assert bp.summary() == "Alice Smith → Gate B12, Seat 12A"

@pytest.fixture
def bp():
    ticket = DummyTicket("TK123", "12A")
    passenger = DummyPassenger("Alice Smith")
    return BoardingPass(ticket, passenger, "B12")
