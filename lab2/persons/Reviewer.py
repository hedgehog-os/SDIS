from datetime import datetime, timedelta
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Draft import Draft

class Reviewer:
    def __init__(self,
                 reviewer_id: int,
                 full_name: str,
                 affiliation: Optional[str] = None,
                 reviewed_drafts: Optional[List["Draft"]] = None,
                 comments: Optional[List[str]] = None,
                 last_reviewed_at: Optional[datetime] = None) -> None:
        self.reviewer_id: int = reviewer_id
        self.full_name: str = full_name
        self.affiliation: Optional[str] = affiliation
        self.reviewed_drafts: List["Draft"] = reviewed_drafts or []
        self.comments: List[str] = comments or []
        self.last_reviewed_at: Optional[datetime] = last_reviewed_at

    def review_draft(self, draft: "Draft", comment: Optional[str] = None) -> None:
        """Назначает рецензента на черновик и добавляет комментарий, если указан."""
        if draft not in self.reviewed_drafts:
            self.reviewed_drafts.append(draft)
        if draft.reviewed_by is None:
            draft.reviewed_by = []
        if self not in draft.reviewed_by:
            draft.reviewed_by.append(self)
        if comment:
            self.comments.append(comment)
        self.last_reviewed_at = datetime.now()

    def remove_draft(self, draft: "Draft") -> None:
        """Удаляет черновик из списка рецензированных и обновляет обе стороны связи."""
        if draft in self.reviewed_drafts:
            self.reviewed_drafts.remove(draft)
        if draft.reviewed_by and self in draft.reviewed_by:
            draft.reviewed_by.remove(self)

    def count_reviewed_drafts(self) -> int:
        """Возвращает количество черновиков, рецензированных этим рецензентом."""
        return len(self.reviewed_drafts)

    def get_recent_drafts(self, days: int = 30) -> List["Draft"]:
        """Возвращает черновики, рецензированные за последние N дней."""
        threshold = datetime.now() - timedelta(days=days)
        return [d for d in self.reviewed_drafts if d.created_at >= threshold]

    def get_comments_for_draft(self, draft: "Draft") -> List[str]:
        """Возвращает комментарии, относящиеся к конкретному черновику."""
        return self.comments if draft in self.reviewed_drafts else []

    def summarize(self) -> str:
        """Форматирует краткую информацию о рецензенте."""
        return (
            f"Рецензент #{self.reviewer_id}: {self.full_name}\n"
            f"Аффилиация: {self.affiliation or '—'}\n"
            f"Рецензировано черновиков: {self.count_reviewed_drafts()}\n"
            f"Комментариев: {len(self.comments)}\n"
            f"Последняя активность: {self.last_reviewed_at.strftime('%Y-%m-%d') if self.last_reviewed_at else '—'}"
        )

    def to_dict(self) -> dict:
        """Сериализует рецензента в словарь."""
        return {
            "reviewer_id": self.reviewer_id,
            "full_name": self.full_name,
            "affiliation": self.affiliation,
            "reviewed_draft_ids": [d.draft_id for d in self.reviewed_drafts],
            "comments": self.comments,
            "last_reviewed_at": self.last_reviewed_at.isoformat() if self.last_reviewed_at else None
        }
