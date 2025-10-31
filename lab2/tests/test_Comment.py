import pytest
from datetime import datetime, timedelta
from metadata_and_analitics.Comment import Comment

@pytest.fixture
def comment():
    return Comment(
        comment_id=1,
        author_id=100,
        document_id=200,
        user_id=300,
        content="Это тестовый комментарий с ключевым словом.",
        posted_at=datetime.now() - timedelta(minutes=30)
    )
def test_initial_state(comment):
    assert comment.comment_id == 1
    assert comment.author_id == 100
    assert comment.document_id == 200
    assert comment.user_id == 300
    assert comment.content.startswith("Это тестовый комментарий")
    assert isinstance(comment.posted_at, datetime)

def test_edit_content(comment):
    old_time = comment.posted_at
    comment.edit_content("Обновлённый текст комментария.")
    assert comment.content == "Обновлённый текст комментария."
    assert comment.posted_at > old_time

def test_edit_content_invalid(comment):
    comment.edit_content("")  # не должно применяться
    assert comment.content != ""

def test_contains_keyword_true(comment):
    assert comment.contains_keyword("ключевым") is True

def test_contains_keyword_false(comment):
    assert comment.contains_keyword("несуществующее") is False

def test_is_recent_true(comment):
    assert comment.is_recent(threshold_minutes=60) is True

def test_is_recent_false():
    old_comment = Comment(
        comment_id=2,
        author_id=101,
        document_id=201,
        user_id=301,
        content="Старый комментарий",
        posted_at=datetime.now() - timedelta(hours=2)
    )
    assert old_comment.is_recent(threshold_minutes=60) is False

def test_format_for_display(comment):
    output = comment.format_for_display()
    assert "Комментарий #1 (Документ 200)" in output
    assert "Автор ID: 100, Пользователь ID: 300" in output
    assert "Текст: Это тестовый комментарий" in output

def test_get_summary_short(comment):
    short = comment.get_summary(max_length=100)
    assert short == comment.content

def test_get_summary_truncated(comment):
    truncated = comment.get_summary(max_length=10)
    assert truncated.startswith(comment.content[:10])
    assert truncated.endswith("...")
