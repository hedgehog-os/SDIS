from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Report import Report


class Chart:

    chart_types = {
        'bar', 'line', 'pie', 'scatter',
        'histogram', 'area', 'bubble',
        'heatmap', 'radar', 'boxplot'
    }

    def __init__(self, chart_id: int, title: str, chart_type: str, data: dict) -> None:
        self.chart_id: int = chart_id
        self.title: str = title
        self.chart_type: str = chart_type
        self.data: dict = data

    @property
    def chart_type(self):
        return self._chart_type

    @chart_type.setter
    def chart_type(self, value):
        if value not in self.chart_types:
            raise ValueError(f'Недопустимый статус: {value}')
        self._chart_type = value

    def update_data(self, new_data: dict) -> None:
        """Обновляет данные диаграммы."""
        if isinstance(new_data, dict):
            self.data = new_data

    def add_data_point(self, key: str, value: float | int) -> None:
        """Добавляет одну точку данных в диаграмму."""
        self.data[key] = value

    def remove_data_point(self, key: str) -> None:
        """Удаляет точку данных по ключу."""
        if key in self.data:
            del self.data[key]

    def get_data_summary(self) -> str:
        """Возвращает краткую сводку по данным диаграммы."""
        if not self.data:
            return "Данные отсутствуют."
        return "\n".join(f"{k}: {v}" for k, v in self.data.items())

    def get_chart_info(self) -> str:
        """Возвращает описание диаграммы."""
        return (
            f"Диаграмма #{self.chart_id}\n"
            f"Название: {self.title}\n"
            f"Тип: {self.chart_type}\n"
            f"Точек данных: {len(self.data)}"
        )

    def is_empty(self) -> bool:
        """Проверяет, содержит ли диаграмма данные."""
        return not bool(self.data)

    def get_max_value(self) -> float | int | None:
        """Возвращает максимальное значение среди данных."""
        if not self.data:
            return None
        return max(self.data.values())

    def get_min_value(self) -> float | int | None:
        """Возвращает минимальное значение среди данных."""
        if not self.data:
            return None
        return min(self.data.values())

    def export_as_text(self) -> str:
        """Возвращает текстовое представление диаграммы."""
        lines = [
            f"Диаграмма #{self.chart_id}",
            f"Название: {self.title}",
            f"Тип: {self.chart_type}",
            "Данные:"
        ]
        lines += [f"- {k}: {v}" for k, v in self.data.items()]
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Преобразует диаграмму в словарь."""
        return {
            "chart_id": self.chart_id,
            "title": self.title,
            "chart_type": self.chart_type,
            "data": self.data
        }

    def attach_to_report(self, report: "Report") -> None:
        """Добавляет диаграмму в отчёт, если она ещё не включена."""
        if self not in report.charts:
            report.charts.append(self)

    def summarize(self) -> str:
        """Возвращает краткую сводку по диаграмме."""
        return (
            f"{self.title} ({self.chart_type}) — "
            f"{len(self.data)} точек, макс: {self.get_max_value()}, мин: {self.get_min_value()}"
        )
