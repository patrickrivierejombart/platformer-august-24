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

    def _crouch(self, index = 0):
        pass

    def _dash(self, index = 0):
        pass # Dash (misc)
    
    def _arrowShoot(self, index = 0):
        pass # Shoot an arrow (far combat)
    
    def _dobbleJump(self, index = 0):
        pass # Do a second jump in the air (misc)
    
    def _swift(self, index = 0):
        pass # Get faster (misc)
    
    def _windUpdraft(self, index = 0):
        pass # Get launched in the air with wind (misc)

    def _windTornadoSelf(self, index = 0):
        pass # Protect yourself with a tornado (defense)
    
    def _windTornadoEnemy(self, index = 0):
        pass # Launch the enemy in the air (far combat)

    def _windGust(self, index = 0):
        pass # Launch a powerful wind gust straight to the enemy (far combat)
    
    def _firePunch(self, index = 0):
        pass # Give your opponent a big fire punch (close combat)
    
    def _fireSpeedBoost(self, index = 0):
        pass # Get propusled forward for some time with fire (misc)
    
    def _fireBall(self, index = 0):
        pass # Launch a big fireball to your enemy, size and power depends on your level (far combat)
    
    def _fireUpdraft(self, index = 0):
        pass # Get a little height boost (misc)
    
    def _fireCook(self, index = 0):
        pass # Cook your food to restore more of your stamina (misc)
    
    def _waterNegateFire(self, index = 0):
        pass # You can remove fire from: enemies, building, trees and maybe more (misc)
    
    def _waterBubbleProtect(self, index = 0):
        pass # You can protect yourself with a bubble, not very effective against fire attacks (defense)
    
    def _waterBubbleResp(self, index = 0):
        pass # You can breath under water (misc)

    def _waterArrow(self, index = 0):
        pass # You can launch a powerful water arrow to your enemy (far combat)

    def _waterBubbleChoke(self, index = 0):
        pass # You can choke your enemy by puting a water bubble on his head (far combat)

    def _earthWall(self):
        pass # You can protect yourself with an earth wall (defense)

    def _earthSpike(self):
        pass # You can launch a powerful earth spike to your enemy, takes a lot of time to charge (far combat)

    def _earthHammer(self):
        pass # You can hit your enemy with an earth hammer, temporarly stuns them and deals them damage (close combat)

    def _earthRestrain(self):
        pass # You can restrain your enemy movement (defense/far combat)

    def _swordsmanDownSlash(self):
        pass # Do a powerful downslash towards your enemy (close and far combat)

    def _swordsmanParry(self):
        pass # Parry an enemy attack (defense)

    def _swordsmanDropDown(self):
        pass # Jump from a high place to fall on your enemy with your sword (close combat)

    def _swordsmanNormalAttack(self):
        pass # Attack your enemy with your sword (close combat)

    def _ninjaLurk(self):
        pass # Get unoticed by eveyone (misc)

    def _ninjaRapidSlash(self):
        pass # Jump and propulse yourself towards your enemy to slash them (close combat)

    def _ninjaKnifeThrow(self):
        pass # Throw your knife towards your enemy (fara combat)

    def _ninjaSwift(self):
        pass # Be faster for a certain time (misc)

    def _ninjaHighJump(self):
        pass # Jump higher for a certain time (misc)

    def _healerSelfHeal(self):
        pass # Heal yourself (misc)

    def _healerHeal(self):
        pass # Heal anyone (misc)

    def _healerLifeSteal(self):
        pass # Steal your enemy's hp (far combat)

    def _healerBarrier(self):
        pass # Deploy a magic barrier to defend yourself (defense)

    def _healerSwift(self):
        pass # Get faster for a short time (misc)

    def _healerWandPunch(self):
        pass # Punch your enemy with your wand imbued with mana, deals a little damage but propulse your enemy (close combat)

    def _alchimistPoison(self):
        pass # Launch a powder to poison everyone that's inside (far combat)

    def _alchimistZap(self):
        pass # Launch a powder to zap everyone that's inside (far combat)

    def _alchimistHeal(self):
        pass # Launch a powder to heal everyone that's inside (misc)

    def _alchimistWeaken(self):
        pass # Launch a powder to weaken everyone that's inside (debuff)

    def _alchimistResistance(self):
        pass # Launch a powder to buff with resistence everyone that's inside (buff)

    def _alchimistSpeed(self):
        pass # Launch a powder to buff with speed everyone that's inside (buff)

    def _alchimistSleep(self):
        pass # Launch a powder to put to sleep everyone that's inside (misc)

    def _alchimistParalize(self):
        pass # Launch a powder to paralize everyone that's inside (misc)

    def _alchimistRecoltFlowerPowder(self):
        pass # Recolt flower powder to be able to use your abilities (misc)

    def _alchimistCook(self):
        pass # You are a better cook (passive)
    


# archer, mage, épeiste, ninja, soigneur, alchimiste, 
# item: morph, fly