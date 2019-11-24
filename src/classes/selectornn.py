import copy
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense

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


class Selector:

    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
        self.last_scenario = None
        self.nn = Sequential()
        self.nn.add(Dense(50, activation='sigmoid', input_shape=(2 * N_INPUTS,)))
        #self.nn.add(Dense(50, activation='relu'))
        self.nn.add(Dense(1, activation='sigmoid'))
        adam = keras.optimizers.Adam(lr=self.learning_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0,
                                     amsgrad=False)
        #self.nn.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
        self.nn.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    def compare(self, task1, task2):
        input_array = np.append(get_parameters(task1), get_parameters(task2)).reshape(2*N_INPUTS, 1).T
        output = self.nn.predict(input_array)
        return task1 if output > 0.5 else task2

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

    def update_params(self, true_solution_id):
        true_solution = [t for t in self.last_scenario.tasks if t.id == true_solution_id][0]
        n = 2 * (len(self.last_scenario.tasks) - 1)
        x_train = np.zeros(shape=(n, 2*N_INPUTS))
        y_train = np.zeros(shape=(n, 1))
        i = 0
        for task in self.last_scenario.tasks:
            if task.id != true_solution.id:
                x_train[i, :] = np.append(get_parameters(true_solution), get_parameters(task))
                y_train[i] = 1
                x_train[i + n//2, :] = np.append(get_parameters(task), get_parameters(true_solution))
                y_train[i + n//2] = 0
                i += 1
        self.nn.fit(x_train, y_train, verbose=0)
