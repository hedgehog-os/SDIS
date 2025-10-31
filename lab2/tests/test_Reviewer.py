from datetime import datetime

class DummyDraft:
    def __init__(self, draft_id, created_at=None):
        self.draft_id = draft_id
        self.created_at = created_at or datetime.now()
        self.reviewed_by = None
import pytest
from datetime import datetime, timedelta
from persons.Reviewer import Reviewer

@pytest.fixture
def reviewer():
    return Reviewer(
        reviewer_id=1,
        full_name="Error Reviewer",
        affiliation="LabX"
    )
def test_review_draft_adds_draft_and_comment(reviewer):
    draft = DummyDraft(draft_id=101)
    reviewer.review_draft(draft, comment="Хорошо структурирован")
    assert draft in reviewer.reviewed_drafts
    assert reviewer in draft.reviewed_by
    assert "Хорошо структурирован" in reviewer.comments
    assert reviewer.last_reviewed_at is not None

def test_review_draft_without_comment(reviewer):
    draft = DummyDraft(draft_id=102)
    reviewer.review_draft(draft)
    assert draft in reviewer.reviewed_drafts
    assert reviewer in draft.reviewed_by
    assert reviewer.comments == []

def test_remove_draft_removes_both_sides(reviewer):
    draft = DummyDraft(draft_id=103)
    reviewer.review_draft(draft, comment="Удалить позже")
    reviewer.remove_draft(draft)
    assert draft not in reviewer.reviewed_drafts
    assert reviewer not in draft.reviewed_by

def test_count_reviewed_drafts(reviewer):
    d1 = DummyDraft(draft_id=201)
    d2 = DummyDraft(draft_id=202)
    reviewer.review_draft(d1)
    reviewer.review_draft(d2)
    assert reviewer.count_reviewed_drafts() == 2

def test_get_recent_drafts_filters_by_date(reviewer):
    recent = DummyDraft(draft_id=301, created_at=datetime.now() - timedelta(days=5))
    old = DummyDraft(draft_id=302, created_at=datetime.now() - timedelta(days=60))
    reviewer.review_draft(recent)
    reviewer.review_draft(old)
    recent_drafts = reviewer.get_recent_drafts(days=30)
    assert recent in recent_drafts
    assert old not in recent_drafts

def test_get_comments_for_draft_present(reviewer):
    draft = DummyDraft(draft_id=401)
    reviewer.review_draft(draft, comment="Нужна доработка")
    comments = reviewer.get_comments_for_draft(draft)
    assert "Нужна доработка" in comments

def test_get_comments_for_draft_absent(reviewer):
    unrelated = DummyDraft(draft_id=402)
    comments = reviewer.get_comments_for_draft(unrelated)
    assert comments == []

def test_summarize_output(reviewer):
    draft = DummyDraft(draft_id=501)
    reviewer.review_draft(draft, comment="ОК")
    summary = reviewer.summarize()
    assert f"Рецензент #{reviewer.reviewer_id}" in summary
    assert "Аффилиация: LabX" in summary
    assert "Комментариев: 1" in summary

def test_to_dict_contains_all_fields(reviewer):
    draft = DummyDraft(draft_id=601)
    reviewer.review_draft(draft, comment="Проверено")
    data = reviewer.to_dict()
    assert data["reviewer_id"] == 1
    assert data["full_name"] == "Error Reviewer"
    assert data["affiliation"] == "LabX"
    assert data["reviewed_draft_ids"] == [601]
    assert "Проверено" in data["comments"]
    assert isinstance(data["last_reviewed_at"], str)
