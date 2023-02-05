import pygame
from options import *
from utils import *
from abstract import *
from hitbox import *
import pygame_menu

class Player(EntityMovable):
    def __init__(self, id, state):
        super().__init__(state)
        self.lastdash = -1
        self.lastdashdir = 0
        self.id = id
        self.health = 100
        self.energy = 0
        self.touchingFloor = True
        self.gravity = True #true if we are in air and fall
        self.moving = 0 #nonzero if needs to move
        self.jumping = 0 #positive if we need to jump
        self.charging = 0 #time until attack comes out
        self.attacking = 0 #time left in attack animation
        self.stun = 0 #time in stun
        self.hitglow = 0 #time left glowing
        self.lasthitframe = -1
        self.combo = 0
        self.mult = 1
        self.canAttack = True
        self.healthbar = pygame.transform.scale(pygame.image.load("./assets/imgs/healthbar.png").convert_alpha(), (300, 100))
        self.text = ""
        self.textopacity = 0 #clear
        self.textx, self.texty = 500, 500
        self.textactive = False
        self.font = pygame.font.Font(pygame_menu.font.FONT_8BIT, 20)
        self.textimg = self.font.render(self.text, True, (255,255,255))
        self.comboopacity = 0
        self.comboimg = self.font.render("COMBO 0", True, (255,255,255))
        self.combofont = pygame.font.Font(pygame_menu.font.FONT_8BIT, 50)

        self.sprite = [{}, {}]
        for s in ["idle", "air", "charge", "attack", "hit", "heavy", "hvcharge", "die"]:
            for c in [0, 1]:
                self.sprite[c].update({s + "r": pygame.image.load("./assets/imgs/cat" + str(c+1) + s + ".png").convert_alpha()})

        for n in [0, 1, 2, 3, 4]:
            self.sprite[0].update({"run" + str(n) + "r": pygame.image.load("./assets/imgs/cat1run" + str(n) + ".png").convert_alpha()})
            self.sprite[0].update({"run" + str(4-n) + "l": pygame.transform.flip(self.sprite[0]["run" + str(n) + "r"], True, False)})

        for n in [0, 1, 2, 3, 4, 5]:
            self.sprite[1].update({"run" + str(n) + "r": pygame.image.load("./assets/imgs/cat2run" + str(n) + ".png").convert_alpha()})
            self.sprite[1].update({"run" + str(5-n) + "l": pygame.transform.flip(self.sprite[1]["run" + str(n) + "r"], True, False)})

        for s in ["idle", "air", "charge", "attack", "hit", "heavy", "hvcharge", "die"]:
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

    def accel(self, x, y):
        if self.stun > 0:
            super().accel(STUNSPEED*x, y)
        else:
            super().accel(x, y)

    def tick(self, delta, entities):
        super().tick(delta)

        self.tickAttack(delta, entities)
        self.energy = max(0,self.energy-delta/10)
        self.hitglow -= delta
        self.stun -= delta
        # movement
        if self.moving !=0:
            if self.touchingFloor and self.attacking == 0 and self.charging == 0 and self.stun <= 0:
                self.accel(PLAYERACCEL*self.moving, 0)
            elif not self.touchingFloor:
                self.accel(AIRACCEL*self.moving, 0)
            else:
                pass
        if self.jumping != 0 and self.touchingFloor: #jumps iff on floor; jumping == scale of how high to jump
            self.y = GROUNDHEIGHT - 1; self.vely = JUMPVEL*self.jumping; self.mystate = "air"
            #makes you go off the ground and accelerates up to jump; makes jumping state 0 so we don't continue jumping
            self.jumping = 0
        #if self.gravity:
        #    self.accel(0, GRAVITY*delta) #applies gravity

        nextTouchingFloor = self.y >= GROUNDHEIGHT
        if nextTouchingFloor and not self.touchingFloor: #just landed
            self.attacking = min(self.attacking,HITCOOLDOWN)
        self.touchingFloor = nextTouchingFloor

        if self.touchingFloor: #makes you not falling if youre on ground
            if self.attacking == 0 and self.charging == 0 and self.stun <= 0:
                if abs(self.velx) < 0.1 or self.x <= CATWIDTH/2 or self.x >= self.state.WIDTH-CATWIDTH/2:
                    self.mystate = "idle"
                else:
                    self.mystate = "run" + str(int((self.x / 100) % (5 + self.id)))
            self.velx /= FRICTION
            self.vely = 0
            self.y = GROUNDHEIGHT
        else:
            self.velx /= AIRFRICTION #applies the right friction by reducing speed by dividing
        if self.stun > 0: self.mystate = "hit"

        if self.textactive:
            self.textopacity -= delta/4
        if self.textopacity < 0:
            self.textopacity = 0
            self.textactive = False

        if self.comboopacity > 2:
            self.comboopacity -= delta/4
        else:
            self.comboopacity = 0

        if self.dashing(): #we've done a perfect
            self.textset("Perfect", (self.x, self.y - CATHEIGHT*CATSCALE/2))
        if self.hitglow>0:
            self.textactive = False #lets us repeatedly have hit text
            self.textset("perfect hit", (self.x, self.y - CATHEIGHT*CATSCALE/2))

        self.comboset()



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
                    self.mystate = "heavy" if self.attackType == "heavy" else "attack"
                    self.attacking = COOLDOWNTIME * (2 if self.attackType == "heavy" else 1)


    def render(self, screen):
        if self.attacking<=0:
            self.facing = "l" if self.velx < 0 else "r"

        if self.dashing() or self.hitglow>0: #for dash effects - makes cat brighter
            _image = self.sprite[self.id][self.mystate + self.facing].copy()
            _image.fill([(217, 255, 244), (255,179,196)][self.id], special_flags=pygame.BLEND_RGB_MAX) #
            screen.blit(_image, (self.x - CATWIDTH/2, self.y - CATHEIGHT/2))
        else:
            screen.blit(self.sprite[self.id][self.mystate + self.facing], (self.x - CATWIDTH/2, self.y - CATHEIGHT/2))

    def renderHealth(self, screen):

        screen.blit(self.healthbar, (self.id*780 + 100, 35))

        pygame.draw.rect(screen, (255, 0, 119), pygame.Rect(self.id*780 + 170, 68, 2.20*self.health, 15))
        pygame.draw.rect(screen, (145, 255, 217), pygame.Rect(self.id*780 + 170, 89, 1.86*self.energy, 14))

    def textset(self, text, pos):
        if not self.textactive:
            self.textactive = True
            self.text = text
            self.textx, self.texty = pos
            self.textopacity = 370 #opaque
            self.textimg = self.font.render(self.text, True, (255,255,255))

    def renderText(self, screen):
        if self.textactive:
            self.textimg.set_alpha(min(self.textopacity, 255))
            screen.blit(self.textimg, (self.textx - self.textimg.get_width()/2, self.texty - self.textimg.get_height()/2))
        else:
            pass

    def comboset(self):
        if self.combo > 0.1:
            #self.comboactive = True
            #self.text = text
            #self.textx, self.texty = pos
            self.comboopacity = 370 #opaque
            self.comboimg = self.combofont.render("combo " + str(self.combo), True, (255,255,255))

    def renderCombo(self, screen):
        if self.comboopacity > 2:
            self.comboimg.set_alpha(min(self.comboopacity, 255))
            screen.blit(self.comboimg, (640 - self.comboimg.get_width()/2, 600 - self.comboimg.get_height()/2))
        else:
            pass