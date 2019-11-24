import pickle

from src.api import API
from src.classes.scenario import ScenarioGuess
from src.classes.selector import Selector
from src.classes.comparison_functions import comparison_using_importance
from src.classes.comparison_functions import comparison_using_importance_and_description

def save_model(file_name, model):
    with open(file_name, 'wb') as file:
        pickle.dump(model, file)


def main():
    # create a selector class
    comparison_parameters = [1, 1, 1, 1]
    learning_rate = 0.05
    weight = 0.1
    model = Selector(comparison_using_importance_and_description, comparison_parameters, learning_rate, weight)
    N = 10000
    hits = 0
    last_hits = 0
    frequency = 100
    for i in range(1, N + 1):
        # get one scenario
        sample = API.get_scenario_guess_from_dataset(i)
        scenario = sample.scenario
        true_solution_id = sample.task_id
        # make prediction
        prediction = model.predict(scenario)
        # check the prediction and update parameters
        guess = ScenarioGuess(scenario, prediction.id)
        # correct, true_solution_id = API.post_scenario(guess)
        if true_solution_id == guess.task_id:
            hits += 1
            last_hits += 1
        new_params = model.compute_new_params(true_solution_id)
        model.update_params(new_params)
        # save model
        if i % frequency == 0:
            print('Iterations: {}'.format(i))
            print('Accuracy (overall): {0:.2f}%'.format(hits/i*100))
            print('Accuracy (last): {0:.2f}%'.format(last_hits/frequency*100))
            print('--------------------')
            last_hits = 0
            file_name = '../models/model_v1.mod'
            save_model(file_name, model)


if __name__ == '__main__':
    main()
