from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Form import Form


class CheckList:
    def __init__(self,
                 checklist_id: int,
                 title: str,
                 items: List[str],
                 form: Optional["Form"] = None,
                 checklist_items: list = None,
                 is_complete: bool = False,
                 ) -> None:
        self.checklist_id: int = checklist_id
        self.title: str = title
        self.items: List[str] = items
        self.checklist_items: List[str] = checklist_items
        self.is_complete: bool = is_complete

        # Ассоциация
        self.form: Optional["Form"] = form

    def mark_item_complete(self, item: str) -> None:
        """Отмечает элемент как выполненный."""
        if item not in self.items:
            raise ValueError(f"Элемент '{item}' не найден в чек-листе.")
        if item not in self.checklist_items:
            self.checklist_items.append(item)
        self._update_completion_status()

    def reset_checklist(self) -> None:
        """Сбрасывает выполнение всех пунктов чек-листа."""
        self.checklist_items.clear()
        self.is_complete = False

    def sort_checklist(self, reverse: bool = False) -> None:
        """Сортирует элементы чек-листа по алфавиту."""
        self.items.sort(reverse=reverse)

    def _update_completion_status(self) -> None:
        """Обновляет статус выполнения чек-листа."""
        self.is_complete = set(self.items) == set(self.checklist_items)

    def link_to_form(self, form: "Form") -> None:
        """Привязывает чек-лист к форме."""
        self.form = form
        form.checklist = self

    def unlink_form(self) -> None:
        """Удаляет связь с формой."""
        if self.form:
            self.form.checklist = None
        self.form = None

    def export_as_text(self) -> str:
        """Возвращает текстовое представление чек-листа."""
        status = "Выполнено" if self.is_complete else "В процессе"
        lines = [f"Чек-лист: {self.title}", f"Статус: {status}", "Пункты:"]
        for item in self.items:
            mark = "completed" if item in self.checklist_items else "not fulfilled"
            lines.append(f"{mark} {item}")
        return "\n".join(lines)

    def preview(self) -> None:
        """Выводит краткий визуальный обзор чек-листа."""
        print(self.export_as_text())

    def is_form_ready(self) -> bool:
        """Проверяет, заполнена ли форма, связанная с чек-листом."""
        if not self.form:
            return False
        return len(self.form.fields) > 0
