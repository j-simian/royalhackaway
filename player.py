import pygame
from options import *
from utils import *
from abstract import *
from hitbox import *

class Player(EntityMovable):
    def __init__(self, id, state):
        super().__init__(state)
        self.lastdash = -1
        self.lastdashdir = 0
        self.id = id
        self.health = 100
        self.touchingFloor = True
        self.gravity = True #true if we are in air and fall
        self.moving = 0 #nonzero if needs to move
        self.jumping = 0 #positive if we need to jump
        self.charging = 0 #time until attack comes out
        self.attacking = 0 #time left in attack animation
        self.stun = 0 #time in stun
        self.canAttack = True
        self.healthbar = pygame.transform.scale(pygame.image.load("./assets/imgs/healthbar.png").convert_alpha(), (300, 100))

        self.sprite = [{"idler": pygame.image.load("./assets/imgs/cat1idle.png").convert_alpha(), "airr": pygame.image.load("./assets/imgs/cat1air.png").convert_alpha(), "attackr": pygame.image.load("./assets/imgs/cat1attack.png").convert_alpha(), "charger": pygame.image.load("./assets/imgs/cat1charge.png").convert_alpha()},
                       {"idler": pygame.image.load("./assets/imgs/cat2idle.png").convert_alpha(), "airr": pygame.image.load("./assets/imgs/cat2air.png").convert_alpha(), "attackr": pygame.image.load("./assets/imgs/cat2attack.png").convert_alpha(), "charger": pygame.image.load("./assets/imgs/cat2charge.png").convert_alpha()}]#load in drawn frames

        for n in [0, 1, 2, 3, 4]:
            self.sprite[0].update({"run" + str(n) + "r": pygame.image.load("./assets/imgs/cat1run" + str(n) + ".png").convert_alpha()})
            self.sprite[0].update({"run" + str(4-n) + "l": pygame.transform.flip(self.sprite[0]["run" + str(n) + "r"], True, False)})

        for n in [0, 1, 2, 3, 4, 5]:
            self.sprite[1].update({"run" + str(n) + "r": pygame.image.load("./assets/imgs/cat2run" + str(n) + ".png").convert_alpha()})
            self.sprite[1].update({"run" + str(5-n) + "l": pygame.transform.flip(self.sprite[1]["run" + str(n) + "r"], True, False)})

        for s in ["idle", "air", "charge", "attack"]:
            for c in [0, 1]:
                self.sprite[c].update({s + "l": pygame.transform.flip(self.sprite[c][s+"r"], True, False)})
                #mirrors frames
        #list of all possible frames. it's a list of dict's, #0 for cat 1 and #1 for cat 2, so we dont need 10000 if statements. indexed by id and mystate.
        for i in range(2):
            for key in self.sprite[i]:
                _image = self.sprite[i][key]
                self.sprite[i][key] = pygame.transform.smoothscale(_image, (int(CATSCALE*_image.get_width()), int(CATSCALE*_image.get_height())))

        self.mystate = "idle"
        self.facing = "l"
        #what this sprite is doing rn/how to display it

    def tick(self, delta, entities):
        super().tick(delta)

        self.tickAttack(delta, entities)
        self.stun -= delta
        # movement
        if self.moving !=0:
            if self.touchingFloor and self.attacking == 0 and self.charging == 0:
                self.accel(PLAYERACCEL*self.moving, 0)
            elif not self.touchingFloor and self.attacking == 0 and self.charging == 0:
                self.accel(AIRACCEL*self.moving, 0)
            else:
                pass
        if self.jumping != 0 and self.touchingFloor: #jumps iff on floor; jumping == scale of how high to jump
            self.y = GROUNDHEIGHT - 1; self.vely = JUMPVEL*self.jumping; self.mystate = "air"
            #makes you go off the ground and accelerates up to jump; makes jumping state 0 so we don't continue jumping
        if self.gravity:
            self.accel(0, GRAVITY*delta) #applies gravity
        self.touchingFloor = self.y >= GROUNDHEIGHT

        if self.touchingFloor: #makes you not falling if youre on ground
            if self.attacking == 0 and self.charging == 0:
                if abs(self.velx) < 0.1 or self.x <= CATWIDTH/2 or self.x >= self.state.WIDTH-CATWIDTH/2:
                    self.mystate = "idle"
                else:
                    self.mystate = "run" + str(int((self.x / 100) % (5 + self.id)))
            self.velx /= FRICTION
            self.vely = 0
            self.y = GROUNDHEIGHT
        else:
            self.velx /= AIRFRICTION #applies the right friction by reducing speed by dividing



    def tickAttack(self, delta, entities):
        if self.attacking>0:
            self.attacking-=delta
            if self.attacking<=0:
                self.attacking = 0
                self.canAttack = True
        if self.charging>0:

            self.charging -= delta
            if self.charging <= 0:
                self.charging = 0
                if self.stun<=0:
                    entities['hitbox' + str(self.state.hitboxes)] = Hitbox(self.state.hitboxes, attacks[self.attackType], self.state, self, entities["p"+str(int(2-self.id))])
                    self.state.hitboxes+=1
                    self.mystate = "attack"
                    self.attacking = COOLDOWNTIME * (2 if self.attackType == "heavy" else 1)


    def render(self, screen):
        self.facing = "l" if self.velx < 0 else "r"
        screen.blit(self.sprite[self.id][self.mystate + self.facing], (self.x - CATWIDTH/2, self.y - CATHEIGHT/2))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(self.x, self.y, 5, 5))

    def renderHealth(self, screen):
        screen.blit(self.healthbar, (self.id*780 + 100, 50))
        #pygame.draw.rect(screen, (127, 0, 0), healthbar)
        pygame.draw.rect(screen, (255, 0, 119), pygame.Rect(self.id*780 + 170, 83, 2.20*self.health, 15))
        pygame.draw.rect(screen, (145, 255, 217), pygame.Rect(self.id*780 + 170, 104, 186, 14))
