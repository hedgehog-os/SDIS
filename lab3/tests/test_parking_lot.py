import pytest
from models.infrastructure.parking_lot import ParkingLot

def test_valid_initialization():
    lot = ParkingLot("LotA", 5)
    assert lot.lot_id == "LotA"
    assert lot.capacity == 5
    assert lot.occupied == 0
    assert lot.is_open is True
    assert lot.maintenance_required is False
    assert lot.vehicle_log == []

def test_invalid_capacity():
    with pytest.raises(ValueError, match="Parking lot capacity must be positive."):
        ParkingLot("LotB", 0)

@pytest.fixture
def lot():
    return ParkingLot("LotC", 3)

def test_park_vehicle_success(lot):
    assert lot.park_vehicle("CAR123") is True
    assert lot.occupied == 1
    assert "CAR123" in lot.vehicle_log

def test_park_vehicle_when_full(lot):
    lot.park_vehicle("A")
    lot.park_vehicle("B")
    lot.park_vehicle("C")
    assert lot.park_vehicle("D") is False

def test_park_vehicle_when_closed(lot):
    lot.close()
    assert lot.park_vehicle("CAR999") is False

def test_park_vehicle_when_under_maintenance(lot):
    lot.mark_for_maintenance()
    assert lot.park_vehicle("CAR888") is False

def test_release_vehicle_success(lot):
    lot.park_vehicle("CAR321")
    assert lot.release_vehicle("CAR321") is True
    assert "CAR321" not in lot.vehicle_log
    assert lot.occupied == 0

def test_release_vehicle_not_found(lot):
    assert lot.release_vehicle("UNKNOWN") is False

def test_mark_and_clear_maintenance(lot):
    lot.mark_for_maintenance()
    assert lot.maintenance_required is True
    lot.clear_maintenance()
    assert lot.maintenance_required is False

def test_close_and_open(lot):
    lot.close()
    assert lot.is_open is False
    lot.open()
    assert lot.is_open is True

def test_is_available_true(lot):
    assert lot.is_available() is True

def test_is_available_false_due_to_full(lot):
    lot.park_vehicle("A")
    lot.park_vehicle("B")
    lot.park_vehicle("C")
    assert lot.is_available() is False

def test_is_available_false_due_to_maintenance(lot):
    lot.mark_for_maintenance()
    assert lot.is_available() is False

def test_is_available_false_due_to_closed(lot):
    lot.close()
    assert lot.is_available() is False

def test_occupancy_rate(lot):
    lot.park_vehicle("A")
    lot.park_vehicle("B")
    assert lot.occupancy_rate() == 0.67

def test_reset(lot):
    lot.park_vehicle("X")
    lot.mark_for_maintenance()
    lot.close()
    lot.reset()
    assert lot.occupied == 0
    assert lot.vehicle_log == []
    assert lot.maintenance_required is False
    assert lot.is_open is True

def test_get_vehicle_list(lot):
    lot.park_vehicle("CAR1")
    lot.park_vehicle("CAR2")
    vehicles = lot.get_vehicle_list()
    assert vehicles == ["CAR1", "CAR2"]
    assert vehicles is not lot.vehicle_log  # ensure copy

def test_is_vehicle_present(lot):
    lot.park_vehicle("CARX")
    assert lot.is_vehicle_present("CARX") is True
    assert lot.is_vehicle_present("GHOST") is False
