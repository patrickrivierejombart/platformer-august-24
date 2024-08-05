from utils.utils_2d import Action, Force
from typing import List


def read_configured_actions() -> List[Action]:
    import yaml
    actions_configuration_path = "assets/configurations/actions.yml"
    actions_yaml = None
    with open(actions_configuration_path, 'r') as actions_configuration_file:
        try:
            actions_yaml = yaml.safe_load(actions_configuration_file)
        except Exception:
            raise Exception(f'Configuration file {actions_configuration_file} is either missing or corrupt.')
    if actions_yaml:
        action_list = [
            Action(
                action_name=action_name, 
                vector_list=[
                    Force.from_tuple((actions_yaml[action_name][idx])) 
                    for idx in range(len(actions_yaml[action_name]))
                    ]) 
                for action_name in actions_yaml
                ]
        return action_list
    return list()
