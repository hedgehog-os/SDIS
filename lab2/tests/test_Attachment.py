import pytest
from datetime import datetime
from documents.Attachment import Attachment

class DummyDocument:
    def __init__(self, document_id):
        self.document_id = document_id
        self.attachments = []

@pytest.fixture
def sample_attachment():
    return Attachment(
        attachment_id=1,
        filename="report.pdf",
        filetype="application/pdf",
        format="pdf"
    )

def test_initialization_defaults():
    att = Attachment(2, "data.csv", "text/csv", format="csv")
    assert att.filename == "data.csv"
    assert att.filetype == "text/csv"
    assert att.format == "csv"
    assert isinstance(att.uploaded_at, datetime)
    assert att.document is None

def test_valid_format_property(sample_attachment):
    assert sample_attachment.format == "pdf"
    assert sample_attachment.is_valid_format()

def test_invalid_format_raises():
    with pytest.raises(ValueError):
        Attachment(3, "bad.exe", "binary", format="exe")

def test_rename_file_valid(sample_attachment):
    sample_attachment.rename_file("new_name.pdf")
    assert sample_attachment.filename == "new_name.pdf"

def test_rename_file_invalid(sample_attachment):
    with pytest.raises(ValueError):
        sample_attachment.rename_file("")

def test_get_file_extension(sample_attachment):
    assert sample_attachment.get_file_extension() == "pdf"

def test_get_file_extension_no_dot():
    att = Attachment(4, "readme", "text/plain", format="txt")
    assert att.get_file_extension() == ""

def test_upload_file_links_and_appends(sample_attachment):
    doc = DummyDocument(101)
    sample_attachment.upload_file(doc)
    assert sample_attachment.document == doc
    assert sample_attachment in doc.attachments

def test_link_to_document_only(sample_attachment):
    doc = DummyDocument(102)
    sample_attachment.link_to_document(doc)
    assert sample_attachment.document == doc
    assert sample_attachment not in doc.attachments

def test_is_linked_to_document(sample_attachment):
    assert not sample_attachment.is_linked_to_document()
    doc = DummyDocument(103)
    sample_attachment.link_to_document(doc)
    assert sample_attachment.is_linked_to_document()

def test_unlink_document_removes_from_doc(sample_attachment):
    doc = DummyDocument(104)
    sample_attachment.upload_file(doc)
    sample_attachment.unlink_document()
    assert sample_attachment.document is None
    assert sample_attachment not in doc.attachments
