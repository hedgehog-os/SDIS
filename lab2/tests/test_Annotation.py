import pytest
from datetime import datetime, timedelta
from metadata_and_analitics.Annotation import Annotation

@pytest.fixture
def annotation():
    return Annotation(
        annotation_id=1,
        document_id=101,
        user_id=42,
        text="Это важная аннотация, содержащая ключевые данные.",
        timestamp=datetime.now() - timedelta(minutes=30)
    )
def test_initial_state(annotation):
    assert annotation.annotation_id == 1
    assert annotation.document_id == 101
    assert annotation.user_id == 42
    assert annotation.text.startswith("Это важная аннотация")
    assert isinstance(annotation.timestamp, datetime)

def test_edit_text(annotation):
    old_timestamp = annotation.timestamp
    annotation.edit_text("Обновлённый текст аннотации.")
    assert annotation.text == "Обновлённый текст аннотации."
    assert annotation.timestamp > old_timestamp

def test_edit_text_invalid(annotation):
    annotation.edit_text("")  # пустая строка не должна применяться
    assert annotation.text != ""

def test_contains_keyword_true(annotation):
    assert annotation.contains_keyword("ключевые") is True

def test_contains_keyword_false(annotation):
    assert annotation.contains_keyword("несуществующее") is False

def test_get_summary_short(annotation):
    short_text = "Краткая аннотация."
    a = Annotation(2, 102, 43, short_text)
    assert a.get_summary() == short_text

def test_get_summary_truncated(annotation):
    summary = annotation.get_summary(max_length=20)
    assert summary.endswith("...")

def test_is_recent_true(annotation):
    assert annotation.is_recent(threshold_minutes=60) is True

def test_is_recent_false():
    old = Annotation(3, 103, 44, "Старая аннотация", timestamp=datetime.now() - timedelta(hours=2))
    assert old.is_recent(threshold_minutes=60) is False

def test_format_for_display(annotation):
    output = annotation.format_for_display()
    assert f"Аннотация #1 (Документ 101)" in output
    assert "Пользователь: 42" in output
    assert "Текст: Это важная аннотация" in output
