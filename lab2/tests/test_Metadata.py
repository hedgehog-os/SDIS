class DummyKeyword:
    def __init__(self, word, relevance_score):
        self.word = word
        self.relevance_score = relevance_score

class DummyDocument:
    def __init__(self, document_id, tags=None, keywords=None):
        self.document_id = document_id
        self.tags = tags or []
        self.keywords = keywords
        self.metadata = None
import pytest
from metadata_and_analitics.Keyword import Keyword
from datetime import datetime, timedelta
from metadata_and_analitics.Metadata import Metadata
from Exceptions import (
    MetadataTagConflictError,
    MetadataKeywordNotFoundError,
    MetadataEncryptionError,
    MetadataDecryptionError
)

@pytest.fixture
def metadata():
    return Metadata(
        document_id=1,
        author="Error",
        created_at=datetime.now() - timedelta(days=1),
        tags=["важное", "эксперимент"],
        keywords=["температура", "давление"]
    )
def test_add_tag_success(metadata):
    metadata.add_tag("новое")
    assert "новое" in metadata.tags

def test_add_tag_conflict(metadata):
    with pytest.raises(MetadataTagConflictError):
        metadata.add_tag("важное")

def test_remove_tag_existing(metadata):
    metadata.remove_tag("эксперимент")
    assert "эксперимент" not in metadata.tags

def test_remove_tag_nonexistent(metadata):
    metadata.remove_tag("несуществующий")  # не должно вызывать ошибку
    assert "несуществующий" not in metadata.tags

def test_remove_keyword_existing(metadata):
    metadata.remove_keyword("давление")
    assert "давление" not in metadata.keywords

def test_approve_and_reject(metadata):
    metadata.approve()
    assert metadata.approved is True
    metadata.reject()
    assert metadata.approved is False

def test_encrypt_success(metadata):
    metadata.encrypt("RSA")
    assert metadata.is_encrypted is True
    assert metadata.encryption_method == "RSA"

def test_encrypt_missing_method(metadata):
    with pytest.raises(MetadataEncryptionError):
        metadata.encrypt("")

def test_decrypt_success(metadata):
    metadata.encrypt("AES")
    metadata.decrypt()
    assert metadata.is_encrypted is False
    assert metadata.encryption_method is None

def test_decrypt_not_encrypted(metadata):
    with pytest.raises(MetadataDecryptionError):
        metadata.decrypt()

def test_is_keyword_present_true(metadata):
    assert metadata.is_keyword_present("Температура") is True

def test_is_keyword_present_false(metadata):
    assert metadata.is_keyword_present("влажность") is False

def test_summarize(metadata):
    summary = metadata.summarize()
    assert "Metadata for Document #1" in summary
    assert "Автор: Error" in summary
    assert "Теги: важное, эксперимент" in summary
    assert "Ключевые слова: температура, давление" in summary

def test_link_to_document_success(metadata):
    doc = DummyDocument(document_id=1)
    metadata.link_to_document(doc)
    assert doc.metadata == metadata

def test_link_to_document_mismatch(metadata):
    doc = DummyDocument(document_id=99)
    metadata.link_to_document(doc)
    assert doc.metadata is None

def test_to_dict(metadata):
    data = metadata.to_dict()
    assert data["document_id"] == 1
    assert data["author"] == "Error"
    assert data["tags"] == ["важное", "эксперимент"]
    assert data["keywords"] == ["температура", "давление"]
    assert isinstance(data["created_at"], str)

def test_is_created_before_true(metadata):
    future = datetime.now()
    assert metadata.is_created_before(future) is True

def test_is_created_before_false(metadata):
    past = datetime.now() - timedelta(days=2)
    assert metadata.is_created_before(past) is False

def test_is_created_after_true(metadata):
    past = datetime.now() - timedelta(days=2)
    assert metadata.is_created_after(past) is True

def test_is_created_after_false(metadata):
    future = datetime.now()
    assert metadata.is_created_after(future) is False
def test_add_tag_to_empty_list():
    m = Metadata(
        document_id=2,
        author="Error",
        created_at=datetime.now(),
        tags=[],
        keywords=[]
    )
    m.add_tag("новый")
    assert m.tags == ["новый"]

def test_remove_keyword_not_found_exception():
    m = Metadata(
        document_id=3,
        author="Error",
        created_at=datetime.now(),
        tags=[],
        keywords=["давление"]
    )
    with pytest.raises(MetadataKeywordNotFoundError):
        m.remove_keyword("температура")

def test_encrypt_twice(metadata):
    metadata.encrypt("AES")
    metadata.encrypt("RSA")
    assert metadata.is_encrypted is True
    assert metadata.encryption_method == "RSA"

def test_summarize_empty_fields():
    m = Metadata(
        document_id=4,
        author="Error",
        created_at=datetime.now(),
        tags=[],
        keywords=[]
    )
    summary = m.summarize()
    assert "Теги: —" in summary
    assert "Ключевые слова: —" in summary

def test_is_keyword_present_case_insensitive(metadata):
    assert metadata.is_keyword_present("ТЕМПЕРАТУРА") is True

def test_to_dict_encryption_fields(metadata):
    metadata.encrypt("AES")
    data = metadata.to_dict()
    assert data["is_encrypted"] is True
    assert data["encryption_method"] == "AES"
