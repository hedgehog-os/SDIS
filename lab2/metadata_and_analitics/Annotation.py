from datetime import datetime
from typing import Optional

class Annotation:
    def __init__(self,
                 annotation_id: int,
                 document_id: int,
                 user_id: int,
                 text: str,
                 timestamp: Optional[datetime] = None) -> None:
        self.annotation_id: int = annotation_id
        self.document_id: int = document_id
        self.user_id: int = user_id
        self.text: str = text
        self.timestamp: datetime = timestamp or datetime.now()

    def edit_text(self, new_text: str) -> None:
        """Обновляет текст аннотации и фиксирует время изменения."""
        if new_text and isinstance(new_text, str):
            self.text = new_text
            self.timestamp = datetime.now()

    def contains_keyword(self, keyword: str) -> bool:
        """Проверяет, содержит ли аннотация заданное ключевое слово."""
        return keyword.lower() in self.text.lower()

    def get_summary(self, max_length: int = 50) -> str:
        """Возвращает краткое описание аннотации."""
        return self.text[:max_length] + ("..." if len(self.text) > max_length else "")

    def is_recent(self, threshold_minutes: int = 60) -> bool:
        """Проверяет, была ли аннотация создана недавно."""
        delta = datetime.now() - self.timestamp
        return delta.total_seconds() < threshold_minutes * 60

    def format_for_display(self) -> str:
        """Форматирует аннотацию для отображения."""
        return (
            f"Аннотация #{self.annotation_id} (Документ {self.document_id})\n"
            f"Пользователь: {self.user_id}\n"
            f"Время: {self.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
            f"Текст: {self.text}"
        )
