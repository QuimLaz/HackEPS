from src.classes.task import Task


def importance(parameters, task: Task):
    return parameters[0] * task.duration + parameters[1] * task.sla + \
           parameters[2] * task.category.stress_level


def comparison_using_importance(parameters, task1: Task, task2: Task):
    return task1 if importance(parameters, task1) > importance(parameters, task2) else task2

