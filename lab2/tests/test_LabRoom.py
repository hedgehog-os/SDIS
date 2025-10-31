from datetime import datetime, timedelta
from typing import Optional

class DummyDevice:
    def __init__(self, device_id: int, calibrated: bool = True, calibration_date: Optional[datetime] = None):
        self.device_id = device_id
        self._calibrated = calibrated
        self._calibration_date = calibration_date or datetime.now()

    def is_calibrated(self) -> bool:
        return self._calibrated

    def was_calibrated_recently(self, days: int = 30) -> bool:
        return self._calibration_date >= datetime.now() - timedelta(days=days)
import pytest
from experiments_and_equipments.LabRoom import LabRoom

@pytest.fixture
def lab():
    return LabRoom(room_number="A101")

def test_initial_state(lab):
    assert lab.room_number == "A101"
    assert lab.equipment == []

def test_add_device(lab):
    d = DummyDevice(1)
    lab.add_device(d)
    assert d in lab.equipment

def test_add_device_no_duplicate(lab):
    d = DummyDevice(2)
    lab.add_device(d)
    lab.add_device(d)
    assert lab.equipment.count(d) == 1

def test_remove_device(lab):
    d = DummyDevice(3)
    lab.add_device(d)
    lab.remove_device(d)
    assert d not in lab.equipment

def test_has_device_true(lab):
    d = DummyDevice(4)
    lab.add_device(d)
    assert lab.has_device(d) is True

def test_has_device_false(lab):
    d = DummyDevice(5)
    assert lab.has_device(d) is False

def test_get_device_ids(lab):
    d1 = DummyDevice(10)
    d2 = DummyDevice(20)
    lab.equipment = [d1, d2]
    assert lab.get_device_ids() == [10, 20]

def test_get_uncalibrated_devices(lab):
    d1 = DummyDevice(11, calibrated=False)
    d2 = DummyDevice(12, calibrated=True)
    lab.equipment = [d1, d2]
    result = lab.get_uncalibrated_devices()
    assert result == [d1]

def test_get_recently_calibrated_devices(lab):
    from datetime import datetime, timedelta
    recent = DummyDevice(13, calibration_date=datetime.now())
    old = DummyDevice(14, calibration_date=datetime.now() - timedelta(days=60))
    lab.equipment = [recent, old]
    result = lab.get_recently_calibrated_devices(days=30)
    assert recent in result
    assert old not in result



def test_to_dict(lab):
    d1 = DummyDevice(17)
    d2 = DummyDevice(18)
    lab.equipment = [d1, d2]
    data = lab.to_dict()
    assert data["room_number"] == "A101"
    assert data["device_ids"] == [17, 18]
