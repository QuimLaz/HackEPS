import pickle

from src.api import API
from src.classes.scenario import ScenarioGuess
from src.classes.selectornn import Selector


def save_model(file_name, model):
    with open(file_name, 'wb') as file:
        pickle.dump(model, file)


def main(agent_id):
    # create a selector class
    logs = open('../logs/logs_agent_{}.txt'.format(agent_id), 'w')
    learning_rate = 0.01
    # model = Selector(comparison_using_importance, comparison_parameters, learning_rate, weight)
    model = Selector(learning_rate)
    N = 2500
    hits = 0
    trials = 0
    last_hits = 0
    frequency = 100
    for i in range(N):
        # get one scenario
        sample = API.get_scenario_guess_from_dataset(i, agent_id)
        scenario = sample.scenario
        true_solution_id = sample.task_id
        # make prediction
        prediction = model.predict(scenario)
        # check the prediction and update parameters
        guess = ScenarioGuess(scenario, prediction.id)
        # correct, true_solution_id = API.post_scenario(guess)
        trials += 1
        if true_solution_id == guess.task_id:
            hits += 1
            last_hits += 1
        # new_params = model.compute_new_params(true_solution_id)
        # model.update_params(new_params)
        model.update_params(true_solution_id)
        # save model
        if i % frequency == 0:
            logs.write('Iterations: {}\n'.format(i))
            logs.write('Accuracy (overall): {0:.2f}%\n'.format(hits / trials * 100))
            logs.write('Accuracy (last): {0:.2f}%\n'.format(last_hits / frequency * 100))
            logs.write('--------------------\n')
            last_hits = 0
            file_name = '../models/agent{}/model_iter_{}.mod'.format(agent_id, i)
            save_model(file_name, model)

    API.remove_dataset()


if __name__ == '__main__':
    for agent_id in [1, 2, 3]:
        main(agent_id)
