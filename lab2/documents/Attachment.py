from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document  # только для type hints


class Attachment:
    formats = {
        'pdf', 'docx', 'txt', 'md', 'html',
        'xlsx', 'csv', 'json', 'xml',
        'latex', 'py', 'cpp'
    }

    def __init__(self,
                 attachment_id: int,
                 filename: str,
                 filetype: str,
                 uploaded_at: Optional[datetime] = None,
                 document: Optional["Document"] = None,
                 format: str = None) -> None:
        
        self.attachment_id: int = attachment_id
        self.filename: str = filename
        self.filetype: str = filetype
        self.uploaded_at: datetime = uploaded_at or datetime.now()
        self.format = format
        self.document: Optional["Document"] = document


    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value not in self.formats:
            raise ValueError(f'Недопустимый формат: {value}')
        self._format = value

    def upload_file(self, document: "Document") -> None:
        self.document = document
        document.attachments.append(self)

    def link_to_document(self, document: "Document") -> None:
        self.document = document


    def is_valid_format(self) -> bool:
        """Проверяет, допустим ли формат файла."""
        return self.format in self.formats

    def rename_file(self, new_name: str) -> None:
        """Переименовывает файл вложения."""
        if not new_name or not isinstance(new_name, str):
            raise ValueError("Недопустимое имя файла.")
        self.filename = new_name

    def get_file_extension(self) -> str:
        """Возвращает расширение файла по имени."""
        if '.' in self.filename:
            return self.filename.split('.')[-1].lower()
        return ""

    def is_linked_to_document(self) -> bool:
        """Проверяет, связано ли вложение с каким-либо документом."""
        return self.document is not None

    def unlink_document(self) -> None:
        """Удаляет связь с документом, если она есть."""
        if self.document and self in self.document.attachments:
            self.document.attachments.remove(self)
        self.document = None
