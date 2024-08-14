from ENTITY.entity import PhysicsEntity
from typing import Literal, Tuple
import math


class Mob(PhysicsEntity):
    sprite_path="assets/textures/mob/"

    def _circular_los(self, player_position: Tuple[int, int], threshold: int):
        diff_x = player_position[0] - self.position_int[0]
        diff_y = player_position[1] - self.position_int[1]
        err_player_to_mob = math.sqrt(diff_x**2 + diff_y**2)
        return err_player_to_mob <= threshold

    def _vertical_los(self, player_position: Tuple[int, int], threshold: int):
        x_offset = self.base_size[0]/2
        return player_position[0] >= self.position_int[0] - x_offset and\
            player_position[0] <= self.position_int[0] + x_offset and\
            player_position[1] >= self.position_int[1] - threshold and\
            player_position[1] <= self.position_int[1] + threshold

    def _horizontal_los(self, player_position: Tuple[int, int], threshold: int):
        y_offset = self.base_size[1]/2
        return player_position[0] >= self.position_int[0] - threshold and\
            player_position[0] <= self.position_int[0] + threshold and\
            player_position[1] >= self.position_int[1] - y_offset and\
            player_position[1] <= self.position_int[1] + y_offset

    def los(self, player_position: Tuple[int, int], threshold: int = 5, los_type: Literal["circular", "vertical", "horizontal"] = "circular") -> bool:
        if los_type == "circular":
            return self._circular_los(player_position=player_position, threshold=threshold)
        elif los_type == "vertical":
            return self._vertical_los(player_position=player_position, threshold=threshold)
        elif los_type == "horizontal":
            return self._horizontal_los(player_position=player_position, threshold=threshold)
