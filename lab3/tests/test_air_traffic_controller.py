import pytest
from models.staff.air_traffic_controller import AirTrafficController

class DummyFlight:
    def __init__(self, flight_number):
        self.flight_number = flight_number

@pytest.fixture
def controller():
    return AirTrafficController("Ivan", "TWR-01")

@pytest.fixture
def other_controller():
    return AirTrafficController("Olga", "TWR-02")

def test_authorize_takeoff(controller):
    flight = DummyFlight("SU123")
    msg = controller.authorize_takeoff(flight)
    assert msg == "Flight SU123 authorized for takeoff by Ivan"
    assert controller.is_controlling(flight) is True
    assert "SU123" in controller.get_active_flight_numbers()
    assert msg in controller.log

def test_release_flight(controller):
    flight = DummyFlight("SU124")
    controller.authorize_takeoff(flight)
    controller.release_flight(flight)
    assert controller.is_controlling(flight) is False
    assert "released from control" in controller.log[-1]

def test_is_controlling(controller):
    flight = DummyFlight("SU125")
    assert controller.is_controlling(flight) is False
    controller.authorize_takeoff(flight)
    assert controller.is_controlling(flight) is True

def test_get_active_flight_numbers(controller):
    f1 = DummyFlight("SU126")
    f2 = DummyFlight("SU127")
    controller.authorize_takeoff(f1)
    controller.authorize_takeoff(f2)
    assert controller.get_active_flight_numbers() == ["SU126", "SU127"]

def test_summary(controller):
    f1 = DummyFlight("SU128")
    controller.authorize_takeoff(f1)
    summary = controller.summary()
    assert "Controller Ivan (Tower TWR-01)" in summary
    assert "1 active flight" in summary

def test_to_dict(controller):
    f1 = DummyFlight("SU129")
    controller.authorize_takeoff(f1)
    d = controller.to_dict()
    assert d["name"] == "Ivan"
    assert d["control_tower_id"] == "TWR-01"
    assert d["active_flights"] == ["SU129"]
    assert d["log"] == controller.log
    assert d["log"] is not controller.log  # ensure it's a copy

def test_handover_success(controller, other_controller):
    flight = DummyFlight("SU130")
    controller.authorize_takeoff(flight)
    msg = controller.handover_to(flight, other_controller)
    assert "handed over from Ivan" in msg
    assert other_controller.is_controlling(flight) is True
    assert msg in controller.log
    assert msg in other_controller.log

def test_handover_failure(controller, other_controller):
    flight = DummyFlight("SU131")
    msg = controller.handover_to(flight, other_controller)
    assert msg == "Flight SU131 is not under control of Ivan"
    assert msg in controller.log
    assert flight not in other_controller.active_flights

def test_get_flight_log(controller):
    f1 = DummyFlight("SU132")
    f2 = DummyFlight("SU133")
    controller.authorize_takeoff(f1)
    controller.authorize_takeoff(f2)
    controller.release_flight(f1)
    log = controller.get_flight_log(f1)
    assert all("SU132" in entry for entry in log)
    assert not any("SU133" in entry for entry in log)

def test_get_handover_history(controller, other_controller):
    f1 = DummyFlight("SU134")
    controller.authorize_takeoff(f1)
    controller.handover_to(f1, other_controller)
    history = controller.get_handover_history()
    assert any("handed over" in entry for entry in history)
