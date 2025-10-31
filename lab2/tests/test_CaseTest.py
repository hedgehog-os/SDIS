from datetime import datetime

class DummyMeasurement:
    def __init__(self, value: float, unit: str, sensor=None, recent=True):
        self.value = value
        self.unit = unit
        self.sensor = sensor
        self._recent = recent

    def is_recent(self, threshold_minutes: int = 60) -> bool:
        return self._recent

    def is_from_sensor(self, sensor) -> bool:
        return self.sensor == sensor

class DummySensor:
    def __init__(self, sensor_id: int, name: str = "Датчик"):
        self.sensor_id = sensor_id
        self.name = name

class DummyProcedure:
    def __init__(self, procedure_id: int, name: str = "Процедура"):
        self.procedure_id = procedure_id
        self.name = name
import pytest
from experiments_and_equipments.CaseTest import CaseTest

@pytest.fixture
def testcase():
    return CaseTest(
        testcase_id=1,
        name="Температурный тест",
        description="Проверка стабильности при нагреве"
    )
def test_initial_state(testcase):
    assert testcase.testcase_id == 1
    assert testcase.name == "Температурный тест"
    assert testcase.description == "Проверка стабильности при нагреве"
    assert isinstance(testcase.created_at, datetime)
    assert testcase.procedure is None
    assert testcase.measurements is None

def test_add_measurement(testcase):
    m = DummyMeasurement(25.0, "°C")
    testcase.add_measurement(m)
    assert testcase.measurements == [m]

def test_add_multiple_measurements(testcase):
    m1 = DummyMeasurement(25.0, "°C")
    m2 = DummyMeasurement(101.0, "kPa")
    testcase.add_measurement(m1)
    testcase.add_measurement(m2)
    assert len(testcase.measurements) == 2

def test_remove_measurement(testcase):
    m = DummyMeasurement(50.0, "°C")
    testcase.add_measurement(m)
    testcase.remove_measurement(m)
    assert m not in testcase.measurements

def test_get_recent_measurements(testcase):
    recent = DummyMeasurement(1.0, "m/s", recent=True)
    old = DummyMeasurement(2.0, "m/s", recent=False)
    testcase.measurements = [recent, old]
    result = testcase.get_recent_measurements(minutes=60)
    assert result == [recent]

def test_get_measurements_by_unit(testcase):
    m1 = DummyMeasurement(1.0, "°C")
    m2 = DummyMeasurement(2.0, "kPa")
    testcase.measurements = [m1, m2]
    result = testcase.get_measurements_by_unit("°C")
    assert result == [m1]

def test_get_measurements_from_sensor(testcase):
    s1 = DummySensor(1)
    s2 = DummySensor(2)
    m1 = DummyMeasurement(1.0, "°C", sensor=s1)
    m2 = DummyMeasurement(2.0, "°C", sensor=s2)
    testcase.measurements = [m1, m2]
    result = testcase.get_measurements_from_sensor(s1)
    assert result == [m1]

def test_summarize_with_procedure(testcase):
    procedure = DummyProcedure(10, "Нагрев")
    testcase.procedure = procedure
    testcase.measurements = [DummyMeasurement(1.0, "°C")]
    summary = testcase.summarize()
    assert "Тест-кейс #1: Температурный тест" in summary
    assert "Процедура: Нагрев" in summary
    assert "Измерений: 1" in summary

def test_summarize_without_procedure(testcase):
    summary = testcase.summarize()
    assert "Процедура: —" in summary

def test_to_dict_with_procedure(testcase):
    procedure = DummyProcedure(20)
    testcase.procedure = procedure
    testcase.measurements = [DummyMeasurement(1.0, "°C")]
    data = testcase.to_dict()
    assert data["testcase_id"] == 1
    assert data["name"] == "Температурный тест"
    assert data["procedure_id"] == 20
    assert data["measurement_count"] == 1

def test_to_dict_without_measurements(testcase):
    data = testcase.to_dict()
    assert data["measurement_count"] == 0
