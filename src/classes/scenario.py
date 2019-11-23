from typing import List, Dict

from src.classes.task import Task


class Scenario:

    def __init__(self, scenario_id: str, tasks: List[Task], agent_id: str):
        self.scenario_id: str = scenario_id
        self.tasks: List[Task] = tasks
        self.agent_id: str = agent_id

    @staticmethod
    def from_json(scenario_map: Dict):
        return Scenario(scenario_map['scenarioId'], [Task.from_json(tj) for tj in scenario_map['tasks']], scenario_map['agentId'])

    def to_json(self):
        return {
            'scenarioId': self.scenario_id,
            'tasks': [t.to_json() for t in self.tasks],
            'agentId': self.agent_id
        }


class ScenarioGuess:
    def __init__(self, scenario: Scenario, task_id: str) -> None:
        self.scenario: Scenario = scenario
        self.task_id: str = task_id

    def to_json(self) -> Dict:
        return {
            'scenario': self.scenario.to_json(),
            'taskId': self.task_id
        }
