from datetime import datetime


class DummyDevice:
    def __init__(self):
        self.calibrations = []

class DummyRevision:
    def __init__(self, revision_id, document_id, author_id, timestamp, notes, change_history):
        self.revision_id = revision_id
        self.document_id = document_id
        self.author_id = author_id
        self.timestamp = timestamp
        self.notes = notes
        self.change_history = change_history



class DummyDocument:
    def __init__(self, document_id):
        self.document_id = document_id
        self.revisions = []

class DummyComment:
    def __init__(self, comment_id, document_id, author_id, content, posted_at):
        self.comment_id = comment_id
        self.document_id = document_id
        self.author_id = author_id
        self.content = content
        self.posted_at = posted_at



class DummyReport:
    def __init__(self, report_id, author_id):
        self.report_id = report_id
        self.author_id = author_id
        self.comments = []

import pytest
from datetime import datetime, timedelta
from experiments_and_equipments.Calibration import Calibration

@pytest.fixture
def calibration():
    return Calibration(
        calibration_id=1,
        date=datetime.now() - timedelta(days=10),
        technician="Иванов И.И.",
        notes="Проверка датчиков"
    )
def test_update_notes(calibration):
    calibration.update_notes("Обновлённые заметки")
    assert calibration.notes == "Обновлённые заметки"

def test_update_notes_invalid(calibration):
    calibration.update_notes("")
    assert calibration.notes == "Проверка датчиков"

def test_reschedule_future(calibration):
    future_date = datetime.now() + timedelta(days=5)
    calibration.reschedule(future_date)
    assert calibration.date == future_date

def test_reschedule_past(calibration):
    past_date = datetime.now() - timedelta(days=5)
    calibration.reschedule(past_date)
    assert calibration.date != past_date  # дата не изменилась

def test_is_recent_true(calibration):
    assert calibration.is_recent() is True

def test_is_recent_false():
    old = Calibration(2, datetime.now() - timedelta(days=60), "Техник", "Старые данные")
    assert old.is_recent() is False

def test_format_for_display(calibration):
    text = calibration.format_for_display()
    assert f"Калибровка #{calibration.calibration_id}" in text
    assert "Техник: Иванов И.И." in text

def test_to_dict(calibration):
    data = calibration.to_dict()
    assert data["calibration_id"] == 1
    assert data["technician"] == "Иванов И.И."
    assert "date" in data and "notes" in data

def test_is_assigned_to_true(calibration):
    assert calibration.is_assigned_to("иванов и.и.") is True

def test_is_assigned_to_false(calibration):
    assert calibration.is_assigned_to("Петров П.П.") is False

def test_link_to_device(calibration):
    device = DummyDevice()
    calibration.link_to_device(device)
    assert calibration in device.calibrations

def test_is_for_device_true(calibration):
    device = DummyDevice()
    calibration.link_to_device(device)
    assert calibration.is_for_device(device) is True

def test_is_for_device_false(calibration):
    device = DummyDevice()
    assert calibration.is_for_device(device) is False

import sys

def test_attach_to_document(calibration):
    def mock_revision(revision_id, document_id, author_id, timestamp, notes, change_history):
        return DummyRevision(revision_id, document_id, author_id, timestamp, notes, change_history)

    sys.modules["documents.Revision"] = type("mock_module", (), {"Revision": mock_revision})

    doc = DummyDocument(document_id=5)
    calibration.attach_to_document(doc)
    assert len(doc.revisions) == 1
    assert "Калибровка #1" in doc.revisions[0].notes
    assert doc.revisions[0].author_id == 0

def test_contribute_to_report(calibration):
    def mock_comment(comment_id, document_id, user_id, content, posted_at):
        return DummyComment(comment_id, document_id, user_id, content, posted_at)

    sys.modules["metadata_and_analitics.Comment"] = type("mock_module", (), {"Comment": mock_comment})

    report = DummyReport(report_id=7, author_id=99)
    calibration.contribute_to_report(report)
    assert len(report.comments) == 1
    comment = report.comments[0]
    assert "Калибровка #1 выполнена" in comment.content
    assert comment.author_id == 99


