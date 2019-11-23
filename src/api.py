import json
import random
from typing import Tuple, List

import requests

from src.classes.evaluation import Evaluations, Evaluation
from src.classes.scenario import Scenario, ScenarioGuess


class API:
    api_key = 'mamamiodqm'
    base_url = 'http://18.184.40.57:9010'
    scenario_url = f'{base_url}/scenario'
    evaluation_url = f'{base_url}/evaluation'
    team_key = f'?teamKey={api_key}'
    dataset = None

    def __init__(self) -> None:
        # Make API class non-instantiable
        raise Exception('API cannot be instantiated')

    @classmethod
    def get_scenario(cls, id: int = 1) -> Scenario:
        id = id if 0 < id < 4 else 2
        response = requests.get(url=f'{cls.scenario_url}/{id}{cls.team_key}')
        scenario_map = response.json()['value']
        return Scenario.from_json(scenario_map)

    @classmethod
    def get_scenario_guess_from_dataset(cls, i) -> ScenarioGuess:
        if cls.dataset is None:
            cls.dataset = cls.get_dataset()
        return cls.dataset[i % len(cls.dataset)]

    @classmethod
    def post_scenario(cls, scenario_guess: ScenarioGuess) -> Tuple[bool, str]:
        response = requests.post(url=f'{cls.scenario_url}{cls.team_key}', data=json.dumps(scenario_guess.to_json()),
                                 headers={'Content-type': 'application/json', 'Accept': 'application/json'}
                                 )
        correct = response.json()['value']
        return scenario_guess.task_id == correct, correct

    @classmethod
    def get_evaluation(cls) -> List[Scenario]:
        response = requests.get(url=f'{cls.evaluation_url}{cls.team_key}')
        scenario_list = response.json()
        return [Scenario.from_json(s) for s in scenario_list]

    @classmethod
    def post_evaluation(cls, evaluations: Evaluations) -> int:
        response = requests.post(url=f'{cls.evaluation_url}{cls.team_key}', data=json.dumps(evaluations.to_json()),
                                 headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        return response.json()['value']

    @classmethod
    def init_ranking(cls) -> int:
        scs = cls.get_evaluation()
        ev = Evaluations([
            Evaluation(
                scenario.scenario_id,
                scenario.uncompleted_tasks[random.randrange(0, len(scenario.uncompleted_tasks))].id
            ) for scenario in scs])
        return cls.post_evaluation(ev)

    @classmethod
    def create_dataset(cls, n: int = 1000) -> None:
        f = open('solutions.json', mode='r', encoding='utf8')
        sols: List = json.loads(f.read())
        f.close()
        for i in range(n):
            try:
                sc = API.get_scenario(0)
            except:
                print('CACA')
            else:
                scg = ScenarioGuess(sc, sc.uncompleted_tasks[0].id)
                _, correct = API.post_scenario(scg)
                scg.task_id = correct
                sols.append(scg.to_json())
                f = open('solutions.json', mode='w', encoding='utf8')
                f.write(json.dumps(sols, indent=4))
                f.close()

    @classmethod
    def get_dataset(cls) -> List[ScenarioGuess]:
        sgs: List[ScenarioGuess] = []
        f = open(f'../data/api-backup1.json', 'r', encoding='utf8')
        sgs += [ScenarioGuess.from_json(s) for s in json.loads(f.read())['assignations']]
        f.close()
        return sgs
