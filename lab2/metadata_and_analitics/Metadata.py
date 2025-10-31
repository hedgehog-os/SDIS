from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from Exceptions import (
    MetadataTagConflictError,
    MetadataKeywordNotFoundError,
    MetadataEncryptionError,
    MetadataDecryptionError
)

if TYPE_CHECKING:
    from documents.Document import Document
    from Keyword import Keyword


class Metadata:
    def __init__(self,
                document_id: int,
                author: str,
                created_at: datetime,
                tags: List[str],
                keywords: List[str],
                approved: bool = False,
                is_encrypted: bool = False,
                encryption_method: Optional[str] = None) -> None:
        
        self.document_id: int = document_id
        self.author: str = author
        self.created_at: datetime = created_at
        self.tags: List[str] = tags
        self.keywords: List[str] = keywords
        self.approved: bool = approved
        self.is_encrypted: bool = is_encrypted
        self.encryption_method: Optional[str] = encryption_method

    def add_tag(self, tag: str) -> None:
        if tag in self.tags:
            raise MetadataTagConflictError(f"Тег '{tag}' уже существует.")
        self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Удаляет тег, если он существует."""
        if tag in self.tags:
            self.tags.remove(tag)

    def remove_keyword(self, keyword: str) -> None:
        if keyword not in self.keywords:
            raise MetadataKeywordNotFoundError(f"Ключевое слово '{keyword}' не найдено.")
        self.keywords.remove(keyword)

    def approve(self) -> None:
        """Устанавливает статус утверждения."""
        self.approved = True

    def reject(self) -> None:
        """Снимает статус утверждения."""
        self.approved = False

    def encrypt(self, method: str = "AES-256") -> None:
        if not method:
            raise MetadataEncryptionError("Метод шифрования не указан.")
        self.is_encrypted = True
        self.encryption_method = method

    def decrypt(self) -> None:
        if not self.is_encrypted:
            raise MetadataDecryptionError("Метаданные не зашифрованы.")
        self.is_encrypted = False
        self.encryption_method = None

    def is_keyword_present(self, word: str) -> bool:
        """Проверяет наличие ключевого слова."""
        return word.lower() in (kw.lower() for kw in self.keywords)

    def summarize(self) -> str:
        """Возвращает краткую сводку метаданных."""
        return (
            f"Metadata for Document #{self.document_id}\n"
            f"Автор: {self.author}\n"
            f"Создано: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Теги: {', '.join(self.tags) or '—'}\n"
            f"Ключевые слова: {', '.join(self.keywords) or '—'}\n"
            f"Утверждён: {'Да' if self.approved else 'Нет'}\n"
            f"Шифрование: {'Да' if self.is_encrypted else 'Нет'}"
            + (f" ({self.encryption_method})" if self.is_encrypted else "")
        )

    def link_to_document(self, document: "Document") -> None:
        """Привязывает метаданные к документу, если ID совпадают."""
        if document.document_id == self.document_id:
            document.metadata = self

    def sync_tags_and_keywords(self, document: "Document") -> None:
        """Синхронизирует теги и ключевые слова с документом."""
        from Keyword import Keyword  # локальный импорт
        document.tags = list(set(document.tags + self.tags))
        if document.keywords is None:
            document.keywords = []
        for word in self.keywords:
            if not any(k.word == word for k in document.keywords):
                document.keywords.append(Keyword(word=word, relevance_score=0.5))


    def to_dict(self) -> dict:
        """Сериализует метаданные в словарь."""
        return {
            "document_id": self.document_id,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "keywords": self.keywords,
            "approved": self.approved,
            "is_encrypted": self.is_encrypted,
            "encryption_method": self.encryption_method
        }

    def is_created_before(self, date: datetime) -> bool:
        """Проверяет, были ли метаданные созданы до указанной даты."""
        return self.created_at < date

    def is_created_after(self, date: datetime) -> bool:
        """Проверяет, были ли метаданные созданы после указанной даты."""
        return self.created_at > date
