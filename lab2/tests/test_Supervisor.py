from datetime import datetime, timedelta

class DummyComment:
    def __init__(self, comment_id, document_id, user_id, content, posted_at):
        self.comment_id = comment_id
        self.document_id = document_id
        self.user_id = user_id
        self.content = content
        self.posted_at = posted_at

class DummyDocument:
    def __init__(self, document_id, status, created_at=None):
        self.document_id = document_id
        self.status = status
        self.created_at = created_at or datetime.now()
        self.comments = []
import pytest
from persons.Supervisor import Supervisor

@pytest.fixture
def supervisor():
    return Supervisor(
        supervisor_id=1,
        fullname="Error Supervisor",
        email="error@lab.com",
        reviewed_documents=[]
    )

def test_review_document_without_comment(supervisor):
    doc = DummyDocument(document_id=102, status="final")
    supervisor.review_document(doc)
    assert doc in supervisor.reviewed_documents
    assert doc.comments == []

def test_remove_document(supervisor):
    doc = DummyDocument(document_id=103, status="archived")
    supervisor.review_document(doc)
    supervisor.remove_document(doc)
    assert doc not in supervisor.reviewed_documents

def test_count_reviewed_documents(supervisor):
    d1 = DummyDocument(document_id=201, status="draft")
    d2 = DummyDocument(document_id=202, status="final")
    supervisor.review_document(d1)
    supervisor.review_document(d2)
    assert supervisor.count_reviewed_documents() == 2

def test_get_documents_by_status(supervisor):
    d1 = DummyDocument(document_id=301, status="draft")
    d2 = DummyDocument(document_id=302, status="final")
    d3 = DummyDocument(document_id=303, status="draft")
    supervisor.review_document(d1)
    supervisor.review_document(d2)
    supervisor.review_document(d3)
    drafts = supervisor.get_documents_by_status("draft")
    assert drafts == [d1, d3]

def test_get_recent_documents(supervisor):
    recent = DummyDocument(document_id=401, status="final", created_at=datetime.now() - timedelta(days=5))
    old = DummyDocument(document_id=402, status="final", created_at=datetime.now() - timedelta(days=60))
    supervisor.review_document(recent)
    supervisor.review_document(old)
    recent_docs = supervisor.get_recent_documents(days=30)
    assert recent in recent_docs
    assert old not in recent_docs

def test_summarize_output(supervisor):
    doc = DummyDocument(document_id=601, status="final")
    supervisor.review_document(doc)
    summary = supervisor.summarize()
    assert f"Руководитель #{supervisor.supervisor_id}" in summary
    assert "Рецензировано документов: 1" in summary

def test_to_dict_format(supervisor):
    doc = DummyDocument(document_id=701, status="archived")
    supervisor.review_document(doc)
    data = supervisor.to_dict()
    assert data["supervisor_id"] == 1
    assert data["fullname"] == "Error Supervisor"
    assert data["email"] == "error@lab.com"
    assert data["reviewed_document_ids"] == [701]
