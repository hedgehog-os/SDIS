class DummySensor:
    def __init__(self, sensor_id: int, name: str = "Температурный датчик"):
        self.sensor_id = sensor_id
        self.name = name
import pytest
from datetime import datetime, timedelta
from experiments_and_equipments.Measurement import Measurement

@pytest.fixture
def sensor():
    return DummySensor(sensor_id=42, name="Датчик давления")

@pytest.fixture
def measurement(sensor):
    return Measurement(
        value=23.5,
        unit="°C",
        timestamp=datetime.now() - timedelta(minutes=30),
        sensor=sensor
    )
def test_initial_state(measurement, sensor):
    assert measurement.value == 23.5
    assert measurement.unit == "°C"
    assert isinstance(measurement.timestamp, datetime)
    assert measurement.sensor == sensor

def test_is_recent_true(measurement):
    assert measurement.is_recent(threshold_minutes=60) is True

def test_is_recent_false():
    old_timestamp = datetime.now() - timedelta(hours=2)
    m = Measurement(value=10.0, unit="m/s", timestamp=old_timestamp)
    assert m.is_recent(threshold_minutes=60) is False

def test_format_for_display_with_sensor(measurement):
    output = measurement.format_for_display()
    assert "Измерение: 23.50 °C" in output
    assert "Сенсор: Датчик давления" in output

def test_format_for_display_without_sensor():
    m = Measurement(value=5.0, unit="kg")
    output = m.format_for_display()
    assert "Сенсор: —" in output

def test_to_dict_with_sensor(measurement):
    data = measurement.to_dict()
    assert data["value"] == 23.5
    assert data["unit"] == "°C"
    assert isinstance(data["timestamp"], str)
    assert data["sensor_id"] == 42

def test_to_dict_without_sensor():
    m = Measurement(value=1.0, unit="Pa")
    data = m.to_dict()
    assert data["sensor_id"] is None

def test_is_from_sensor_true(measurement, sensor):
    assert measurement.is_from_sensor(sensor) is True

def test_is_from_sensor_false():
    s1 = DummySensor(1)
    s2 = DummySensor(2)
    m = Measurement(value=0.1, unit="V", sensor=s1)
    assert m.is_from_sensor(s2) is False
