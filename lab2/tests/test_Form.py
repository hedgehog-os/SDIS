class DummyCheckList:
    def __init__(self, is_complete=False):
        self.is_complete = is_complete
        self.form = None

import pytest
from datetime import datetime
from documents.Form import Form

@pytest.fixture
def form():
    return Form(
        form_id=1,
        title="Форма регистрации",
        author_id=42,
        fields=["Имя", "Фамилия", "Email"]
    )

def test_initial_state(form):
    assert form.title == "Форма регистрации"
    assert form.author_id == 42
    assert form.fields == ["Имя", "Фамилия", "Email"]
    assert form.checklist is None

def test_validate_fields_success(form):
    assert form.validate_fields() is True

def test_validate_fields_failure():
    f = Form(2, "Пустая форма", 99, fields=["Имя", "", " "])
    assert f.validate_fields() is False

def test_assign_to_user(form):
    form.assign_to_user(77)
    assert form.author_id == 77

def test_link_checklist(form):
    checklist = DummyCheckList()
    form.link_checklist(checklist)
    assert form.checklist == checklist
    assert checklist.form == form

def test_unlink_checklist(form):
    checklist = DummyCheckList()
    form.link_checklist(checklist)
    form.unlink_checklist()
    assert form.checklist is None
    assert checklist.form is None

def test_get_checklist_status_unlinked(form):
    assert form.get_checklist_status() == "Чек-лист не привязан."

def test_get_checklist_status_incomplete(form):
    checklist = DummyCheckList(is_complete=False)
    form.link_checklist(checklist)
    assert form.get_checklist_status() == "В процессе"

def test_get_checklist_status_complete(form):
    checklist = DummyCheckList(is_complete=True)
    form.link_checklist(checklist)
    assert form.get_checklist_status() == "Завершён"

def test_submit_form_success(form, capsys):
    checklist = DummyCheckList(is_complete=True)
    form.link_checklist(checklist)
    form.submit_form()
    output = capsys.readouterr().out
    assert "успешно отправлена" in output

def test_submit_form_no_fields():
    f = Form(3, "Без полей", 1, fields=[])
    with pytest.raises(ValueError, match="Форма не может быть отправлена без полей."):
        f.submit_form()

def test_submit_form_incomplete_checklist(form):
    checklist = DummyCheckList(is_complete=False)
    form.link_checklist(checklist)
    with pytest.raises(ValueError, match="чек-лист не завершён"):
        form.submit_form()
