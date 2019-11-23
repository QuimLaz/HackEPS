from typing import List


class Evaluation:

    def __init__(self, scenario_id: str, task_id: str) -> None:
        self.scenarioId: str = scenario_id
        self.taskId: str = task_id


class Evaluations:

    def __init__(self, evaluations: List[Evaluation]) -> None:
        self.evaluations: List[Evaluation] = evaluations
