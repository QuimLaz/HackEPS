from classes.category import Category


class Task:
    def __init__(self, id: str, completed: bool, category: Category, report_id: str, duration: int, sla: int) -> None:
        self.id: str = id
        self.completed: bool = completed
        self.category: Category = category
        self.report_id: str = report_id
        self.duration: int = duration
        self.sla: int = sla
