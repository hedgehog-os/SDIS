from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from persons.UserProfile import UserProfile
    from documents.Document import Document


class AccessLog:
    allowed_actions = {'view', 'edit', 'download'}

    def __init__(self, user_id: int, action: str, email: str, timestamp: datetime, document_id: Optional[int] = None) -> None:
        self.user_id: int = user_id
        self.email: str = email
        self.timestamp: datetime = timestamp
        self.document_id: Optional[int] = document_id
        self._action: str = ""  # инициализация внутреннего поля
        self.action = action     # вызов сеттера с валидацией

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, value: str) -> None:
        if value not in self.allowed_actions:
            raise ValueError(f'Недопустимый статус: {value}')
        self._action = value

    def is_for_document(self, doc_id: int) -> bool:
        return self.document_id == doc_id

    def is_recent(self, minutes: int = 60) -> bool:
        return self.timestamp >= datetime.now() - timedelta(minutes=minutes)

    def is_action(self, action_type: str) -> bool:
        return self.action == action_type

    def summarize(self) -> str:
        doc_info = f"Документ #{self.document_id}" if self.document_id is not None else "Без документа"
        return (
            f"Доступ: {self.action}\n"
            f"Пользователь ID: {self.user_id}\n"
            f"{doc_info}\n"
            f"Время: {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),
            "document_id": self.document_id
        }

    def is_by_user(self, user_id: int) -> bool:
        return self.user_id == user_id

    def matches_user_profile(self, profile: "UserProfile") -> bool:
        return self.user_id == profile.expert_id and self.email_matches(profile.email)

    def email_matches(self, email: str) -> bool:
        return self.email == email

    def is_related_to(self, document: "Document") -> bool:
        return self.document_id == document.document_id

    def generate_audit_entry(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
            "action": self.action,
            "document_id": self.document_id
        }

    def format_for_notification(self) -> str:
        doc_info = f"документ #{self.document_id}" if self.document_id else "неуказанный документ"
        return (
            f"Пользователь #{self.user_id} выполнил действие '{self.action}' "
            f"с {doc_info} в {self.timestamp.strftime('%Y-%m-%d %H:%M')}."
        )
