from utils.texture_utils import import_sprite
from ENTITY.entity import PhysicsEntity
from settings import PLAYER_JUMP, PLAYER_WALK_RIGHT, PLAYER_WALK_LEFT, STOP_PLAYER_JUMP, STOP_PLAYER_WALK_RIGHT, STOP_PLAYER_WALK_LEFT


class Player(PhysicsEntity):
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
        if self.velocity_float[1] < 0:
            self.status = "jump"
        elif self.velocity_float[0] != 0 and self.collisions['down']:
            self.status = "walk"
        elif not self.collisions['down']:
            self.status = "fall"
        else:
            self.status = "idle"

    def _jump(self, do_jump: bool):
        # Player jump if on_ground
        if not self.collisions['down']:
            return
        if do_jump:
            self.velocity_goal_float[1] = - do_jump * self.jump
    
    def _crouch(self, do_crouch: bool):
        self.moving_y[1] = do_crouch

    def _walk_right(self, do_walk_right: bool):
        self.moving_x[1] = do_walk_right

    def _walk_left(self, do_walk_left: bool):
        self.moving_x[0] = do_walk_left

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
        
        self.velocity_goal_float[0] = (self.moving_x[1] - self.moving_x[0]) * self.speed
