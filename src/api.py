from typing import Tuple, List

import requests
import json

from src.classes.evaluation import Evaluations, Evaluation
from src.classes.scenario import Scenario, ScenarioGuess


class API:
    api_key = 'mamamiodqm'
    base_url = 'http://18.184.40.57:9010'
    scenario_url = f'{base_url}/scenario'
    evaluation_url = f'{base_url}/evaluation'
    team_key = f'?teamKey={api_key}'

    @classmethod
    def get_scenario(cls, id: int) -> Scenario:
        response = requests.get(url=f'{cls.scenario_url}/{id}{cls.team_key}')
        scenario_map = response.json()['value']
        return Scenario.from_json(scenario_map)

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


if __name__ == '__main__':
    scs = API.get_evaluation()
    ev = Evaluations([Evaluation(s.scenario_id, s.tasks[2].id) for s in scs])
    score = API.post_evaluation(ev)
    print(score)