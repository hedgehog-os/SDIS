class DummyChart:
    def __init__(self, chart_type="bar"):
        self.chart_type = chart_type

class DummySummary:
    def __init__(self):
        self.report = None

class DummyCommitteeMember:
    def __init__(self, full_name="Иван Петров", role="эксперт"):
        self.full_name = full_name
        self.role = role
        self.evaluated_reports = []
        self.evaluation_notes = []
        self.last_evaluation_date = None

import pytest
from datetime import datetime
from documents.Report import Report
from Exceptions import ReportReviewerNotAssignedError, ReportChartNotFoundError

@pytest.fixture
def report():
    return Report(
        report_id=1,
        title="Годовой отчёт",
        author_id=42,
        charts=[DummyChart("bar"), DummyChart("line")],
        comments=[]
    )

def test_initial_state(report):
    assert report.title == "Годовой отчёт"
    assert report.author_id == 42
    assert len(report.charts) == 2
    assert report.summary is None
    assert report.reviewed_by is None

def test_add_chart(report):
    chart = DummyChart("pie")
    report.add_chart(chart)
    assert chart in report.charts
    assert len(report.charts) == 3

def test_remove_chart_success(report):
    chart = report.charts[0]
    report.remove_chart(chart)
    assert chart not in report.charts

def test_remove_chart_failure(report):
    chart = DummyChart("scatter")
    with pytest.raises(ReportChartNotFoundError):
        report.remove_chart(chart)

def test_assign_summary(report):
    summary = DummySummary()
    report.assign_summary(summary)
    assert report.summary == summary
    assert summary.report == report

def test_clear_summary(report):
    summary = DummySummary()
    report.assign_summary(summary)
    report.clear_summary()
    assert report.summary is None
    assert summary.report is None

def test_assign_committee_member(report):
    member = DummyCommitteeMember()
    report.assign_committee_member(member)
    assert member in report.reviewed_by
    assert report in member.evaluated_reports
    assert member.last_evaluation_date is not None

def test_assign_committee_member_no_duplicates(report):
    member = DummyCommitteeMember()
    report.assign_committee_member(member)
    report.assign_committee_member(member)
    assert report.reviewed_by.count(member) == 1

def test_remove_committee_member(report):
    member = DummyCommitteeMember()
    report.assign_committee_member(member)
    report.remove_committee_member(member)
    assert member not in report.reviewed_by
    assert report not in member.evaluated_reports

def test_add_evaluation_note_success(report):
    member = DummyCommitteeMember()
    report.assign_committee_member(member)
    report.add_evaluation_note(member, "Отличная структура")
    assert "Отличная структура" in member.evaluation_notes
    assert member.last_evaluation_date is not None

def test_add_evaluation_note_failure(report):
    member = DummyCommitteeMember()
    with pytest.raises(ReportReviewerNotAssignedError):
        report.add_evaluation_note(member, "Нет доступа")

def test_get_committee_roles(report):
    m1 = DummyCommitteeMember(role="эксперт")
    m2 = DummyCommitteeMember(role="председатель")
    report.assign_committee_member(m1)
    report.assign_committee_member(m2)
    roles = report.get_committee_roles()
    assert "эксперт" in roles
    assert "председатель" in roles

def test_is_reviewed_true(report):
    member = DummyCommitteeMember()
    report.assign_committee_member(member)
    assert report.is_reviewed() is True

def test_is_reviewed_false(report):
    assert report.is_reviewed() is False

def test_export_as_text(report):
    text = report.export_as_text()
    assert "Отчёт: Годовой отчёт" in text
    assert "Диаграмм: 2" in text
    assert "Резюме: отсутствует" in text

def test_count_charts_by_type(report):
    counts = report.count_charts_by_type()
    assert counts["bar"] == 1
    assert counts["line"] == 1

def test_get_reviewers_by_role(report):
    m1 = DummyCommitteeMember(full_name="Анна", role="эксперт")
    m2 = DummyCommitteeMember(full_name="Павел", role="председатель")
    report.assign_committee_member(m1)
    report.assign_committee_member(m2)
    names = report.get_reviewers_by_role("эксперт")
    assert names == ["Анна"]
