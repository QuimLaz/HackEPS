import json
import random
import sys

from src.classes.scenario import Scenario
from src.classes.task import Task


def select_next_task(sc: Scenario) -> Task:
    report_ids = {}
    for t in sc.completed_tasks:
        try:
            report_ids[t.report_id] += 1
        except KeyError:
            report_ids[t.report_id] = 1
    report_id_with_least_completed_tasks = min(report_ids.keys(), key=(lambda k: report_ids[k]))
    min_stress_level_task = min(sc.uncompleted_tasks, key=(lambda task: task.category.stress_level))
    report_tasks = [t for t in sc.uncompleted_tasks if t.report_id == report_id_with_least_completed_tasks]
    return min_stress_level_task if len(report_tasks) == 0 else random.choice(report_tasks)


if __name__ == '__main__':
    path = sys.argv[1]
    file = open(path, mode='r', encoding='utf8')
    scenario: Scenario = Scenario.from_json(json.loads(file.read()))
    file.close()
    guess = select_next_task(scenario)
    print(guess.id)
