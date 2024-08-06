import pygame
from utils.sprite_utils import import_sprite
from settings import *
from utils import utils_config as cutils


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):  # + sprite_path TODO
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_move = -16
        # player status
        self.life = 5
        self.game_over = False
        self.win = False
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def _import_character_assets(self):
        character_path = "assets/textures/player/"
        self.animations = {
            "idle": [],
            "walk": [],
            "jump": [],
            "fall": [],
            "lose": [],
            "win": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def _animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (35, 50))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        # set the rect (boundary)
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def _get_input(self, player_event):
        if player_event != False:
            if player_event == "right":
                self.direction.x = 1
                self.facing_right = True
            elif player_event == "left":
                self.direction.x = -1
                self.facing_right = False
        else:
            self.direction.x = 0

    def _jump(self):
        self.direction.y = self.jump_move

    def _get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        elif self.direction.x != 0:
            self.status = "walk"
        else:
            self.status = "idle"

    def update(self, player_event):
        self._get_status()
        if self.life > 0 and not self.game_over:
            if player_event == "space" and self.on_ground:
                self._jump()
            else:
                self._get_input(player_event)
        elif self.game_over and self.win:
            self.direction.x = 0
            self.status = "win"
        else:
            self.direction.x = 0
            self.status = "lose"
        self._animate()

class New_Player(Player):
    def __init__(self, pos, action_list):
        super().__init__(pos)
        self.action_list = action_list
    
    def _jump(self, index = 0):
        jump_action: cutils.Action = self.action_list["player_jump"]
        jump_action.trigger()
    
    def _crouch(self, index = 0):
        pass

    def _dash(self, index = 0):
        jump_action: cutils.Action = self.action_list["player_dash"]
        jump_action.trigger()
    
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