from datetime import datetime
from typing import Dict

class Observer:
    def __init__(self,
                 observer_id: int,
                 fullname: str,
                 email: str,
                 access_logs: Dict[str, datetime],
                 last_accessed: datetime) -> None:
        self.observer_id: int = observer_id
        self.fullname: str = fullname
        self.email: str = email
        self.access_logs: Dict[str, datetime] = access_logs
        self.last_accessed: datetime = last_accessed

    def log_access(self, resource: str) -> None:
        """Регистрирует доступ к ресурсу и обновляет дату последнего входа."""
        now = datetime.now()
        self.access_logs[resource] = now
        self.last_accessed = now

    def remove_access_log(self, resource: str) -> None:
        """Удаляет запись о доступе к указанному ресурсу."""
        if resource in self.access_logs:
            del self.access_logs[resource]

    def get_accessed_resources(self) -> list[str]:
        """Возвращает список всех ресурсов, к которым был доступ."""
        return list(self.access_logs.keys())

    def get_last_access_time(self, resource: str) -> datetime | None:
        """Возвращает время последнего доступа к ресурсу."""
        return self.access_logs.get(resource)

    def was_active_recently(self, minutes: int = 60) -> bool:
        """Проверяет, был ли наблюдатель активен в последние N минут."""
        from datetime import timedelta
        return self.last_accessed >= datetime.now() - timedelta(minutes=minutes)

    def get_recent_resources(self, minutes: int = 60) -> list[str]:
        """Возвращает ресурсы, к которым был доступ в последние N минут."""
        from datetime import timedelta
        threshold = datetime.now() - timedelta(minutes=minutes)
        return [r for r, t in self.access_logs.items() if t >= threshold]

    def summarize(self) -> str:
        """Форматирует краткую информацию о наблюдателе."""
        return (
            f"Наблюдатель #{self.observer_id}: {self.fullname}\n"
            f"Email: {self.email}\n"
            f"Последний доступ: {self.last_accessed.strftime('%Y-%m-%d %H:%M')}\n"
            f"Ресурсов просмотрено: {len(self.access_logs)}"
        )

    def to_dict(self) -> dict:
        """Сериализует наблюдателя в словарь."""
        return {
            "observer_id": self.observer_id,
            "fullname": self.fullname,
            "email": self.email,
            "last_accessed": self.last_accessed.isoformat(),
            "access_logs": {r: t.isoformat() for r, t in self.access_logs.items()}
        }
