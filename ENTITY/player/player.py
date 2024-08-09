from utils.sprite_utils import import_sprite
from ENTITY.entity import Entity
from settings import PLAYER_JUMP, PLAYER_WALK_RIGHT, PLAYER_WALK_LEFT, STOP_PLAYER_JUMP, STOP_PLAYER_WALK_RIGHT, STOP_PLAYER_WALK_LEFT


class Player(Entity):
    sprite_path="assets/textures/player/"

    def _import_character_assets(self, sprite_path):
        """REDEFINE IN HERITAGE : use self.animations"""
        character_path = sprite_path
        self.animations = {
            "fall": [],
            "idle": [],
            "jump": [],
            "lose": [],
            "walk": [],
            "win": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def _get_status(self):
        # Get player active status
        if self.velocity.y < 0:
            self.status = "jump"
        elif self.velocity.x != 0:
            self.status = "walk"
        elif not self.on_ground:
            self.status = "fall"
        else:
            self.status = "idle"

    def _jump(self, do_jump: bool):
        # Player jump if on_ground
        if not self.on_ground:
            return
        if do_jump and not self.status == "jump":
            self.velocity_goal.y = -self.jump

    def _walk_right(self, do_walk_right: bool):
        # Walk and face right
        if do_walk_right:
            self.facing_right = True
            self.velocity_goal.x = self.speed
        elif self.velocity_goal.x > 0:
            self.velocity_goal.x = 0

    def _walk_left(self, do_walk_left: bool):
        # Walk and face left
        if do_walk_left:
            self.facing_right = False
            self.velocity_goal.x = -self.speed
        elif self.velocity_goal.x < 0:
            self.velocity_goal.x = 0

    def _act(self, event):
        if self.status == "dead":  # if dead, don't act
            return
        # ACT
        if event == PLAYER_JUMP:
            self._jump(True)
        if event == PLAYER_WALK_RIGHT:
            self._walk_right(True)
        if event == PLAYER_WALK_LEFT:
            self._walk_left(True)
        # STOP ACTING
        if event == STOP_PLAYER_JUMP:
            self._jump(False)
        if event == STOP_PLAYER_WALK_RIGHT:
            self._walk_right(False)
        if event == STOP_PLAYER_WALK_LEFT:
            self._walk_left(False)
