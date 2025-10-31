import pytest
from documents.CheckList import CheckList

class DummyForm:
    def __init__(self):
        self.fields = []
        self.checklist = None

@pytest.fixture
def checklist():
    return CheckList(
        checklist_id=1,
        title="Проверка оборудования",
        items=["Проверить питание", "Проверить кабели", "Проверить датчики"],
        checklist_items=[],
        is_complete=False
    )

def test_initial_state(checklist):
    assert checklist.title == "Проверка оборудования"
    assert checklist.is_complete is False
    assert len(checklist.items) == 3
    assert checklist.checklist_items == []

def test_mark_item_complete(checklist):
    checklist.mark_item_complete("Проверить питание")
    assert "Проверить питание" in checklist.checklist_items
    assert checklist.is_complete is False

def test_mark_all_items_complete(checklist):
    for item in checklist.items:
        checklist.mark_item_complete(item)
    assert checklist.is_complete is True

def test_mark_invalid_item_raises(checklist):
    with pytest.raises(ValueError):
        checklist.mark_item_complete("Несуществующий пункт")

def test_reset_checklist(checklist):
    checklist.mark_item_complete("Проверить питание")
    checklist.reset_checklist()
    assert checklist.checklist_items == []
    assert checklist.is_complete is False

def test_sort_checklist_default(checklist):
    checklist.sort_checklist()
    assert checklist.items == sorted(checklist.items)

def test_sort_checklist_reverse(checklist):
    checklist.sort_checklist(reverse=True)
    assert checklist.items == sorted(checklist.items, reverse=True)

def test_link_to_form(checklist):
    form = DummyForm()
    checklist.link_to_form(form)
    assert checklist.form == form
    assert form.checklist == checklist

def test_unlink_form(checklist):
    form = DummyForm()
    checklist.link_to_form(form)
    checklist.unlink_form()
    assert checklist.form is None
    assert form.checklist is None

def test_export_as_text(checklist):
    checklist.mark_item_complete("Проверить питание")
    text = checklist.export_as_text()
    assert "Чек-лист: Проверка оборудования" in text
    assert "completed Проверить питание" in text
    assert "not fulfilled Проверить кабели" in text

def test_preview_output(capsys, checklist):
    checklist.mark_item_complete("Проверить питание")
    checklist.preview()
    captured = capsys.readouterr()
    assert "Чек-лист: Проверка оборудования" in captured.out

def test_is_form_ready_true(checklist):
    form = DummyForm()
    form.fields = ["Поле 1"]
    checklist.link_to_form(form)
    assert checklist.is_form_ready() is True

def test_is_form_ready_false(checklist):
    form = DummyForm()
    checklist.link_to_form(form)
    assert checklist.is_form_ready() is False

def test_is_form_ready_none(checklist):
    checklist.form = None
    assert checklist.is_form_ready() is False
