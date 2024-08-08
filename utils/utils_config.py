from utils.utils_2d import Action, Force
from typing import Dict
from pygame.math import Vector2


def read_configured_actions() -> Dict[str, Action]:
    import yaml
    actions_configuration_path = "assets/configurations/actions.yml"
    actions_yaml = None
    with open(actions_configuration_path, 'r') as actions_configuration_file:
        try:
            actions_yaml = yaml.safe_load(actions_configuration_file)
        except Exception:
            raise Exception(f'Configuration file {actions_configuration_file} is either missing or corrupt.')
    if actions_yaml:
        action_list = {
            action_name: Action(
                action_name=action_name,
                vector_list=[
                    Vector2((actions_yaml[action_name][idx]))
                    for idx in range(len(actions_yaml[action_name]))
                    ]
                )
            for action_name in actions_yaml
        }
        return action_list
    return dict()
