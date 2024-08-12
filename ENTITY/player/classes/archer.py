

from ENTITY.player.player import Player
from pygame.math import Vector2




class Archer(Player):
    def __init__(self, player_pos: Vector2,arrow_pos: Vector2):
        super().__init__()
        self.arrow_pos = arrow_pos
        self.player_pos = player_pos

    def arrow_shoot(self):
        self.arrow_pos = self.player_pos