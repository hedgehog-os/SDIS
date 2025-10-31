class DummyAttachment:
    def __init__(self):
        self.document = None

class DummyRevision:
    def __init__(self, version_number, notes=None):
        self.version_number = version_number
        self.notes = notes

class DummyComment:
    def __init__(self, content):
        self.content = content

class DummyKeyword:
    def __init__(self, word):
        self.word = word

import pytest
from documents.Template import Template

@pytest.fixture
def template():
    return Template(
        template_id=1,
        name="Шаблон отчёта",
        content_structure="section -> paragraph"
    )

def test_initial_state(template):
    assert template.name == "Шаблон отчёта"
    assert template.content_structure == "section -> paragraph"
    assert template.attachments == []
    assert template.revisions == []
    assert template.comments == []
    assert template.keywords == []

def test_format_setter_valid(template):
    template._format = None  # инициализация приватного поля
    template.format = "md"
    assert template.format == "md"

def test_format_setter_invalid(template):
    template._format = None
    with pytest.raises(ValueError):
        template.format = "pdf"

def test_assign_template_adds_self(template):
    other = Template(2, "Родительский шаблон", "structure")
    template.assign_template(other)
    assert template in other.applicable_documents
    assert template.template == other

def test_remove_template_removes_self(template):
    parent = Template(3, "Родитель", "structure", applicable_documents=[template])
    template.template = parent
    template.remove_template()
    assert template not in parent.applicable_documents
    assert template.template is None

def test_add_attachment(template):
    attachment = DummyAttachment()
    template.add_attachment(attachment)
    assert attachment in template.attachments
    assert attachment.document == template

def test_remove_attachment(template):
    attachment = DummyAttachment()
    template.add_attachment(attachment)
    template.remove_attachment(attachment)
    assert attachment not in template.attachments
    assert attachment.document is None

def test_get_latest_revision(template):
    r1 = DummyRevision(1)
    r2 = DummyRevision(3)
    r3 = DummyRevision(2)
    template.revisions = [r1, r2, r3]
    latest = template.get_latest_revision()
    assert latest.version_number == 3

def test_get_latest_revision_none(template):
    assert template.get_latest_revision() is None

def test_get_revision_history(template):
    template.revisions = [
        DummyRevision(1, "Первый черновик"),
        DummyRevision(2, None),
        DummyRevision(3, "Финальная версия")
    ]
    history = template.get_revision_history()
    assert history == [
        "v1: Первый черновик",
        "v2: —",
        "v3: Финальная версия"
    ]

def test_get_comment_summary_empty(template):
    assert template.get_comment_summary() == "Комментариев нет."

def test_get_comment_summary_filled(template):
    template.comments = [
        DummyComment("Хороший шаблон"),
        DummyComment("Нужно добавить раздел")
    ]
    summary = template.get_comment_summary()
    assert "- Хороший шаблон" in summary
    assert "- Нужно добавить раздел" in summary

def test_get_keywords_as_text_empty(template):
    assert template.get_keywords_as_text() == "Нет ключевых слов."

def test_get_keywords_as_text_filled(template):
    template.keywords = [DummyKeyword("отчёт"), DummyKeyword("анализ")]
    text = template.get_keywords_as_text()
    assert text == "отчёт, анализ"
