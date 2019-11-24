from sklearn.feature_extraction.text import TfidfVectorizer

from src.classes.task import Task


def importance(parameters, task: Task):
    # there are only 2 types of tasks
    type_weight = parameters[0] if task.category.type == 0 else parameters[1]
    if task.category.stress_level == 1:
        stress_level_weight = parameters[2]
    elif task.category.stress_level == 2:
        stress_level_weight = parameters[3]
    elif task.category.stress_level == 3:
        stress_level_weight = parameters[4]
    return parameters[5] * task.duration + parameters[6] * task.sla + \
           parameters[7] * task.category.stress_level + type_weight + stress_level_weight


def comparison_using_importance(parameters, task1: Task, task2: Task):
    return task1 if importance(parameters, task1) > importance(parameters, task2) else task2


def value_description(description: str) -> float:
    vectorizer = TfidfVectorizer(stop_words='english', min_df=3)
    return sum(vectorizer.fit_transform(description))


def importance_with_description(parameters, task: Task):
    return parameters[0] * task.duration + parameters[1] * task.sla + \
           parameters[2] * task.category.stress_level + parameters[3] * value_description(
        task.category.description)


def comparison_using_importance_and_description(parameters, task1: Task, task2: Task):
    return task1 if importance_with_description(parameters, task1) > importance_with_description(parameters,
                                                                                                 task2) else task2
