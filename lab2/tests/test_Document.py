import pytest
from datetime import datetime
from documents.Document import Document
from metadata_and_analitics.Comment import Comment
from Exceptions import DocumentNotReadyError, DocumentAlreadyArchivedError, DocumentRestoreError

# Заглушки
class DummyMetadata:
    def __init__(self):
        self.approved = False
        self.is_encrypted = False
        self.encryption_method = None

class DummyTemplate:
    def __init__(self, name="Шаблон A"):
        self.name = name

class DummyRevision:
    def get_revision_info(self):
        return "Ревизия 1"

class DummyAttachment:
    def get_file_extension(self):
        return "pdf"

class DummyKeyword:
    def __init__(self, word):
        self.word = word

class DummyForm:
    def __init__(self, form_id):
        self.form_id = form_id
        self.title = ""
        self.author_id = None

class DummyProtocol:
    def __init__(self, steps):
        self.steps = steps

class DummyReport:
    def __init__(self, author_id, title="Отчёт"):
        self.author_id = author_id
        self.title = title
        self.comments = []

# Фикстура документа
@pytest.fixture
def doc():
    return Document(
        document_id=1,
        title="Тестовый документ",
        author_id=42,
        metadata=DummyMetadata(),
        template=DummyTemplate(),
        revisions=[DummyRevision()],
        attachments=[DummyAttachment()],
        comments=[],
        keywords=[DummyKeyword("анализ")],
        tags=["проверка"]
    )

# Тесты
def test_initial_status(doc):
    assert doc.status == "draft"

def test_status_setter_valid(doc):
    doc.status = "final"
    assert doc.status == "final"

def test_status_setter_invalid(doc):
    with pytest.raises(ValueError):
        doc.status = "неверный"

def test_add_and_remove_tag(doc):
    doc.add_tag("новый")
    assert "новый" in doc.tags
    doc.remove_tag("новый")
    assert "новый" not in doc.tags

def test_add_and_remove_keyword(doc):
    kw = DummyKeyword("тест")
    doc.add_keyword(kw)
    assert kw in doc.keywords
    doc.remove_keyword(kw)
    assert kw not in doc.keywords

def test_revise_sets_status_draft(doc):
    doc.status = "final"
    doc.revise(DummyRevision())
    assert doc.status == "draft"
    assert len(doc.revisions) == 2

def test_submit_success(doc):
    doc.submit()
    assert doc.status == "final"

def test_submit_failure():
    d = Document(2, "Неполный", 1)
    with pytest.raises(DocumentNotReadyError):
        d.submit()

def test_archive_and_restore(doc):
    doc.archive()
    assert doc.status == "archived"
    doc.restore()
    assert doc.status == "final"

def test_archive_twice_raises(doc):
    doc.archive()
    with pytest.raises(DocumentAlreadyArchivedError):
        doc.archive()

def test_restore_invalid_raises(doc):
    doc.status = "draft"
    with pytest.raises(DocumentRestoreError):
        doc.restore()

def test_approve_sets_metadata(doc):
    doc.status = "final"
    doc.approve()
    assert doc.metadata.approved is True

def test_approve_invalid_status(doc):
    doc.status = "draft"
    with pytest.raises(ValueError):
        doc.approve()

def test_encrypt_and_decrypt(doc):
    doc.encrypt("RSA")
    assert doc.metadata.is_encrypted is True
    assert doc.metadata.encryption_method == "RSA"
    doc.decrypt()
    assert doc.metadata.is_encrypted is False

def test_is_ready_for_submission(doc):
    assert doc.is_ready_for_submission() is True

def test_export_as_text(doc):
    text = doc.export_as_text()
    assert "Документ: Тестовый документ" in text
    assert "Ключевые слова: анализ" in text

def test_get_attachment_formats(doc):
    formats = doc.get_attachment_formats()
    assert formats["pdf"] == 1

def test_find_comments_containing():
    doc = Document(
        document_id=2,
        title="Документ с комментариями",
        author_id=99,
        metadata=None,
        template=None,
        revisions=[],
        comments=[],
        keywords=[],
        tags=[]
    )
    comment = Comment(
        comment_id=1,
        document_id=2,
        author_id=99,
        user_id=2,
        content="Это важный комментарий",
        posted_at=datetime.now()
    )
    doc.comments.append(comment)
    results = doc.find_comments_containing("важный")
    assert len(results) == 1
    assert "важный" in results[0]


def test_summarize_revisions(doc):
    summary = doc.summarize_revisions()
    assert "Ревизия 1" in summary

def test_link_form(doc):
    form = DummyForm(form_id=1)
    doc.link_form(form)
    assert form.title == doc.title
    assert form.author_id == doc.author_id

def test_validate_against_protocol(doc):
    protocol = DummyProtocol(steps=["проверка оборудования"])
    assert doc.validate_against_protocol(protocol) is True

def test_generate_document_summary(doc):
    summary = doc.generate_document_summary()
    assert "Документ: Тестовый документ" in summary
    assert "Ключевые слова: анализ" in summary
