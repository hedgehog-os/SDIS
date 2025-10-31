from datetime import datetime
from Exceptions import PhoneNumberFormatError, EmailFormatError, SecurityQuestionEmptyError
class UserProfile:
    account_statuses: set[str] = {'active', 'suspended', 'pending', 'deleted'}

    def __init__(self,
                 expert_id: int,
                 username: str,
                 email: str,
                 phone_number: str,
                 security_question: str,
                 two_factor_enabled: bool,
                 preferred_language: str,
                 timezone: str,
                 account_status: str,
                 registered_at: datetime | None = None) -> None:
        self.expert_id: int = expert_id
        self.username: str = username
        self.email: str = email
        self.phone_number: str = phone_number
        self.security_question: str = security_question
        self.two_factor_enabled: bool = two_factor_enabled
        self.preferred_language: str = preferred_language
        self.timezone: str = timezone
        self._account_status: str = ""
        self.account_status = account_status
        self.registered_at: datetime = registered_at or datetime.now()

    @property
    def account_status(self) -> str:
        return self._account_status

    @account_status.setter
    def account_status(self, value: str) -> None:
        if value not in self.account_statuses:
            raise ValueError(f"Недопустимый статус: {value}")
        self._account_status = value

    def enable_two_factor(self) -> None:
        """Включает двухфакторную аутентификацию."""
        self.two_factor_enabled = True

    def disable_two_factor(self) -> None:
        """Отключает двухфакторную аутентификацию."""
        self.two_factor_enabled = False

    def reset_security_question(self, new_question: str) -> None:
        if not new_question:
            raise SecurityQuestionEmptyError("Контрольный вопрос не может быть пустым.")
        self.security_question = new_question

    def update_email(self, new_email: str) -> None:
        if not new_email or "@" not in new_email:
            raise EmailFormatError("Неверный формат email.")
        self.email = new_email

    def update_phone(self, new_phone: str) -> None:
        if not new_phone.isdigit():
            raise PhoneNumberFormatError("Номер телефона должен содержать только цифры.")
        self.phone_number = new_phone

    def set_language(self, language: str) -> None:
        """Устанавливает предпочтительный язык."""
        self.preferred_language = language

    def set_timezone(self, timezone: str) -> None:
        """Устанавливает часовой пояс."""
        self.timezone = timezone

    def is_active(self) -> bool:
        """Проверяет, активен ли профиль."""
        return self.account_status == "active"

    def is_suspended(self) -> bool:
        """Проверяет, приостановлен ли профиль."""
        return self.account_status == "suspended"

    def is_pending(self) -> bool:
        """Проверяет, ожидает ли профиль подтверждения."""
        return self.account_status == "pending"

    def summarize(self) -> str:
        """Форматирует краткую информацию о профиле."""
        return (
            f"Профиль #{self.expert_id}: {self.username}\n"
            f"Email: {self.email} | Телефон: {self.phone_number}\n"
            f"Статус: {self.account_status}\n"
            f"Язык: {self.preferred_language} | Часовой пояс: {self.timezone}\n"
            f"2FA: {'включена' if self.two_factor_enabled else 'отключена'}\n"
            f"Зарегистрирован: {self.registered_at.strftime('%Y-%m-%d %H:%M')}"
        )

    def to_dict(self) -> dict:
        """Сериализует профиль в словарь."""
        return {
            "expert_id": self.expert_id,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "security_question": self.security_question,
            "two_factor_enabled": self.two_factor_enabled,
            "preferred_language": self.preferred_language,
            "timezone": self.timezone,
            "account_status": self.account_status,
            "registered_at": self.registered_at.isoformat()
        }
