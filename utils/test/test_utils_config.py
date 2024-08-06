from utils.utils_config import read_configured_actions


if __name__ == "__main__":
    action_list = read_configured_actions()
    for action in action_list:
        action.trigger()
        while action.action_list:
            print(action.play().vector)
            action.trigger()
