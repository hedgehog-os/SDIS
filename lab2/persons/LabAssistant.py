from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from experiments_and_equipments.LabRoom import LabRoom
    from experiments_and_equipments.Experiment import Experiment
    from experiments_and_equipments.Device import Device


class LabAssistant:
    def __init__(self,
                 assistant_id: int,
                 fullname: str,
                 email: str,
                 position: str,
                 lab_room: int,
                 equipment_list: List[str] | None = None) -> None:
        self.assistant_id: int = assistant_id
        self.fullname: str = fullname
        self.email: str = email
        self.position: str = position
        self.lab_room: int = lab_room
        self.equipment_list: List[str] = equipment_list or []

    def add_equipment(self, item: str) -> None:
        """Добавляет оборудование в список, если оно ещё не включено."""
        if item and item not in self.equipment_list:
            self.equipment_list.append(item)

    def remove_equipment(self, item: str) -> None:
        """Удаляет оборудование из списка, если оно есть."""
        if item in self.equipment_list:
            self.equipment_list.remove(item)

    def has_equipment(self, item: str) -> bool:
        """Проверяет, есть ли указанное оборудование у ассистента."""
        return item in self.equipment_list

    def count_equipment(self) -> int:
        """Возвращает количество единиц оборудования."""
        return len(self.equipment_list)

    def get_equipment_by_prefix(self, prefix: str) -> List[str]:
        """Фильтрует оборудование по началу названия."""
        return [e for e in self.equipment_list if e.startswith(prefix)]

    def summarize(self) -> str:
        """Форматирует краткую информацию об ассистенте."""
        return (
            f"Ассистент #{self.assistant_id}: {self.fullname}\n"
            f"Email: {self.email}\n"
            f"Должность: {self.position}\n"
            f"Лаборатория: {self.lab_room}\n"
            f"Оборудование: {len(self.equipment_list)} единиц"
        )

    def to_dict(self) -> dict:
        """Сериализует ассистента в словарь."""
        return {
            "assistant_id": self.assistant_id,
            "fullname": self.fullname,
            "email": self.email,
            "position": self.position,
            "lab_room": self.lab_room,
            "equipment_list": self.equipment_list
        }

    def is_assigned_to_room(self, room: "LabRoom") -> bool:
        """Проверяет, прикреплён ли ассистент к указанной лаборатории."""
        return self.lab_room == room.room_number

    def get_room_equipment_overlap(self, room: "LabRoom") -> List[str]:
        """Возвращает список оборудования, которое есть и у ассистента, и в лаборатории."""
        return [item for item in self.equipment_list if any(d.name == item for d in room.equipment)]

    def get_assigned_devices(self, all_devices: List["Device"]) -> List["Device"]:
        """Возвращает список устройств, назначенных ассистенту по названию."""
        return [d for d in all_devices if d.name in self.equipment_list]

    def assist_in_experiment(self, experiment: "Experiment") -> str:
        """Формирует запись об участии ассистента в эксперименте."""
        return (
            f"{self.fullname} ({self.position}) помогал в эксперименте #{experiment.experiment_id} "
            f"с процедурой '{experiment.procedure.name}' начиная с {experiment.start_date.strftime('%Y-%m-%d')}."
        )
