from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.Device import Device
    from documents.Document import Document
    from documents.Revision import Revision
    from documents.Report import Report
    from metadata_and_analitics.Comment import Comment


class Calibration:
    def __init__(self,
                 calibration_id: int,
                 date: datetime,
                 technician: str,
                 notes: str) -> None:
        self.calibration_id: int = calibration_id
        self.date: datetime = date
        self.technician: str = technician
        self.notes: str = notes

    def update_notes(self, new_notes: str) -> None:
        """Обновляет текст заметок по калибровке."""
        if isinstance(new_notes, str) and new_notes.strip():
            self.notes = new_notes

    def reschedule(self, new_date: datetime) -> None:
        """Переносит дату калибровки."""
        if new_date > datetime.now():
            self.date = new_date

    def is_recent(self, threshold_days: int = 30) -> bool:
        """Проверяет, была ли калибровка проведена недавно."""
        return (datetime.now() - self.date).days <= threshold_days

    def format_for_display(self) -> str:
        """Форматирует калибровку для отображения."""
        return (
            f"Калибровка #{self.calibration_id}\n"
            f"Дата: {self.date.strftime('%Y-%m-%d')}\n"
            f"Техник: {self.technician}\n"
            f"Заметки: {self.notes or '—'}"
        )

    def to_dict(self) -> dict:
        """Сериализует калибровку в словарь."""
        return {
            "calibration_id": self.calibration_id,
            "date": self.date.isoformat(),
            "technician": self.technician,
            "notes": self.notes
        }

    def is_assigned_to(self, technician_name: str) -> bool:
        """Проверяет, назначена ли калибровка указанному технику."""
        return self.technician.lower() == technician_name.lower()

    def link_to_device(self, device: "Device") -> None:
        """Привязывает калибровку к устройству."""
        if not hasattr(device, "calibrations"):
            device.calibrations = []
        if self not in device.calibrations:
            device.calibrations.append(self)

    def is_for_device(self, device: "Device") -> bool:
        """Проверяет, относится ли калибровка к данному устройству."""
        return hasattr(device, "calibrations") and self in device.calibrations

    def attach_to_document(self, document: "Document") -> None:
        """Добавляет заметку о калибровке в документ."""
        from documents.Revision import Revision  # локальный импорт
        note: str = f"Калибровка #{self.calibration_id} от {self.date.strftime('%Y-%m-%d')} — техник: {self.technician}"
        if not hasattr(document, "revisions"):
            document.revisions = []
        revision: "Revision" = Revision(
            revision_id=len(document.revisions) + 1,
            document_id=document.document_id,
            author_id=0,
            timestamp=self.date,
            notes=note,
            change_history=[]
        )
        document.revisions.append(revision)

    def contribute_to_report(self, report: "Report") -> None:
        """Добавляет информацию о калибровке в отчёт."""
        from metadata_and_analitics.Comment import Comment  # локальный импорт
        summary: str = (
            f"Калибровка #{self.calibration_id} выполнена {self.date.strftime('%Y-%m-%d')} "
            f"техником {self.technician}. Заметки: {self.notes}"
        )
        comment: "Comment" = Comment(
            comment_id=len(report.comments) + 1,
            document_id=report.report_id,
            user_id=report.author_id,
            content=summary,
            posted_at=datetime.now()
        )
        report.comments.append(comment)
