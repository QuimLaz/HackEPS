from typing import List

from classes.task import Task


class Scenario:

    def __init__(self, scenario_id: str, tasks: List[Task]):
        self.scenario_id: str = scenario_id
        self.tasks: List[Task] = tasks


class ScenarioGuess:
    def __init__(self, scenario: Scenario, task_id: str) -> None:
        self.scenario: Scenario = scenario
        self.task_id: str = task_id
