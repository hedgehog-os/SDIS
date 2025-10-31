from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from persons.Editor import Editor  # только для type hints

class Revision:
    def __init__(self,
                 revision_id: int,
                 document_id: int,
                 version_number: int,
                 editor_id: int,
                 edited_at: Optional[datetime] = None,
                 notes: Optional[str] = None,
                 previous_revision: Optional["Revision"] = None,
                 change_history: Optional[List[str]] = None,
                 editor: Optional["Editor"] = None) -> None:
        self.revision_id: int = revision_id
        self.document_id: int = document_id
        self.version_number: int = version_number
        self.editor_id: int = editor_id
        self.edited_at: datetime = edited_at or datetime.now()
        self.notes: Optional[str] = notes
        self.previous_revision: Optional["Revision"] = previous_revision
        self.change_history: List[str] = change_history or []

        # Ассоциация
        self.editor: Optional["Editor"] = editor

    def add_change(self, description: str) -> None:
        """Добавляет описание изменения в историю."""
        if description and isinstance(description, str):
            self.change_history.append(description)

    def get_change_summary(self) -> str:
        """Возвращает краткое описание всех изменений."""
        if not self.change_history:
            return "Нет зафиксированных изменений."
        return "\n".join(f"- {change}" for change in self.change_history)

    def compare_to_previous(self) -> List[str]:
        """Сравнивает текущую историю изменений с предыдущей версией."""
        if not self.previous_revision:
            return ["Нет предыдущей версии для сравнения."]
        previous_changes = set(self.previous_revision.change_history)
        current_changes = set(self.change_history)
        new_changes = current_changes - previous_changes
        return list(new_changes)

    def is_major_revision(self) -> bool:
        """Определяет, является ли ревизия крупной (по количеству изменений)."""
        return len(self.change_history) >= 5

    def get_revision_info(self) -> str:
        """Возвращает краткую информацию о ревизии."""
        return (
            f"Версия: {self.version_number}\n"
            f"Редактор ID: {self.editor_id}\n"
            f"Дата редактирования: {self.edited_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Заметки: {self.notes or '—'}\n"
            f"Изменений: {len(self.change_history)}"
        )

    def export_as_text(self) -> str:
        """Возвращает текстовое представление ревизии."""
        lines = [
            f"Ревизия #{self.revision_id} — Версия {self.version_number}",
            f"Документ ID: {self.document_id}",
            f"Редактор ID: {self.editor_id}",
            f"Дата редактирования: {self.edited_at.strftime('%Y-%m-%d %H:%M')}",
            f"Заметки: {self.notes or '—'}",
            "История изменений:"
        ]
        lines += [f"- {change}" for change in self.change_history]
        return "\n".join(lines)

    def link_editor_notes(self, editor: Optional["Editor"]) -> None:
        """Добавляет заметки редактора в ревизию."""
        if editor:
            self.notes = editor.editor_notes

    def visualize_diff(self) -> str:
        """Генерирует текстовое сравнение текущей и предыдущей ревизии."""
        if not self.previous_revision:
            return "Нет предыдущей версии для сравнения."
        old = set(self.previous_revision.change_history)
        new = set(self.change_history)
        added = new - old
        removed = old - new

        lines = ["Изменения по сравнению с предыдущей версией:"]
        if added:
            lines.append("Добавлено:")
            lines += [f"  + {item}" for item in added]
        if removed:
            lines.append("Удалено:")
            lines += [f"  - {item}" for item in removed]
        if not added and not removed:
            lines.append("Изменений нет.")
        return "\n".join(lines)
