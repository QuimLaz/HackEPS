class Task:
    def __init__(self, id, completed, category, report_id, duration, sla) -> None:
        self.id = id
        self.completed = completed
        self.category = category
        self.report_id = report_id
        self.duration = duration
        self.sla = sla
