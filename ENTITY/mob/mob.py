from ENTITY.entity import Entity
from utils.utils_2d import Position
from typing import Literal
import math


class Mob(Entity):
    sprite_path="assets/textures/mob/"

    def _circular_los(self, player_position: Position, threshold: int):
        diff_x = player_position.x - self.position.x
        diff_y = player_position.y - self.position.y
        err_player_to_mob = math.sqrt(diff_x**2 + diff_y**2)
        return err_player_to_mob <= threshold

    def _vertical_los(self, player_position: Position, threshold: int):
        x_offset = self.base_size[0]/2
        return player_position.x >= self.position.x - x_offset and\
            player_position.x <= self.position.x + x_offset and\
            player_position.y >= self.position.y - threshold and\
            player_position.y <= self.position.y + threshold

    def _horizontal_los(self, player_position: Position, threshold: int):
        y_offset = self.base_size[1]/2
        return player_position.x >= self.position.x - threshold and\
            player_position.x <= self.position.x + threshold and\
            player_position.y >= self.position.y - y_offset and\
            player_position.y <= self.position.y + y_offset

    def los(self, player_position: Position, threshold: int = 5, los_type: Literal["circular", "vertical", "horizontal"] = "circular") -> bool:
        if los_type == "circular":
            return self._circular_los(player_position=player_position, threshold=threshold)
        elif los_type == "vertical":
            return self._vertical_los(player_position=player_position, threshold=threshold)
        elif los_type == "horizontal":
            return self._horizontal_los(player_position=player_position, threshold=threshold)
