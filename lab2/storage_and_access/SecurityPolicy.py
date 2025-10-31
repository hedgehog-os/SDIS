from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document
    from Permission import Permission


class SecurityPolicy:
    def __init__(self, policy_id: int, name: str, rules: List[str], enforced: bool) -> None:
        self.policy_id: int = policy_id
        self.name: str = name
        self.rules: List[str] = rules
        self.enforced: bool = enforced

    def add_rule(self, rule: str) -> None:
        """Добавляет новое правило в политику, если оно ещё не включено."""
        if rule and rule not in self.rules:
            self.rules.append(rule)

    def remove_rule(self, rule: str) -> None:
        """Удаляет правило из политики."""
        if rule in self.rules:
            self.rules.remove(rule)

    def clear_rules(self) -> None:
        """Удаляет все правила из политики."""
        self.rules.clear()

    def is_rule_enforced(self, rule: str) -> bool:
        """Проверяет, применяется ли конкретное правило."""
        return self.enforced and rule in self.rules

    def applies_to(self, rule_set: List[str]) -> bool:
        """Проверяет, охватывает ли политика все правила из заданного набора."""
        return all(rule in self.rules for rule in rule_set)

    def enable(self) -> None:
        """Включает применение политики."""
        self.enforced = True

    def disable(self) -> None:
        """Отключает применение политики."""
        self.enforced = False

    def toggle(self) -> None:
        """Переключает статус применения политики."""
        self.enforced = not self.enforced

    def summarize(self) -> str:
        """Форматирует краткую информацию о политике безопасности."""
        status = "Активна" if self.enforced else "Неактивна"
        return (
            f"Политика #{self.policy_id}: {self.name}\n"
            f"Статус: {status}\n"
            f"Правила ({len(self.rules)}): {', '.join(self.rules) if self.rules else '—'}"
        )

    def to_dict(self) -> dict:
        """Сериализует политику в словарь."""
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "rules": self.rules,
            "enforced": self.enforced
        }

    def enforce_on_permission(self, permission: "Permission") -> None:
        """Применяет политику к правам доступа: отключает действия, если политика активна."""
        if self.enforced:
            if "no_edit" in self.rules:
                permission.can_edit = False
            if "no_delete" in self.rules:
                permission.can_delete = False

    def restrict_document_access(self, document: "Document") -> None:
        """Применяет ограничения политики к документу (например, блокировка доступа)."""
        if self.enforced and "restricted_access" in self.rules:
            document.status = "restricted"

