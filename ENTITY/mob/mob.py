from utils.utils_2d import Position
import math


class Mob:
    def __init__(self, position: Position):
        self.position = position
    
    def los(self, player_position: Position, threshold: int = 5) -> bool:
        diff_x = player_position.x - self.position.x
        diff_y = player_position.y - self.position.y
        err_player_to_mob = math.sqrt(diff_x**2 + diff_y**2)
        return err_player_to_mob <= threshold
