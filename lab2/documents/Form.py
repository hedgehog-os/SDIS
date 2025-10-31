from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from CheckList import CheckList

class Form:
    def __init__(self,
                 form_id: int,
                 title: str,
                 author_id: int,
                 created_at: Optional[datetime] = None,
                 fields: Optional[List[str]] = None,
                 checklist: Optional["CheckList"] = None) -> None:
        self.form_id: int = form_id
        self.title: str = title
        self.author_id: int = author_id
        self.created_at: datetime = created_at or datetime.now()
        self.fields: List[str] = fields or []

        # Ассоциация
        self.checklist: Optional["CheckList"] = checklist

    def submit_form(self) -> None:
        """Отмечает форму как отправленную, если все поля заполнены и чек-лист завершён."""
        if not self.fields:
            raise ValueError("Форма не может быть отправлена без полей.")
        if self.checklist and not self.checklist.is_complete:
            raise ValueError("Форма не может быть отправлена: чек-лист не завершён.")
        print(f"Форма '{self.title}' успешно отправлена.")

    def validate_fields(self) -> bool:
        """Проверяет, что все поля формы непустые."""
        return all(isinstance(field, str) and field.strip() for field in self.fields)

    def assign_to_user(self, user_id: int) -> None:
        """Назначает форму пользователю (обновляет author_id)."""
        self.author_id = user_id

    def link_checklist(self, checklist: "CheckList") -> None:
        """Привязывает чек-лист к форме и обновляет обе стороны связи."""
        self.checklist = checklist
        checklist.form = self

    def unlink_checklist(self) -> None:
        """Удаляет связь с чек-листом."""
        if self.checklist:
            self.checklist.form = None
        self.checklist = None

    def get_checklist_status(self) -> str:
        """Возвращает статус чек-листа, если он связан с формой."""
        if not self.checklist:
            return "Чек-лист не привязан."
        return "Завершён" if self.checklist.is_complete else "В процессе"
