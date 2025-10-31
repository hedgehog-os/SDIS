from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Document import Document
    from Insight import Insight


class Keyword:
    def __init__(self, word: str, relevance_score: float) -> None:
        self.word: str = word
        self.relevance_score: float = relevance_score

    def boost_score(self, amount: float) -> None:
        """Увеличивает релевантность ключевого слова на заданное значение."""
        if amount > 0:
            self.relevance_score += amount

    def reduce_score(self, amount: float) -> None:
        """Уменьшает релевантность ключевого слова на заданное значение, не ниже нуля."""
        if amount > 0:
            self.relevance_score = max(0.0, self.relevance_score - amount)

    def is_significant(self, threshold: float = 0.5) -> bool:
        """Проверяет, превышает ли релевантность заданный порог."""
        return self.relevance_score >= threshold

    def format_for_display(self) -> str:
        """Форматирует ключевое слово для отображения."""
        return f"{self.word} (релевантность: {self.relevance_score:.2f})"

    def to_dict(self) -> dict:
        """Сериализует ключевое слово в словарь."""
        return {
            "word": self.word,
            "relevance_score": self.relevance_score
        }

    def matches(self, text: str) -> bool:
        """Проверяет, встречается ли ключевое слово в заданном тексте."""
        return self.word.lower() in text.lower()

    def is_used_in_document(self, document: "Document") -> bool:
        """Проверяет, встречается ли ключевое слово в заголовке, тегах, заметках или комментариях документа."""
        if self.word.lower() in document.title.lower():
            return True
        if any(self.word.lower() in tag.lower() for tag in document.tags):
            return True
        if document.revisions:
            for rev in document.revisions:
                if rev.notes and self.word.lower() in rev.notes.lower():
                    return True
                if any(self.word.lower() in change.lower() for change in rev.change_history):
                    return True
        if document.comments:
            for comment in document.comments:
                if self.word.lower() in comment.content.lower():
                    return True
        return False

    def link_to_document(self, document: "Document") -> None:
        """Добавляет ключевое слово в документ, если оно ещё не связано."""
        if document.keywords is None:
            document.keywords = []
        if self not in document.keywords:
            document.keywords.append(self)

    def is_used_in_insight(self, insight: "Insight") -> bool:
        """Проверяет, встречается ли ключевое слово в описании инсайта."""
        return self.word.lower() in insight.description.lower()

    def link_to_insight(self, insight: "Insight") -> None:
        """Добавляет ID инсайта в список связанных, если ключевое слово используется в описании."""
        if self.is_used_in_insight(insight):
            if insight.insight_id not in getattr(self, "linked_insights", []):
                if not hasattr(self, "linked_insights"):
                    self.linked_insights = []
                self.linked_insights.append(insight.insight_id)
