from datetime import datetime, timedelta
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from persons.UserProfile import UserProfile

class Student:
    def __init__(self,
                 student_id: int,
                 fullname: str,
                 email: str,
                 department: str,
                 assigned_documents: List[int] | None = None,
                 activity_log: Dict[str, datetime] | None = None,
                 profile: Optional["UserProfile"] = None) -> None:
        self.student_id: int = student_id
        self.fullname: str = fullname
        self.email: str = email
        self.department: str = department
        self.assigned_documents: List[int] = assigned_documents or []
        self.activity_log: Dict[str, datetime] = activity_log or {}

        # Ассоциация
        self.profile: "UserProfile" = profile

    def assign_document(self, document_id: int) -> None:
        """Назначает документ студенту, если он ещё не назначен."""
        if document_id not in self.assigned_documents:
            self.assigned_documents.append(document_id)

    def remove_document(self, document_id: int) -> None:
        """Удаляет документ из списка назначенных."""
        if document_id in self.assigned_documents:
            self.assigned_documents.remove(document_id)

    def has_document(self, document_id: int) -> bool:
        """Проверяет, назначен ли студенту указанный документ."""
        return document_id in self.assigned_documents

    def log_activity(self, action: str) -> None:
        """Регистрирует активность студента."""
        self.activity_log[action] = datetime.now()

    def get_last_activity(self) -> Optional[tuple[str, datetime]]:
        """Возвращает последнюю активность студента."""
        if not self.activity_log:
            return None
        return max(self.activity_log.items(), key=lambda item: item[1])

    def get_recent_activities(self, minutes: int = 60) -> List[str]:
        """Возвращает действия, совершённые за последние N минут."""
        threshold = datetime.now() - timedelta(minutes=minutes)
        return [action for action, timestamp in self.activity_log.items() if timestamp >= threshold]

    def update_profile(self, profile: "UserProfile") -> None:
        """Привязывает профиль пользователя к студенту."""
        self.profile = profile

    def get_profile_summary(self) -> str:
        """Возвращает краткое описание профиля, если он есть."""
        if not self.profile:
            return "Профиль не привязан."
        return f"{self.profile.username} ({self.profile.role}) — {self.profile.status}"

    def summarize(self) -> str:
        """Форматирует краткую информацию о студенте."""
        last_activity = self.get_last_activity()
        activity_str = f"{last_activity[0]} @ {last_activity[1].strftime('%Y-%m-%d %H:%M')}" if last_activity else "—"
        return (
            f"Студент #{self.student_id}: {self.fullname}\n"
            f"Email: {self.email} | Отделение: {self.department}\n"
            f"Документов назначено: {len(self.assigned_documents)}\n"
            f"Последняя активность: {activity_str}"
        )

    def to_dict(self) -> dict:
        """Сериализует студента в словарь."""
        return {
            "student_id": self.student_id,
            "fullname": self.fullname,
            "email": self.email,
            "department": self.department,
            "assigned_documents": self.assigned_documents,
            "activity_log": {k: v.isoformat() for k, v in self.activity_log.items()},
            "profile_id": self.profile.user_id if self.profile else None
        }
