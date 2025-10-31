from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Chemical import Chemical


class Sample:
    def __init__(self, sample_id: int, chemical: "Chemical", volume_ml: float) -> None:
        self.sample_id: int = sample_id
        self.chemical: "Chemical" = chemical
        self.volume_ml: float = volume_ml

    def get_concentration(self) -> Optional[float]:
        """Возвращает молярную концентрацию вещества, если она известна."""
        return self.chemical.concentration_molar

    def get_moles(self) -> Optional[float]:
        """Вычисляет количество молей вещества в образце."""
        if self.chemical.concentration_molar is not None:
            return self.chemical.concentration_molar * (self.volume_ml / 1000)
        return None

    def describe(self) -> str:
        """Форматирует краткое описание образца."""
        moles = self.get_moles()
        moles_str = f"{moles:.4f} моль" if moles is not None else "—"
        return (
            f"Образец #{self.sample_id}\n"
            f"Вещество: {self.chemical.name} ({self.chemical.formula})\n"
            f"Объём: {self.volume_ml:.2f} мл\n"
            f"Концентрация: {self.chemical.concentration_molar or '—'} M\n"
            f"Количество вещества: {moles_str}"
        )

    def to_dict(self) -> dict:
        """Сериализует образец в словарь."""
        return {
            "sample_id": self.sample_id,
            "chemical_id": self.chemical.chemical_id,
            "chemical_name": self.chemical.name,
            "formula": self.chemical.formula,
            "volume_ml": self.volume_ml,
            "concentration_molar": self.chemical.concentration_molar,
            "moles": self.get_moles()
        }

    def is_same_chemical(self, other: "Sample") -> bool:
        """Проверяет, содержит ли другой образец то же вещество."""
        return self.chemical.chemical_id == other.chemical.chemical_id
