import pytest
from datetime import datetime
from documents.Draft import Draft

@pytest.fixture
def draft():
    return Draft(
        draft_id=1,
        title="Тестовый черновик",
        author_id=42,
        content="Содержимое черновика"
    )

class DummyReviewer:
    def __init__(self, full_name="Иван Иванов", affiliation=None):
        self.full_name = full_name
        self.affiliation = affiliation
        self.comments = []
        self.reviewed_drafts = []
        self.last_reviewed_at = None

def test_initial_state(draft):
    assert draft.title == "Тестовый черновик"
    assert draft.author_id == 42
    assert draft.content == "Содержимое черновика"
    assert draft.reviewed_by is None

def test_assign_reviewer_initializes_list(draft):
    reviewer = DummyReviewer()
    draft.assign_reviewer(reviewer)
    assert reviewer in draft.reviewed_by
    assert draft in reviewer.reviewed_drafts
    assert reviewer.last_reviewed_at is not None

def test_assign_reviewer_does_not_duplicate(draft):
    reviewer = DummyReviewer()
    draft.assign_reviewer(reviewer)
    draft.assign_reviewer(reviewer)
    assert draft.reviewed_by.count(reviewer) == 1

def test_remove_reviewer(draft):
    reviewer = DummyReviewer()
    draft.assign_reviewer(reviewer)
    draft.remove_reviewer(reviewer)
    assert reviewer not in draft.reviewed_by
    assert draft not in reviewer.reviewed_drafts

def test_get_reviewer_names(draft):
    reviewer1 = DummyReviewer(full_name="Анна Смирнова")
    reviewer2 = DummyReviewer(full_name="Пётр Козлов")
    draft.assign_reviewer(reviewer1)
    draft.assign_reviewer(reviewer2)
    names = draft.get_reviewer_names()
    assert names == ["Анна Смирнова", "Пётр Козлов"]

def test_is_reviewed_true(draft):
    reviewer = DummyReviewer()
    draft.assign_reviewer(reviewer)
    assert draft.is_reviewed() is True

def test_is_reviewed_false(draft):
    assert draft.is_reviewed() is False

def test_add_reviewer_comment_success(draft):
    reviewer = DummyReviewer()
    draft.assign_reviewer(reviewer)
    draft.add_reviewer_comment(reviewer, "Комментарий")
    assert "Комментарий" in reviewer.comments
    assert reviewer.last_reviewed_at is not None

def test_export_as_text(draft):
    text = draft.export_as_text()
    assert "Черновик: Тестовый черновик" in text
    assert "Содержание:" in text
    assert "Содержимое черновика" in text

def test_get_all_comments_empty(draft):
    assert draft.get_all_comments() == []

def test_get_all_comments_with_reviewers(draft):
    reviewer1 = DummyReviewer()
    reviewer2 = DummyReviewer()
    draft.assign_reviewer(reviewer1)
    draft.assign_reviewer(reviewer2)
    reviewer1.comments.append("Комментарий 1")
    reviewer2.comments.append("Комментарий 2")
    all_comments = draft.get_all_comments()
    assert "Комментарий 1" in all_comments
    assert "Комментарий 2" in all_comments

def test_get_review_summary_empty(draft):
    assert draft.get_review_summary() == "Нет рецензентов."

def test_get_review_summary_filled(draft):
    reviewer1 = DummyReviewer(full_name="Анна", affiliation="НИИ")
    reviewer2 = DummyReviewer(full_name="Пётр")
    draft.assign_reviewer(reviewer1)
    draft.assign_reviewer(reviewer2)
    reviewer1.comments.extend(["1", "2"])
    reviewer2.comments.append("3")
    summary = draft.get_review_summary()
    assert "Анна (НИИ) — 2 комментариев" in summary
    assert "Пётр (без указания) — 1 комментариев" in summary
