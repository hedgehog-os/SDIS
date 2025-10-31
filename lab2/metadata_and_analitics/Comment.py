from datetime import datetime
from typing import Optional

class Comment:
    def __init__(self,
                 comment_id: int,
                 author_id: int,
                 document_id: int,
                 user_id: int,
                 content: str,
                 posted_at: Optional[datetime] = None) -> None:
        self.comment_id: int = comment_id
        self.author_id: int = author_id
        self.document_id: int = document_id
        self.user_id: int = user_id
        self.content: str = content
        self.posted_at: datetime = posted_at or datetime.now()

    def edit_content(self, new_content: str) -> None:
        """Обновляет текст комментария и фиксирует время изменения."""
        if new_content and isinstance(new_content, str):
            self.content = new_content
            self.posted_at = datetime.now()

    def contains_keyword(self, keyword: str) -> bool:
        """Проверяет, содержит ли комментарий заданное слово."""
        return keyword.lower() in self.content.lower()

    def is_recent(self, threshold_minutes: int = 60) -> bool:
        """Проверяет, был ли комментарий опубликован недавно."""
        delta = datetime.now() - self.posted_at
        return delta.total_seconds() < threshold_minutes * 60

    def format_for_display(self) -> str:
        """Форматирует комментарий для отображения."""
        return (
            f"Комментарий #{self.comment_id} (Документ {self.document_id})\n"
            f"Автор ID: {self.author_id}, Пользователь ID: {self.user_id}\n"
            f"Дата: {self.posted_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Текст: {self.content}"
        )

    def get_summary(self, max_length: int = 80) -> str:
        """Возвращает краткое описание комментария."""
        return self.content[:max_length] + ("..." if len(self.content) > max_length else "")
