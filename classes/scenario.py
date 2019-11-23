class Scenario:

    def __init__(self, scenario_id, tasks):
        self.scenario_id = scenario_id
        self.tasks = tasks


class ScenarioGuess:
    def __init__(self, scenario, task_id) -> None:
        self.scenario = scenario
        self.task_id = task_id
