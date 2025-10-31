import pytest
from datetime import datetime
from persons.Editor import Editor  # или другой путь, если Editor лежит в другой папке

@pytest.fixture
def editor():
    return Editor(
        editor_id=1,
        fullname="Error Editor",
        email="error@example.com"
    )
def test_update_email_valid(editor):
    editor.update_email("new@example.com")
    assert editor.email == "new@example.com"

def test_update_email_invalid(editor):
    editor.update_email("invalid-email")
    assert editor.email != "invalid-email"

def test_append_note(editor):
    editor.append_note("Добавлена новая секция")
    assert "• Добавлена новая секция" in editor.editor_notes

def test_append_note_empty(editor):
    original_notes = editor.editor_notes
    editor.append_note("")
    assert editor.editor_notes == original_notes

def test_increment_revision(editor):
    original = editor.revision_number
    editor.increment_revision()
    assert editor.revision_number == original + 1

def test_record_change(editor):
    editor.record_change("Изменено форматирование")
    assert "Изменено форматирование" in editor.change_history
    assert editor.has_changes() is True

def test_has_changes_false(editor):
    assert editor.has_changes() is False

def test_get_change_log(editor):
    editor.record_change("Добавлен заголовок")
    editor.record_change("Удалён лишний абзац")
    log = editor.get_change_log()
    assert len(log) == 2
    assert all("[" in line and "]" in line for line in log)

def test_summarize(editor):
    editor.append_note("Проверка структуры")
    editor.record_change("Обновлены ссылки")
    summary = editor.summarize()
    assert f"Редактор #{editor.editor_id}" in summary
    assert "Заметки:" in summary
    assert "Изменений: 1" in summary

def test_to_dict(editor):
    editor.append_note("Проверка структуры")
    editor.record_change("Обновлены ссылки")
    data = editor.to_dict()
    assert data["editor_id"] == 1
    assert data["fullname"] == "Error Editor"
    assert data["email"] == "error@example.com"
    assert "• Проверка структуры" in data["editor_notes"]
    assert data["revision_number"] == 1
    assert isinstance(data["change_history"], list)
    assert len(data["change_history"]) == 1
