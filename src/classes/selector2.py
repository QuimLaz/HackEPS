import copy
import numpy as np
from scipy.optimize import minimize
from src.classes.task import Task

TYPES = [0, 1]
DESCRIPTIONS = ["Waste time on daily meeting", "StackOverflow research", "Train neural network", "Scan brain",
                "Copy and Paste from Kaggle", "Try Support Vector Machine for lulz", "Work remote",
                "Build neural network"]
STRESS_LEVELS = [1, 2, 3]

# we also add completed and duration
N_INPUTS = len(TYPES) + len(DESCRIPTIONS) + len(STRESS_LEVELS) + 2

MAX_DISTANCE = 350.0


def get_parameters(task: Task):
    input_vector = np.zeros(N_INPUTS)
    input_vector[TYPES.index(task.category.type)] = 1
    input_vector[DESCRIPTIONS.index(task.category.description) + len(TYPES)] = 1
    input_vector[STRESS_LEVELS.index(task.category.stress_level) + len(TYPES) + len(DESCRIPTIONS)] = 1
    if not task.completed:
        input_vector[len(TYPES) + len(DESCRIPTIONS) + len(STRESS_LEVELS)] = 1
    input_vector[-1] = task.duration/MAX_DISTANCE
    return input_vector


def linear_comparison(parameters, task1: Task, task2: Task):
    if task1.completed:
        return task2
    return task1 if np.dot(parameters, get_parameters(task1)) > np.dot(parameters, get_parameters(task2)) else task2


def objective_function_full(parameters: np.array, model, solution):
    count = 0
    for task in model.last_scenario.tasks:
        if task != solution:
            if model.comparison_function(parameters, task, solution) == solution:
                count += 1
    return -count + model.weight*np.square(parameters).sum()


class Selector:

    def __init__(self, learning_rate, weight):
        self.comparison_function = linear_comparison
        self.comparison_parameters = np.ones(N_INPUTS)
        self.learning_rate = learning_rate
        self.last_scenario = None
        self.weight = weight

    def compare(self, task1, task2):
        return self.comparison_function(self.comparison_parameters, task1, task2)

    def predict(self, scenario):
        self.last_scenario = scenario
        # compare all tasks with each other and count the wins of each one
        count = [0 for task in scenario.tasks]
        for i, task1 in enumerate(scenario.tasks):
            for j, task2 in enumerate(scenario.tasks):
                if i < j:
                    if self.compare(task1, task2) == task1:
                        count[i] += 1
                    else:
                        count[j] += 1
        # predict the task that has one more comparisons
        return scenario.tasks[count.index(max(count))]

    def update_params(self, new_params):
        self.comparison_parameters = self.comparison_parameters + self.learning_rate*new_params

    def compute_new_params(self, solution_id):
        # find which task is the solution
        for task in self.last_scenario.tasks:
            if task.id == solution_id:
                solution = task

        def objective_function(parameters):
            return objective_function_full(parameters, self, solution)

        result_opt = minimize(objective_function, np.array(self.comparison_parameters))
        new_params = copy.deepcopy(result_opt['x'])
        return new_params
