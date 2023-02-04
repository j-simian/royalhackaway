import pygame
from utils import *
from funs import *
from options import *


def initEntities(state):
    entities = {}
    p1 = Player(0, state)
    p2 = Player(1, state)
    p1.x, p2.x = 200, 600
    p1.y, p2.y = GROUNDHEIGHT, GROUNDHEIGHT
    entities["p1"], entities["p2"] = p1, p2
    return entities


def dashAvailable(accuracy, player, frame):
    return accuracy == 'perfect' and (player.lastdash+1/2<frame or player.lastdashdir!=player.moving)


def handlePress(event, timer, player, control, state, enemy, entities):
    (accuracy,whichNote)=timer.onRhythm(False)
    frame = timer.getFullFrame()
    available = dashAvailable(accuracy, player, frame)
    if available and event.key in [control['left'], control['right']]:
        player.lastdash = frame + whichNote/2
        player.lastdashdir = player.moving
        player.dash+=MAXVELX*DASHRATIO
    if event.key == control['left']:
        player.moving = -1
    if event.key == control['right']:
        player.moving = 1
    if event.key == control['up']:
        player.jumping = 0.6
    if event.key == control['attack']:
        if player.canAttack == True:
            if timer.isHalfFrame():
                player.attackType = "heavy"
            else:
                player.attackType = "light"
            player.mystate = "charge"
            player.charging = CHARGETIME
            player.canAttack = False

def handleRelease(event, player, control):
    if event.key == control['left'] and player.moving == -1:
        player.moving = 0
        if pygame.key.get_pressed()[control['right']]:
            player.moving = 1
    if event.key == control['right'] and player.moving == 1:
        player.moving = 0
        if pygame.key.get_pressed()[control['left']]:
            player.moving = -1
    if event.key == control['up'] and player.jumping > 0:
        player.jumping = 0

def handleMove(player, control, event, timer, state, enemy, entities):
    if event.type == pygame.KEYDOWN:
        handlePress(event, timer, player, control, state, enemy, entities)
    if event.type == pygame.KEYUP:
        handleRelease(event, player, control)

class Entity:
    def __init__(self, state):
        self.x = 0.0
        self.y = 0.0
        self.state = state
    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 100, 100))

    def tick(self, delta):
        pass

