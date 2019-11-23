from src.classes.task import Task
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer


def importance(parameters, task: Task):
    return parameters[0] * task.duration + parameters[1] * task.sla + \
           parameters[2] * task.category.stress_level


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
