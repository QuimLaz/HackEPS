from typing import Tuple

import requests
import json

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


if __name__ == '__main__':
    sc = API.get_scenario(2)
    print(len(sc.tasks))
    scg = ScenarioGuess(sc, sc.tasks[2].id)
    answer = API.post_scenario(scg)
