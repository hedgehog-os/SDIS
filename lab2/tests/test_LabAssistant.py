from datetime import datetime

class DummyDevice:
    def __init__(self, name):
        self.name = name

class DummyLabRoom:
    def __init__(self, room_number, equipment=None):
        self.room_number = room_number
        self.equipment = equipment or []

class DummyProcedure:
    def __init__(self, name):
        self.name = name

class DummyExperiment:
    def __init__(self, experiment_id, procedure, start_date):
        self.experiment_id = experiment_id
        self.procedure = procedure
        self.start_date = start_date
import pytest
from persons.LabAssistant import LabAssistant

@pytest.fixture
def assistant():
    return LabAssistant(
        assistant_id=1,
        fullname="Error Helper",
        email="error@lab.com",
        position="Technician",
        lab_room=101,
        equipment_list=["centrifuge", "microscope", "thermometer"]
    )
def test_add_equipment_new(assistant):
    assistant.add_equipment("pipette")
    assert "pipette" in assistant.equipment_list

def test_add_equipment_existing(assistant):
    assistant.add_equipment("microscope")
    assert assistant.equipment_list.count("microscope") == 1

def test_remove_equipment_existing(assistant):
    assistant.remove_equipment("thermometer")
    assert "thermometer" not in assistant.equipment_list

def test_remove_equipment_missing(assistant):
    assistant.remove_equipment("scanner")  # не должно вызвать ошибку
    assert "scanner" not in assistant.equipment_list

def test_has_equipment_true(assistant):
    assert assistant.has_equipment("centrifuge") is True

def test_has_equipment_false(assistant):
    assert assistant.has_equipment("scanner") is False

def test_count_equipment(assistant):
    assert assistant.count_equipment() == 3

def test_get_equipment_by_prefix_match(assistant):
    result = assistant.get_equipment_by_prefix("micro")
    assert result == ["microscope"]

def test_get_equipment_by_prefix_none(assistant):
    result = assistant.get_equipment_by_prefix("xray")
    assert result == []

def test_summarize(assistant):
    summary = assistant.summarize()
    assert "Ассистент #1" in summary
    assert "Оборудование: 3 единиц" in summary

def test_to_dict(assistant):
    data = assistant.to_dict()
    assert data["assistant_id"] == 1
    assert data["fullname"] == "Error Helper"
    assert data["lab_room"] == 101
    assert "microscope" in data["equipment_list"]

def test_is_assigned_to_room_true(assistant):
    room = DummyLabRoom(room_number=101)
    assert assistant.is_assigned_to_room(room) is True

def test_is_assigned_to_room_false(assistant):
    room = DummyLabRoom(room_number=202)
    assert assistant.is_assigned_to_room(room) is False

def test_get_room_equipment_overlap(assistant):
    room = DummyLabRoom(room_number=101, equipment=[DummyDevice("microscope"), DummyDevice("scanner")])
    overlap = assistant.get_room_equipment_overlap(room)
    assert overlap == ["microscope"]

def test_get_assigned_devices(assistant):
    devices = [DummyDevice("microscope"), DummyDevice("scanner"), DummyDevice("centrifuge")]
    assigned = assistant.get_assigned_devices(devices)
    assert len(assigned) == 2
    assert all(d.name in ["microscope", "centrifuge"] for d in assigned)

def test_assist_in_experiment(assistant):
    procedure = DummyProcedure(name="DNA Extraction")
    experiment = DummyExperiment(experiment_id=42, procedure=procedure, start_date=datetime(2025, 10, 1))
    result = assistant.assist_in_experiment(experiment)
    assert "Error Helper (Technician)" in result
    assert "эксперименте #42" in result
    assert "DNA Extraction" in result
    assert "2025-10-01" in result
