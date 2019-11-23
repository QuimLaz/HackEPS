from typing import List, Dict


class Evaluation:

    def __init__(self, scenario_id: str, task_id: str) -> None:
        self.scenario_id: str = scenario_id
        self.task_id: str = task_id

    def to_json(self) -> Dict:
        return {
            'scenarioId': self.scenario_id,
            'taskId': self.scenario_id
        }


class Evaluations:

    def __init__(self, evaluations: List[Evaluation]) -> None:
        self.evaluations: List[Evaluation] = evaluations

    def to_json(self) -> Dict:
        return {
            'evaluations': [e.to_json() for e in self.evaluations]
        }
