from datetime import datetime
from typing import List, Optional

class Editor:
    def __init__(self,
                 editor_id: int,
                 fullname: str,
                 email: str,
                 editor_notes: Optional[str] = "",
                 revision_number: int = 1,
                 change_history: Optional[str] = "") -> None:
        self.editor_id: int = editor_id
        self.fullname: str = fullname
        self.email: str = email
        self.editor_notes: str = editor_notes or ""
        self.revision_number: int = revision_number
        self.change_history: str = change_history or ""

    def update_email(self, new_email: str) -> None:
        if new_email and "@" in new_email:
            self.email = new_email

    def append_note(self, note: str) -> None:
        if note:
            self.editor_notes += f"\n• {note}"

    def increment_revision(self) -> None:
        self.revision_number += 1

    def record_change(self, change: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.change_history += f"\n[{timestamp}] {change}"

    def has_changes(self) -> bool:
        return bool(self.change_history.strip())

    def get_change_log(self) -> List[str]:
        return [line for line in self.change_history.strip().split("\n") if line]

    def summarize(self) -> str:
        return (
            f"Редактор #{self.editor_id}: {self.fullname}\n"
            f"Email: {self.email}\n"
            f"Ревизия: {self.revision_number}\n"
            f"Заметки: {self.editor_notes or '—'}\n"
            f"Изменений: {len(self.get_change_log())}"
        )

    def to_dict(self) -> dict:
        return {
            "editor_id": self.editor_id,
            "fullname": self.fullname,
            "email": self.email,
            "editor_notes": self.editor_notes,
            "revision_number": self.revision_number,
            "change_history": self.get_change_log()
        }
