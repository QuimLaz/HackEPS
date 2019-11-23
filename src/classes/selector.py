import numpy as np
from scipy.optimize import minimize


def objective_function_full(parameters: np.array, model, solution):
    count = 0
    for task in model.last_scenario.tasks:
        if task != solution:
            if model.comparison_function(parameters, task, solution) == solution:
                count += 1
    return -count + model.weight*parameters.squared().sum()


class Selector:

    def __init__(self, comparison_function, comparison_parameters, learning_rate, weight):
        self.comparison_function = comparison_function
        self.comparison_parameters = comparison_parameters
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
        self.comparison_parameters = [old+self.learning_rate*new for old, new in
                                      zip(self.comparison_parameters, new_params)]

    def compute_new_params(self, solution_id):
        # find which task is the solution
        for task in self.last_scenario.tasks:
            if task.id == solution_id:
                solution = task

        def objective_function(parameters):
            return objective_function_full(parameters, self, solution)

        return minimize(objective_function, np.array(self.comparison_parameters))

