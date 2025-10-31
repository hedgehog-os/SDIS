class DummyEditor:
    def __init__(self, editor_notes="Общие правки"):
        self.editor_notes = editor_notes

import pytest
from datetime import datetime
from documents.Revision import Revision

@pytest.fixture
def revision():
    return Revision(
        revision_id=1,
        document_id=101,
        version_number=2,
        editor_id=42,
        change_history=["Добавлен заголовок", "Исправлены опечатки"]
    )

def test_initial_state(revision):
    assert revision.version_number == 2
    assert revision.editor_id == 42
    assert len(revision.change_history) == 2
    assert revision.notes is None

def test_add_change(revision):
    revision.add_change("Добавлен вывод")
    assert "Добавлен вывод" in revision.change_history
    assert len(revision.change_history) == 3

def test_add_change_invalid(revision):
    revision.add_change("")
    revision.add_change(None)
    assert len(revision.change_history) == 2  # ничего не добавилось

def test_get_change_summary(revision):
    summary = revision.get_change_summary()
    assert "- Добавлен заголовок" in summary
    assert "- Исправлены опечатки" in summary

def test_get_change_summary_empty():
    r = Revision(2, 101, 1, 1, change_history=[])
    assert r.get_change_summary() == "Нет зафиксированных изменений."

def test_compare_to_previous():
    prev = Revision(1, 101, 1, 1, change_history=["A", "B"])
    curr = Revision(2, 101, 2, 1, previous_revision=prev, change_history=["A", "B", "C"])
    diff = curr.compare_to_previous()
    assert diff == ["C"]

def test_compare_to_previous_none():
    r = Revision(3, 101, 1, 1)
    assert r.compare_to_previous() == ["Нет предыдущей версии для сравнения."]

def test_is_major_revision_true():
    r = Revision(4, 101, 3, 1, change_history=["1", "2", "3", "4", "5"])
    assert r.is_major_revision() is True

def test_is_major_revision_false(revision):
    assert revision.is_major_revision() is False

def test_get_revision_info(revision):
    info = revision.get_revision_info()
    assert "Версия: 2" in info
    assert "Редактор ID: 42" in info
    assert "Изменений: 2" in info

def test_export_as_text(revision):
    text = revision.export_as_text()
    assert "Ревизия #1 — Версия 2" in text
    assert "- Добавлен заголовок" in text

def test_link_editor_notes(revision):
    editor = DummyEditor("Добавлены ссылки")
    revision.link_editor_notes(editor)
    assert revision.notes == "Добавлены ссылки"

def test_link_editor_notes_none(revision):
    revision.link_editor_notes(None)
    assert revision.notes is None

def test_visualize_diff_added_removed():
    prev = Revision(1, 101, 1, 1, change_history=["A", "B", "C"])
    curr = Revision(2, 101, 2, 1, previous_revision=prev, change_history=["B", "C", "D"])
    diff = curr.visualize_diff()
    assert "Добавлено:" in diff
    assert "  + D" in diff
    assert "Удалено:" in diff
    assert "  - A" in diff

def test_visualize_diff_no_changes():
    prev = Revision(1, 101, 1, 1, change_history=["X", "Y"])
    curr = Revision(2, 101, 2, 1, previous_revision=prev, change_history=["X", "Y"])
    diff = curr.visualize_diff()
    assert "Изменений нет." in diff

def test_visualize_diff_no_previous():
    r = Revision(3, 101, 1, 1)
    assert r.visualize_diff() == "Нет предыдущей версии для сравнения."
