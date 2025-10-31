from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Document import Document
    from Attachment import Attachment
    from Revision import Revision
    from metadata_and_analitics.Comment import Comment
    from metadata_and_analitics.Keyword import Keyword  


class Template:

    formats = {
        'md', 'xml', 'json'
    }

    def __init__(self,
                 template_id: int,
                 name: str,
                 content_structure: str,
                 applicable_documents: Optional[List["Document"]] = None) -> None:
        self.template_id: int = template_id
        self.name: str = name
        self.content_structure: str = content_structure

        # Ассоциация
        self.applicable_documents: Optional[List["Document"]] = applicable_documents
        self.attachments: List["Attachment"] = []
        self.revisions: List["Revision"] = []
        self.comments: List["Comment"] = []
        self.keywords: List["Keyword"] = []


    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value not in self.formats:
            raise ValueError(f'Недопустимый формат: {value}')
        self._format = value

    def assign_template(self, template: "Template") -> None:
        """Привязывает шаблон к документу и обновляет обратную связь."""
        self.template = template
        if template.applicable_documents is None:
            template.applicable_documents = []
        if self not in template.applicable_documents:
            template.applicable_documents.append(self)

    def remove_template(self) -> None:
        """Удаляет связь с шаблоном."""
        if self.template and self in self.template.applicable_documents:
            self.template.applicable_documents.remove(self)
        self.template = None

    def add_attachment(self, attachment: "Attachment") -> None:
        """Добавляет вложение к документу и устанавливает связь."""
        self.attachments.append(attachment)
        attachment.document = self

    def remove_attachment(self, attachment: "Attachment") -> None:
        """Удаляет вложение из документа и разрывает связь."""
        if attachment in self.attachments:
            self.attachments.remove(attachment)
            attachment.document = None

    def get_latest_revision(self) -> Optional["Revision"]:
        """Возвращает последнюю ревизию документа."""
        if not self.revisions:
            return None
        return max(self.revisions, key=lambda r: r.version_number)

    def get_revision_history(self) -> List[str]:
        """Возвращает краткую историю изменений всех ревизий."""
        return [f"v{r.version_number}: {r.notes or '—'}" for r in self.revisions]

    def get_comment_summary(self) -> str:
        """Возвращает краткий обзор комментариев."""
        if not self.comments:
            return "Комментариев нет."
        return "\n".join(f"- {c.content}" for c in self.comments)

    def get_keywords_as_text(self) -> str:
        """Возвращает ключевые слова в виде строки."""
        if not self.keywords:
            return "Нет ключевых слов."
        return ", ".join(k.word for k in self.keywords)
