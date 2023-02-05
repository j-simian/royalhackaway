import pygame 
from options import *
from utils import *
from abstract import *
from copy import deepcopy

class Hitbox(Entity):
    def __init__(self, id, hitbox_options, state, parent, enemy):
        super().__init__(state)
        self.id = id
        self.state = state
        self.offsetx, self.offsety = hitbox_options["offset"]
        self.w, self.h = hitbox_options["dimensions"]
        self.damage = hitbox_options["damage"]
        self.kbx, self.kby = hitbox_options["knockback"]
        self.duration = hitbox_options["duration"]
        self.stun = hitbox_options["stun"]
        self.parent = parent
        self.mult = deepcopy(self.parent.mult)
        self.dead = False
        self.enemy = enemy
        self.x, self.y = self.parent.x + (-self.w if self.parent.facing == "l" else 0) + (-1 if self.parent.facing == "l" else 1) * self.offsetx, self.parent.y + self.offsety

    def tick(self,delta, entities): #collision in here
        super().tick(delta)
        self.x, self.y = self.parent.x + (-self.w if self.parent.facing == "l" else 0) + (-1 if self.parent.facing == "l" else 1) * self.offsetx, self.parent.y + self.offsety

        if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.w, self.h), pygame.Rect(self.enemy.x - HURTWIDTH/2, self.enemy.y - CATHEIGHT /2, HURTWIDTH, CATHEIGHT)):
            soundObj = pygame.mixer.Sound('assets/sfx/audioman.wav')
            soundObj.play()

            if self.parent.facing == "l":
                self.kbx = 0-self.kbx
            if not self.enemy.touchingFloor:
                self.kby = self.kby/2
            self.enemy.health -= self.damage * self.mult
            self.enemy.stun = self.stun
            self.enemy.accel(self.kbx, self.kby)
            self.enemy.canAttack = True
            self.enemy.jumping = 0
            self.parent.canAttack = True
            self.parent.attacking = HITCOOLDOWN
            self.state.hitboxes-=1
            self.dead = True
        self.duration -= delta
        if self.duration <= 0 and self.dead == False:
            soundObj = pygame.mixer.Sound('assets/sfx/clickman.wav')
            soundObj.play()

            self.state.hitboxes-=1
            self.dead = True
    
    def render(self, screen):
        if VIEWHITBOXES:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.w, self.h))
