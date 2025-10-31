from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Chemical import Chemical


class Reaction:
    def __init__(self,
                 reaction_id: int,
                 description: str,
                 reactants: Optional[List["Chemical"]] = None,
                 products: Optional[List["Chemical"]] = None,
                 conditions: Optional[str] = None,
                 recorded_at: Optional[datetime] = None) -> None:
        self.reaction_id: int = reaction_id
        self.description: str = description
        self.reactants: List["Chemical"] = reactants or []
        self.products: List["Chemical"] = products or []
        self.conditions: Optional[str] = conditions
        self.recorded_at: datetime = recorded_at or datetime.now()

    def add_reactant(self, chemical: "Chemical") -> None:
        """Добавляет вещество в список реагентов, если оно ещё не включено."""
        if chemical not in self.reactants:
            self.reactants.append(chemical)
            chemical.add_reaction(self)

    def add_product(self, chemical: "Chemical") -> None:
        """Добавляет вещество в список продуктов, если оно ещё не включено."""
        if chemical not in self.products:
            self.products.append(chemical)
            chemical.add_reaction(self)

    def remove_chemical(self, chemical: "Chemical") -> None:
        """Удаляет вещество из реагентов и продуктов, если оно связано."""
        if chemical in self.reactants:
            self.reactants.remove(chemical)
        if chemical in self.products:
            self.products.remove(chemical)
        if self in chemical.reactions:
            chemical.reactions.remove(self)

    def involves_chemical(self, chemical: "Chemical") -> bool:
        """Проверяет, участвует ли вещество в реакции как реагент или продукт."""
        return chemical in self.reactants or chemical in self.products

    def get_all_chemicals(self) -> List["Chemical"]:
        """Возвращает все вещества, участвующие в реакции."""
        return list(set(self.reactants + self.products))

    def summarize(self) -> str:
        """Форматирует краткое описание реакции."""
        reactant_names = ', '.join(c.name for c in self.reactants) or '—'
        product_names = ', '.join(c.name for c in self.products) or '—'
        return (
            f"🧪 Reaction #{self.reaction_id}\n"
            f"Описание: {self.description}\n"
            f"Реагенты: {reactant_names}\n"
            f"Продукты: {product_names}\n"
            f"Условия: {self.conditions or '—'}\n"
            f"Дата: {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
        )

    def to_dict(self) -> dict:
        """Сериализует реакцию в словарь."""
        return {
            "reaction_id": self.reaction_id,
            "description": self.description,
            "reactants": [c.chemical_id for c in self.reactants],
            "products": [c.chemical_id for c in self.products],
            "conditions": self.conditions,
            "recorded_at": self.recorded_at.isoformat()
        }

    def is_recent(self, days: int = 30) -> bool:
        """Проверяет, была ли реакция записана в последние N дней."""
        from datetime import datetime, timedelta
        return self.recorded_at >= datetime.now() - timedelta(days=days)

    def contains_formula(self, formula: str) -> bool:
        """Проверяет, участвует ли вещество с заданной формулой в реакции."""
        return any(c.formula == formula for c in self.get_all_chemicals())
