from src.classes.task import Task
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer


def importance(parameters, task: Task):
    return parameters[0] * task.duration + parameters[1] * task.sla + \
           parameters[2] * task.category.stress_level


def comparison_using_importance(parameters, task1: Task, task2: Task):
    return task1 if importance(parameters, task1) > importance(parameters, task2) else task2


def compair_two_descriptions(descr1, descr2):
    vectorizer = TfidfVectorizer(stop_words='english', min_df=3)
    descr1_values = vectorizer.fit_transform(descr1)
    descr2_values = vectorizer.fit_transform(descr2)
    if (sum(descr1_values) > sum(descr2_values)):
        return sum(descr1_values)
    else:
        return sum(descr2_values)
