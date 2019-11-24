from src.api import API


def count_types():
    types = set()
    for i in range(50000):
        scenario_guess = API.get_scenario_guess_from_dataset(i)
        for task in scenario_guess.scenario.tasks:
            if task.category.type not in types:
                types.add(task.category.type)
    print('Number of types is: {}'.format(len(types)))


if __name__ == '__main__':
    count_types()
