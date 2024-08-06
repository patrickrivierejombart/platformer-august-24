from utils.utils_config import read_configured_actions


if __name__ == "__main__":
    action_list = read_configured_actions()
    for action_name in action_list:
        action_list[action_name].trigger()
        while action_list[action_name].action_list:
            print(action_list[action_name].play().vector)
            action_list[action_name].trigger()
