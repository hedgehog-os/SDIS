from datetime import datetime, timedelta

class DummyReport:
    def __init__(self, report_id, created_at=None):
        self.report_id = report_id
        self.created_at = created_at or datetime.now()
        self.reviewed_by = None
import pytest
from persons.CommitteeMember import CommitteeMember

@pytest.fixture
def member():
    return CommitteeMember(
        member_id=1,
        full_name="Error Reviewer",
        role="reviewer"
    )
def test_valid_role_assignment():
    m = CommitteeMember(2, "Test Chair", role="chair")
    assert m.role == "chair"

def test_invalid_role_assignment():
    with pytest.raises(ValueError):
        CommitteeMember(3, "Invalid Role", role="manager")

def test_evaluate_report(member):
    report = DummyReport(report_id=101)
    member.evaluate_report(report, note="Хорошо структурирован")
    assert report in member.evaluated_reports
    assert member in report.reviewed_by
    assert "Хорошо структурирован" in member.evaluation_notes
    assert member.last_evaluation_date is not None

def test_evaluate_report_no_note(member):
    report = DummyReport(report_id=102)
    member.evaluate_report(report)
    assert report in member.evaluated_reports
    assert member.last_evaluation_date is not None

def test_remove_report(member):
    report = DummyReport(report_id=103)
    member.evaluate_report(report)
    member.remove_report(report)
    assert report not in member.evaluated_reports
    assert member not in report.reviewed_by

def test_count_evaluated_reports(member):
    r1 = DummyReport(report_id=201)
    r2 = DummyReport(report_id=202)
    member.evaluate_report(r1)
    member.evaluate_report(r2)
    assert member.count_evaluated_reports() == 2

def test_get_recent_reports(member):
    recent = DummyReport(report_id=301, created_at=datetime.now() - timedelta(days=5))
    old = DummyReport(report_id=302, created_at=datetime.now() - timedelta(days=60))
    member.evaluate_report(recent)
    member.evaluate_report(old)
    recent_reports = member.get_recent_reports(days=30)
    assert recent in recent_reports
    assert old not in recent_reports

def test_get_notes_for_report(member):
    report = DummyReport(report_id=401)
    member.evaluate_report(report, note="Подробный анализ")
    notes = member.get_notes_for_report(report)
    assert "Подробный анализ" in notes

def test_get_notes_for_unrelated_report(member):
    unrelated = DummyReport(report_id=402)
    notes = member.get_notes_for_report(unrelated)
    assert notes == []

def test_summarize(member):
    report = DummyReport(report_id=501)
    member.evaluate_report(report)
    summary = member.summarize()
    assert f"Комиссия #{member.member_id}" in summary
    assert "Оценено отчётов: 1" in summary

def test_to_dict(member):
    report = DummyReport(report_id=601)
    member.evaluate_report(report, note="Требует доработки")
    data = member.to_dict()
    assert data["member_id"] == 1
    assert data["full_name"] == "Error Reviewer"
    assert data["role"] == "reviewer"
    assert data["evaluated_report_ids"] == [601]
    assert "Требует доработки" in data["evaluation_notes"]
    assert isinstance(data["last_evaluation_date"], str)
