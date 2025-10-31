from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from persons.Reviewer import Reviewer

class Draft:
    def __init__(self,
                 draft_id: int,
                 title: str,
                 author_id: int,
                 content: str,
                 created_at: Optional[datetime] = None,
                 reviewed_by: Optional[List["Reviewer"]] = None) -> None:
        self.draft_id: int = draft_id
        self.title: str = title
        self.author_id: int = author_id
        self.content: str = content
        self.created_at: datetime = created_at or datetime.now()

        # Ассоциация
        self.reviewed_by: Optional[List["Reviewer"]] = reviewed_by

    def assign_reviewer(self, reviewer: "Reviewer") -> None:
        """Назначает рецензента на черновик и обновляет обе стороны ассоциации."""
        if self.reviewed_by is None:
            self.reviewed_by = []
        if reviewer not in self.reviewed_by:
            self.reviewed_by.append(reviewer)
            reviewer.reviewed_drafts.append(self)
            reviewer.last_reviewed_at = datetime.now()

    def remove_reviewer(self, reviewer: "Reviewer") -> None:
        """Удаляет рецензента из черновика и обновляет обе стороны ассоциации."""
        if self.reviewed_by and reviewer in self.reviewed_by:
            self.reviewed_by.remove(reviewer)
        if self in reviewer.reviewed_drafts:
            reviewer.reviewed_drafts.remove(self)

    def get_reviewer_names(self) -> List[str]:
        """Возвращает список имён всех рецензентов, назначенных на черновик."""
        return [r.full_name for r in self.reviewed_by] if self.reviewed_by else []

    def is_reviewed(self) -> bool:
        """Проверяет, есть ли хотя бы один рецензент."""
        return bool(self.reviewed_by)

    def add_reviewer_comment(self, reviewer: "Reviewer", comment: str) -> None:
        """Добавляет комментарий от рецензента, если он связан с черновиком."""
        if reviewer in self.reviewed_by:
            reviewer.comments.append(comment)
            reviewer.last_reviewed_at = datetime.now()
        else:
            raise ValueError("Рецензент не назначен на этот черновик.")

    def export_as_text(self) -> str:
        """Возвращает текстовое представление черновика."""
        lines = [
            f"Черновик: {self.title}",
            f"Автор ID: {self.author_id}",
            f"Создан: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            "Содержание:",
            self.content
        ]
        return "\n".join(lines)

    def get_all_comments(self) -> List[str]:
        """Собирает все комментарии от рецензентов, связанных с этим черновиком."""
        if not self.reviewed_by:
            return []
        return [comment for reviewer in self.reviewed_by for comment in reviewer.comments]

    def get_review_summary(self) -> str:
        """Формирует краткий обзор рецензирования."""
        if not self.reviewed_by:
            return "Нет рецензентов."
        summary = [f"{r.full_name} ({r.affiliation or 'без указания'}) — {len(r.comments)} комментариев" for r in self.reviewed_by]
        return "\n".join(summary)
