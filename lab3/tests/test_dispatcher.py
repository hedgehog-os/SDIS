import pytest
from models.staff.Dispatcher import Dispatcher

class DummyFlight:
    def __init__(self, flight_number, destination):
        self.flight_number = flight_number
        self.destination = destination

@pytest.fixture
def dispatcher():
    return Dispatcher("Olga", "D-001")

def test_dispatch_flight(dispatcher):
    flight = DummyFlight("SU123", "Paris")
    msg = dispatcher.dispatch_flight(flight)
    assert msg == "Dispatcher Olga dispatched flight SU123"
    assert "SU123" in dispatcher.dispatched_flights
    assert dispatcher.dispatch_log[-1]["destination"] == "Paris"
    assert "Dispatched flight SU123 to Paris" in dispatcher.notes[-1]

def test_has_dispatched_true(dispatcher):
    flight = DummyFlight("SU124", "Berlin")
    dispatcher.dispatch_flight(flight)
    assert dispatcher.has_dispatched(flight) is True

def test_has_dispatched_false(dispatcher):
    flight = DummyFlight("SU125", "Rome")
    assert dispatcher.has_dispatched(flight) is False

def test_total_dispatched(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU126", "Madrid"))
    dispatcher.dispatch_flight(DummyFlight("SU127", "Lisbon"))
    assert dispatcher.total_dispatched() == 2

def test_get_last_dispatch(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU128", "Vienna"))
    dispatcher.dispatch_flight(DummyFlight("SU129", "Prague"))
    assert dispatcher.get_last_dispatch() == "SU129"

def test_get_last_dispatch_empty(dispatcher):
    assert dispatcher.get_last_dispatch() == "None"

def test_get_dispatches_by_destination(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU130", "Tokyo"))
    dispatcher.dispatch_flight(DummyFlight("SU131", "Tokyo"))
    dispatcher.dispatch_flight(DummyFlight("SU132", "Seoul"))
    result = dispatcher.get_dispatches_by_destination("Tokyo")
    assert result == ["SU130", "SU131"]

def test_generate_dispatch_report(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU133", "Dubai"))
    report = dispatcher.generate_dispatch_report()
    assert "Dispatch Report — Olga" in report
    assert "Total dispatched: 1" in report
    assert "• SU133 → Dubai" in report

def test_reset_log(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU134", "Cairo"))
    dispatcher.reset_log()
    assert dispatcher.dispatched_flights == []
    assert dispatcher.dispatch_log == []
    assert "Reset log with 1 entries" in dispatcher.notes[-1]

def test_archive_log(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU135", "Delhi"))
    dispatcher.archive_log()
    assert dispatcher.archive[-1] == dispatcher.dispatch_log
    assert "Archived 1 dispatch entries" in dispatcher.notes[-1]

def test_get_archive(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU136", "Helsinki"))
    dispatcher.archive_log()
    archive = dispatcher.get_archive()
    assert isinstance(archive, list)
    assert archive[0][0]["flight"] == "SU136"

def test_to_dict(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU137", "Stockholm"))
    dispatcher.archive_log()
    d = dispatcher.to_dict()
    assert d["name"] == "Olga"
    assert d["dispatch_id"] == "D-001"
    assert "SU137" in d["dispatched_flights"]
    assert d["archive_count"] == 1
    assert d["notes"] is not dispatcher.notes  # ensure it's a copy

def test_summary(dispatcher):
    dispatcher.dispatch_flight(DummyFlight("SU138", "Oslo"))
    dispatcher.archive_log()
    summary = dispatcher.summary()
    assert "Dispatcher Olga (ID: D-001)" in summary
    assert "- Total flights dispatched: 1" in summary
    assert "- Last dispatched: SU138" in summary
    assert "- Archive snapshots: 1" in summary
