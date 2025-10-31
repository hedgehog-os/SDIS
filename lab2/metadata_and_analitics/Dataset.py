from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from documents.Report import Report


class DataSet:
    def __init__(self, dataset_id: int, name: str, source: str, records: List[dict]) -> None:
        self.dataset_id: int = dataset_id
        self.name: str = name
        self.source: str = source
        self.records: List[dict] = records

    def add_record(self, record: dict) -> None:
        """Добавляет новую запись в набор данных."""
        if isinstance(record, dict):
            self.records.append(record)

    def remove_record(self, index: int) -> None:
        """Удаляет запись по индексу."""
        if 0 <= index < len(self.records):
            del self.records[index]

    def get_record_count(self) -> int:
        """Возвращает количество записей."""
        return len(self.records)

    def get_fields(self) -> List[str]:
        """Возвращает список всех уникальных полей, встречающихся в записях."""
        fields = set()
        for record in self.records:
            fields.update(record.keys())
        return list(fields)

    def filter_records(self, field: str, value) -> List[dict]:
        """Возвращает записи, где указанное поле имеет заданное значение."""
        return [r for r in self.records if r.get(field) == value]

    def summarize(self) -> str:
        """Возвращает краткую сводку по набору данных."""
        return (
            f"DataSet #{self.dataset_id} — {self.name}\n"
            f"Источник: {self.source}\n"
            f"Записей: {self.get_record_count()}\n"
            f"Поля: {', '.join(self.get_fields())}"
        )

    def to_dict(self) -> dict:
        """Сериализует набор данных в словарь."""
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "source": self.source,
            "records": self.records
        }

    def contains_field(self, field: str) -> bool:
        """Проверяет, есть ли указанное поле хотя бы в одной записи."""
        return any(field in r for r in self.records)

    def export_as_csv_text(self) -> str:
        """Возвращает данные в виде CSV-совместимого текста."""
        if not self.records:
            return "Нет данных для экспорта."
        fields = self.get_fields()
        lines = [",".join(fields)]
        for record in self.records:
            row = [str(record.get(field, "")) for field in fields]
            lines.append(",".join(row))
        return "\n".join(lines)

    def aggregate_field(self, field: str) -> dict[str, float]:
        """Выполняет базовую агрегацию: сумма, среднее, максимум, минимум."""
        values = [r[field] for r in self.records if isinstance(r.get(field), (int, float))]
        if not values:
            return {"sum": 0, "avg": 0, "max": 0, "min": 0}
        return {
            "sum": sum(values),
            "avg": sum(values) / len(values),
            "max": max(values),
            "min": min(values)
        }
    
    def to_chart_data(self, x_field: str, y_field: str) -> dict:
        """Генерирует словарь данных для построения диаграммы."""
        chart_data = {}
        for record in self.records:
            x = record.get(x_field)
            y = record.get(y_field)
            if isinstance(x, str) and isinstance(y, (int, float)):
                chart_data[x] = y
        return chart_data

    def attach_to_report(self, report: "Report", chart_title: str, chart_type: str, x_field: str, y_field: str) -> None:
        """Создаёт диаграмму из набора данных и добавляет её в отчёт."""
        from Chart import Chart  # локальный импорт для избежания циклической зависимости
        chart_data = self.to_chart_data(x_field, y_field)
        if chart_data:
            chart = Chart(
                chart_id=len(report.charts) + 1,
                title=chart_title,
                chart_type=chart_type,
                data=chart_data
            )
            report.charts.append(chart)

