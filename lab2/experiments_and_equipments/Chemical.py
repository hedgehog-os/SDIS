from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Reaction import Reaction

class Chemical:
    def __init__(self,
                 chemical_id: int,
                 name: str,
                 formula: str,
                 concentration_molar: Optional[float] = None,
                 reactions: Optional[List["Reaction"]] = None) -> None:
        self.chemical_id: int = chemical_id
        self.name: str = name
        self.formula: str = formula
        self.concentration_molar: Optional[float] = concentration_molar

        # Ассоциация
        self.reactions: List["Reaction"] = reactions or []

    def add_reaction(self, reaction: "Reaction") -> None:
        """Добавляет реакцию в список, если она ещё не связана."""
        if reaction not in self.reactions:
            self.reactions.append(reaction)
            if self not in reaction.reactants and self not in reaction.products:
                reaction.reactants.append(self)  # по умолчанию считаем реагентом

    def remove_reaction(self, reaction: "Reaction") -> None:
        """Удаляет реакцию из списка и из объекта реакции."""
        if reaction in self.reactions:
            self.reactions.remove(reaction)
        if self in reaction.reactants:
            reaction.reactants.remove(self)
        if self in reaction.products:
            reaction.products.remove(self)

    def is_reactant_in(self, reaction: "Reaction") -> bool:
        """Проверяет, является ли вещество реагентом в данной реакции."""
        return self in reaction.reactants

    def is_product_in(self, reaction: "Reaction") -> bool:
        """Проверяет, является ли вещество продуктом в данной реакции."""
        return self in reaction.products

    def get_reaction_ids(self) -> List[int]:
        """Возвращает список ID всех связанных реакций."""
        return [r.reaction_id for r in self.reactions]

    def get_reactions_as(self, role: str = "reactant") -> List["Reaction"]:
        """Возвращает реакции, где вещество выступает как реагент или продукт."""
        if role == "reactant":
            return [r for r in self.reactions if self in r.reactants]
        elif role == "product":
            return [r for r in self.reactions if self in r.products]
        else:
            raise ValueError("Роль должна быть 'reactant' или 'product'")

    def summarize(self) -> str:
        """Форматирует краткую информацию о веществе и его реакциях."""
        return (
            f"Chemical #{self.chemical_id}: {self.name} ({self.formula})\n"
            f"Концентрация: {self.concentration_molar or '—'} M\n"
            f"Связанные реакции: {', '.join(map(str, self.get_reaction_ids())) or '—'}"
        )

    def to_dict(self) -> dict:
        """Сериализует химическое вещество в словарь."""
        return {
            "chemical_id": self.chemical_id,
            "name": self.name,
            "formula": self.formula,
            "concentration_molar": self.concentration_molar,
            "reaction_ids": self.get_reaction_ids()
        }

    def get_recent_reactions(self, days: int = 30) -> List["Reaction"]:
        """Возвращает реакции, записанные за последние N дней."""
        from datetime import datetime, timedelta
        threshold = datetime.now() - timedelta(days=days)
        return [r for r in self.reactions if r.recorded_at >= threshold]

    def get_reactions_by_condition(self, keyword: str) -> List["Reaction"]:
        """Возвращает реакции, содержащие ключевое слово в условиях."""
        return [
            r for r in self.reactions
            if r.conditions and keyword.lower() in r.conditions.lower()
        ]

    def visualize_reaction_roles(self) -> str:
        """Генерирует текстовую диаграмму роли вещества в реакциях."""
        reactant_count = len(self.get_reactions_as("reactant"))
        product_count = len(self.get_reactions_as("product"))
        return (
            f"{self.name} ({self.formula})\n"
            f"Реагент: {'|' * min(reactant_count, 20)} ({reactant_count})\n"
            f"Продукт: {'|' * min(product_count, 20)} ({product_count})"
        )

    def get_co_reactants(self) -> List["Chemical"]:
        """Возвращает вещества, участвующие в тех же реакциях как реагенты."""
        co_chemicals = set()
        for r in self.get_reactions_as("reactant"):
            for c in r.reactants:
                if c != self:
                    co_chemicals.add(c)
        return list(co_chemicals)
