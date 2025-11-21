import pytest
from models.infrastructure.ShuttleBus import ShuttleBus

def test_valid_initialization():
    bus = ShuttleBus("B1", "terminal loop", 20)
    assert bus.bus_id == "B1"
    assert bus.route_name == "terminal loop"
    assert bus.capacity == 20
    assert bus.passengers_onboard == 0
    assert bus.is_operational is True
    assert bus.maintenance_required is False
    assert bus.passenger_log == []

def test_invalid_route_name():
    with pytest.raises(ValueError, match="Invalid route name: unknown"):
        ShuttleBus("B2", "unknown", 10)

def test_invalid_capacity():
    with pytest.raises(ValueError, match="Bus capacity must be positive."):
        ShuttleBus("B3", "parking shuttle", 0)

@pytest.fixture
def bus():
    return ShuttleBus("B4", "hotel transfer", 3)

def test_board_passenger_success(bus):
    assert bus.board_passenger("P1") is True
    assert bus.passengers_onboard == 1
    assert "P1" in bus.passenger_log

def test_board_passenger_when_full(bus):
    bus.board_passenger("A")
    bus.board_passenger("B")
    bus.board_passenger("C")
    assert bus.board_passenger("D") is False

def test_board_passenger_when_shutdown(bus):
    bus.shutdown()
    assert bus.board_passenger("Ghost") is False

def test_board_passenger_when_under_maintenance(bus):
    bus.mark_for_maintenance()
    assert bus.board_passenger("Ghost") is False

def test_disembark_passenger_success(bus):
    bus.board_passenger("X")
    assert bus.disembark_passenger("X") is True
    assert "X" not in bus.passenger_log
    assert bus.passengers_onboard == 0

def test_disembark_passenger_not_found(bus):
    assert bus.disembark_passenger("Unknown") is False

def test_mark_and_clear_maintenance(bus):
    bus.mark_for_maintenance()
    assert bus.maintenance_required is True
    bus.clear_maintenance()
    assert bus.maintenance_required is False

def test_shutdown_and_restart(bus):
    bus.shutdown()
    assert bus.is_operational is False
    bus.restart()
    assert bus.is_operational is True

def test_is_available(bus):
    assert bus.is_available() is True
    bus.board_passenger("A")
    bus.board_passenger("B")
    bus.board_passenger("C")
    assert bus.is_available() is False
    bus.mark_for_maintenance()
    assert bus.is_available() is False
    bus.clear_maintenance()
    bus.shutdown()
    assert bus.is_available() is False

def test_occupancy_rate(bus):
    bus.board_passenger("A")
    bus.board_passenger("B")
    assert bus.occupancy_rate() == 0.67

def test_reset(bus):
    bus.board_passenger("X")
    bus.mark_for_maintenance()
    bus.shutdown()
    bus.reset()
    assert bus.passengers_onboard == 0
    assert bus.passenger_log == []
    assert bus.is_operational is True
    assert bus.maintenance_required is False

def test_get_passenger_list(bus):
    bus.board_passenger("P1")
    bus.board_passenger("P2")
    plist = bus.get_passenger_list()
    assert plist == ["P1", "P2"]
    assert plist is not bus.passenger_log  # ensure it's a copy

def test_summary_active(bus):
    bus.board_passenger("P1")
    assert bus.summary() == "Bus B4 on 'hotel transfer' route (1/3, active)"

def test_summary_offline(bus):
    bus.shutdown()
    assert bus.summary() == "Bus B4 on 'hotel transfer' route (0/3, offline)"