class EntityMovable(Entity):
    def __init__(self, state):
        super().__init__(state)
        self.velx = 0
        self.vely = 0
        self.dash = 0
        self.gravity = True
    def tick(self, delta):
        super().tick(delta)
        #if self.gravity:
        #    self.vely += GRAVITY*delta
        self.vely = softClamp(self.vely, MAXVELY)
        self.velx = clampAbs(self.velx, MAXVELX+self.dash)
        self.x += self.velx*delta
        self.y += self.vely*delta
        self.x = clamp(CATWIDTH/2, self.x, self.state.WIDTH-CATWIDTH/2)
        self.dash/=FRICTION
    def accel(self, x, y):
        self.velx += x
        self.vely += y

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

        for n in ["0", "1", "2", "3", "4"]:
            self.sprite[0].update({"run" + n + "r": pygame.image.load("./assets/imgs/cat1run" + n + ".png").convert_alpha()})
            self.sprite[0].update({"run" + n + "l": pygame.transform.flip(self.sprite[0]["run" + n + "r"], True, False)})

        for n in ["0", "1", "2", "3", "4", "5"]:
            self.sprite[1].update({"run" + n + "r": pygame.image.load("./assets/imgs/cat2run" + n + ".png").convert_alpha()})
            self.sprite[1].update({"run" + n + "l": pygame.transform.flip(self.sprite[1]["run" + n + "r"], True, False)})

        for s in ["idle", "air", "charge", "attack"]:
            for c in [0, 1]:
                self.sprite[c].update({s + "l": pygame.transform.flip(self.sprite[c][s+"r"], True, False)})
                #mirrors frames
        #list of all possible frames. it's a list of dict's, #0 for cat 1 and #1 for cat 2, so we dont need 10000 if statements. indexed by id and mystate.

        for key in self.sprite[0]:
            _image = self.sprite[0][key]
            self.sprite[0][key] = pygame.transform.smoothscale(_image, (int(CATSCALE*_image.get_width()), int(CATSCALE*_image.get_height())))

        for key in self.sprite[1]:
            _image = self.sprite[1][key]
            self.sprite[1][key] = pygame.transform.smoothscale(_image, (int(CATSCALE*_image.get_width()), int(CATSCALE*_image.get_height())))

        self.mystate = "idle"
        self.facing = "l"
        #what this sprite is doing rn/how to display it

    def tick(self, delta, entities):
        super().tick(delta)

        self.tickAttack(delta, entities)
        self.stun -= delta
        # movement
        if self.moving !=0:
            if self.touchingFloor:
                self.accel(PLAYERACCEL*self.moving, 0)
            else:
                self.accel(AIRACCEL*self.moving, 0)
        if self.jumping != 0 and self.touchingFloor: #jumps iff on floor; jumping == scale of how high to jump
            self.y = GROUNDHEIGHT - 1; self.vely = JUMPVEL*self.jumping; self.gravity = True; self.mystate = "air"
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
            self.gravity = False
        else:
            self.velx /= AIRFRICTION #applies the right friction by reducing speed by dividing

    def tickAttack(self, delta, entities):
        if self.attacking>0:
            self.attacking-=delta
            if self.attacking<=0:
                self.mystate = "idle"
                self.attacking = 0
                self.canAttack = True
        if self.charging>0:

            self.charging -= delta
            if self.charging <= 0:
                self.charging = 0
                entities['hitbox' + str(self.state.hitboxes)] = Hitbox(self.state.hitboxes, attacks[self.attackType], self.state, self, entities["p"+str(int(2-self.id))])
                self.state.hitboxes+=1
                self.mystate = "attack"
                self.attacking = COOLDOWNTIME * 2 if self.attackType == "heavy" else 1


    def render(self, screen):
        self.facing = "l" if self.velx < 0 else "r"
        screen.blit(self.sprite[self.id][self.mystate + self.facing], (self.x - CATWIDTH/2, self.y - CATHEIGHT/2))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(self.x, self.y, 5, 5))

    def renderHealth(self, screen):
        screen.blit(self.healthbar, (self.id*780 + 100, 50))
        #pygame.draw.rect(screen, (127, 0, 0), healthbar)
        pygame.draw.rect(screen, (255, 0, 119), pygame.Rect(self.id*780 + 170, 83, 2.20*self.health, 15))
        pygame.draw.rect(screen, (145, 255, 217), pygame.Rect(self.id*780 + 170, 104, 186, 14))

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
        self.dead = False
        self.enemy = enemy
        self.x, self.y = self.parent.x + (-self.w if self.parent.facing == "l" else 0) + (-1 if self.parent.facing == "l" else 1) * self.offsetx, self.parent.y + self.offsety

    def tick(self,delta, entities): #collision in here
        super().tick(delta)
        self.x, self.y = self.parent.x + (-self.w if self.parent.facing == "l" else 0) + (-1 if self.parent.facing == "l" else 1) * self.offsetx, self.parent.y + self.offsety

        if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.w, self.h), pygame.Rect(self.enemy.x - CATWIDTH/2, self.enemy.y - CATHEIGHT /2, CATWIDTH, CATHEIGHT)):
            if self.parent.facing == "l":
                self.kbx = 0-self.kbx
            self.enemy.health -= self.damage
            self.enemy.stun = self.stun
            self.enemy.velx = 0
            self.enemy.vely = 0
            self.enemy.accel(self.kbx, self.kby)
            self.state.hitboxes-=1
            self.dead = True
        self.duration -= delta
        if self.duration <= 0 and self.dead == False:
            self.state.hitboxes-=1
            self.dead = True

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.w, self.h))
