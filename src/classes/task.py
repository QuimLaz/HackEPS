from typing import Dict

from src.classes.category import Category


class Task:
    def __init__(self, id: str, completed: bool, category: Category, report_id: str, duration: int, sla: int) -> None:
        self.id: str = id
        self.completed: bool = completed
        self.category: Category = category
        self.report_id: str = report_id
        self.duration: int = duration
        self.sla: int = sla

    @staticmethod
    def from_json(task_map: Dict):
        return Task(task_map['id'], task_map['completed'], Category.from_json(task_map['category']),
                    task_map['reportId'], task_map['duration'], task_map['sla'])

    def to_json(self) -> Dict:
        return {
            'id': self.id,
            'completed': self.completed,
            'category': self.category.to_json(),
            'reportId': self.report_id,
            'duration': self.duration,
            'sla': self.sla
        }
