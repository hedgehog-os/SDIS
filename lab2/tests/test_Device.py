from datetime import datetime, timedelta
from typing import Optional

class DummyCalibration:
    def __init__(self, calibration_id: int, date: Optional[datetime] = None):
        self.calibration_id = calibration_id
        self.date = date or datetime.now()
import pytest
from experiments_and_equipments.Device import Device

@pytest.fixture
def device():
    return Device(device_id=1, name="Термометр")

def test_initial_state(device):
    assert device.device_id == 1
    assert device.name == "Термометр"
    assert device.calibration is None

def test_assign_calibration(device):
    calibration = DummyCalibration(101)
    device.assign_calibration(calibration)
    assert device.calibration == calibration

def test_clear_calibration(device):
    calibration = DummyCalibration(102)
    device.assign_calibration(calibration)
    device.clear_calibration()
    assert device.calibration is None

def test_is_calibrated_true(device):
    device.assign_calibration(DummyCalibration(103))
    assert device.is_calibrated() is True

def test_is_calibrated_false(device):
    assert device.is_calibrated() is False

def test_was_calibrated_recently_true(device):
    recent = DummyCalibration(104, date=datetime.now())
    device.assign_calibration(recent)
    assert device.was_calibrated_recently(days=30) is True

def test_was_calibrated_recently_false(device):
    old = DummyCalibration(105, date=datetime.now() - timedelta(days=60))
    device.assign_calibration(old)
    assert device.was_calibrated_recently(days=30) is False

def test_get_calibration_summary_present(device):
    calibration = DummyCalibration(106, date=datetime(2023, 1, 1))
    device.assign_calibration(calibration)
    summary = device.get_calibration_summary()
    assert "Калибровка #106 от 2023-01-01" in summary

def test_get_calibration_summary_absent(device):
    assert device.get_calibration_summary() == "Нет данных о калибровке."

def test_to_dict_with_calibration(device):
    calibration = DummyCalibration(107)
    device.assign_calibration(calibration)
    data = device.to_dict()
    assert data["device_id"] == 1
    assert data["name"] == "Термометр"
    assert data["calibration_id"] == 107

def test_to_dict_without_calibration(device):
    data = device.to_dict()
    assert data["calibration_id"] is None

def test_format_for_display_with_calibration(device):
    calibration = DummyCalibration(108, date=datetime(2024, 5, 15))
    device.assign_calibration(calibration)
    text = device.format_for_display()
    assert "Устройство #1: Термометр" in text
    assert "Калибровка #108 от 2024-05-15" in text

def test_format_for_display_without_calibration(device):
    text = device.format_for_display()
    assert "Нет данных о калибровке." in text
