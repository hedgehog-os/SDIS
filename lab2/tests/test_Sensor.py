class DummyDevice:
    def __init__(self, device_id: int, name: str):
        self.device_id = device_id
        self.name = name
        self.sensors = []
import pytest
from experiments_and_equipments.Sensor import Sensor

@pytest.fixture
def device():
    return DummyDevice(device_id=1, name="Термометр")

@pytest.fixture
def sensor(device):
    return Sensor(sensor_id=101, type="Температурный", device=device)
def test_initial_state(sensor, device):
    assert sensor.sensor_id == 101
    assert sensor.type == "Температурный"
    assert sensor.device == device

def test_is_attached_to_true(sensor, device):
    assert sensor.is_attached_to(device) is True

def test_is_attached_to_false():
    d1 = DummyDevice(1, "Термометр")
    d2 = DummyDevice(2, "Барометр")
    s = Sensor(sensor_id=102, type="Давление", device=d1)
    assert s.is_attached_to(d2) is False

def test_get_device_name(sensor):
    assert sensor.get_device_name() == "Термометр"

def test_describe(sensor):
    desc = sensor.describe()
    assert "Сенсор #101" in desc
    assert "Тип: Температурный" in desc
    assert "Устройство: Термометр" in desc

def test_to_dict(sensor):
    data = sensor.to_dict()
    assert data["sensor_id"] == 101
    assert data["type"] == "Температурный"
    assert data["device_id"] == 1
    assert data["device_name"] == "Термометр"

def test_annotate_device(sensor, device):
    sensor.annotate_device()
    assert sensor in device.sensors

def test_annotate_device_no_duplicate(sensor, device):
    sensor.annotate_device()
    sensor.annotate_device()
    assert device.sensors.count(sensor) == 1

def test_annotate_device_missing_sensors():
    class DeviceWithoutSensors:
        def __init__(self):
            self.device_id = 3
            self.name = "Без списка"
    d = DeviceWithoutSensors()
    s = Sensor(sensor_id=104, type="Тип", device=d)
    s.annotate_device()
