from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from persons.UserProfile import UserProfile
    from documents.Document import Document
    from storage_and_access.AccessLog import AccessLog


class Permission:
    def __init__(self, user_id: int, document_id: int, can_view: bool, can_edit: bool, can_delete: bool) -> None:
        self.user_id: int = user_id
        self.document_id: int = document_id
        self.can_view: bool = can_view
        self.can_edit: bool = can_edit
        self.can_delete: bool = can_delete

    def has_view_permission(self) -> bool:
        """Проверяет, может ли пользователь просматривать документ."""
        return self.can_view

    def has_edit_permission(self) -> bool:
        """Проверяет, может ли пользователь редактировать документ."""
        return self.can_edit

    def has_delete_permission(self) -> bool:
        """Проверяет, может ли пользователь удалять документ."""
        return self.can_delete

    def has_any_permission(self) -> bool:
        """Проверяет, есть ли у пользователя хотя бы одно разрешение."""
        return self.can_view or self.can_edit or self.can_delete

    def grant_all(self) -> None:
        """Выдаёт все права пользователю."""
        self.can_view = True
        self.can_edit = True
        self.can_delete = True

    def revoke_all(self) -> None:
        """Отбирает все права у пользователя."""
        self.can_view = False
        self.can_edit = False
        self.can_delete = False

    def update_permissions(self, view: bool, edit: bool, delete: bool) -> None:
        """Обновляет права доступа."""
        self.can_view = view
        self.can_edit = edit
        self.can_delete = delete

    def summarize(self) -> str:
        """Форматирует краткую информацию о правах доступа."""
        return (
            f"Права пользователя #{self.user_id} к документу #{self.document_id}:\n"
            f"Просмотр: {'Разрешен' if self.can_view else 'Запрещен'} | "
            f"Редактирование: {'Разрешен' if self.can_edit else 'Запрещен'} | "
            f"Удаление: {'Разрешен' if self.can_delete else 'Запрещен'}"
        )

    def to_dict(self) -> dict:
        """Сериализует объект прав доступа в словарь."""
        return {
            "user_id": self.user_id,
            "document_id": self.document_id,
            "can_view": self.can_view,
            "can_edit": self.can_edit,
            "can_delete": self.can_delete
        }

    def applies_to_user(self, user: "UserProfile") -> bool:
        """Проверяет, относится ли разрешение к данному пользователю."""
        return self.user_id == user.expert_id

    def applies_to_document(self, document: "Document") -> bool:
        """Проверяет, относится ли разрешение к данному документу."""
        return self.document_id == document.document_id

    def enforce_on_document(self, document: "Document") -> str:
        """Возвращает описание доступных действий над документом."""
        actions = []
        if self.can_view:
            actions.append("просмотр")
        if self.can_edit:
            actions.append("редактирование")
        if self.can_delete:
            actions.append("удаление")
        return f"Пользователь может: {', '.join(actions) or 'ничего'} с документом '{document.title}'"

    def validate_access_log(self, log: "AccessLog") -> bool:
        """Проверяет, соответствует ли лог разрешённому действию."""
        if log.user_id != self.user_id or log.document_id != self.document_id:
            return False
        return self._is_action_allowed(log.action)

    def export_permission_report(self, user: "UserProfile", document: "Document") -> str:
        """Формирует текстовый отчёт о правах пользователя к документу."""
        return (
            f"Пользователь: {user.username} (#{user.expert_id})\n"
            f"Документ: {document.title} (#{document.document_id})\n"
            f"Права: {'Просмотр' if self.can_view else '—'} "
            f"{'Редактирование' if self.can_edit else '—'} "
            f"{'Удаление' if self.can_delete else '—'}"
        )

    def _is_action_allowed(self, action: str) -> bool:
        """Проверяет, разрешено ли действие согласно текущим правам."""
        return (
            (action == "view" and self.can_view) or
            (action == "edit" and self.can_edit) or
            (action == "delete" and self.can_delete)
        )
