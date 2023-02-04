import pygame
from utils import *
from funs import *
from options import *


def initEntities(state):
    entities = {}
    p1 = Player(0, state)
    p2 = Player(1, state)
    p1.x = 200
    p2.x = 600
    p1.y = GROUNDHEIGHT
    p2.y = GROUNDHEIGHT
    hitbox = Hitbox(0, {"dimensions": (200, 50), "offset": (-100, -150), "damage": 10, "knockack": (10, 10), "duration": 100000, "knockback": (10, 10)}, state, p1)
    entities["p1"] = p1
    entities["p2"] = p2
    entities["hitb"] = hitbox
    return entities


def dashAvailable(accuracy, player, frame):
    return accuracy == 'perfect' and (player.lastdash+1/2<frame or player.lastdashdir!=player.moving)


def handlePress(event, timer, player, control):
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

def handleRelease(event, player, control):
    if event.key == control['left'] and player.moving == -1:
        player.moving = 0
        if pygame.key.get_pressed()[control['right']]:
            player.moving = 1
    if event.key == control['right'] and player.moving == 1:
        player.moving = 0
        if pygame.key.get_pressed()[control['left']]:
            player.moving = -1
    if event.key == control['down']:
        player.charging = 0.1
    if event.key == control['up'] and player.jumping > 0:
        player.jumping = 0

def handleMove(player, control, event, timer, state):
    if event.type == pygame.KEYDOWN:
        handlePress(event, timer, player, control)

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
        self.vely = clampAbs(self.vely, MAXVELY)
        self.velx = clampAbs(self.velx, MAXVELX+self.dash)
        self.x += self.velx*delta
        self.y += self.vely*delta
        self.x = clamp(0, self.x, self.state.WIDTH-CATWIDTH)
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

        self.healthbar = pygame.transform.scale(pygame.image.load("./assets/imgs/healthbar.png").convert_alpha(), (200, 100))

        self.sprite = [{"idler": pygame.image.load("./assets/imgs/cat1idle.png").convert_alpha(), "airr": pygame.image.load("./assets/imgs/cat1air.png").convert_alpha()},
                       {"idler": pygame.image.load("./assets/imgs/cat2idle.png").convert_alpha(), "airr": pygame.image.load("./assets/imgs/cat2air.png").convert_alpha()}] #load in drawn frames

        for s in ["idle", "air"]:
            for c in [0, 1]:
                self.sprite[c].update({s + "l": pygame.transform.flip(self.sprite[c][s+"r"], True, False)})
                #mirrors frames
        #list of all possible frames. it's a list of dict's, #0 for cat 1 and #1 for cat 2, so we dont need 10000 if statements. indexed by id and mystate.

        self.mystate = "idle"
        self.facing = "l"
        #what this sprite is doing rn/how to display it

    def tick(self, delta):
        super().tick(delta)

        self.attacking -= delta
        if self.charging>0:
            self.charging -= delta
            if self.charging <= 0:
                self.charging = 0
                ##ATTACK
                self.attacking = 0.4

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
            self.mystate = "idle"
            self.velx /= FRICTION
            self.vely = 0
            self.y = GROUNDHEIGHT
            self.gravity = False
        else:
            self.velx /= AIRFRICTION #applies the right friction by reducing speed by dividing

    def render(self, screen):
        self.facing = "l" if self.velx < 0 else "r"
        screen.blit(self.sprite[self.id][self.mystate + self.facing], (self.x - CATWIDTH, self.y - CATHEIGHT))

    def renderHealth(self, screen):
        screen.blit(self.healthbar, (self.id*400 + 100, 50))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0 if self.id == 0 else 1280-640.0*self.health/100.0, 0, 640.0*self.health/100.0, 50))

class Hitbox(Entity):
    def __init__(self, id, hitbox_options, state, parent):
        super().__init__(state)
        self.id = id
        self.offsetx, self.offsety = hitbox_options["offset"]
        self.w, self.h = hitbox_options["dimensions"]
        self.damage = hitbox_options["damage"]
        self.kbx, self.kby = hitbox_options["knockback"]
        self.duration = hitbox_options["duration"]
        self.parent = parent
        self.dead = False

    def tick(self,delta): #collision in here
        super().tick(delta)
        self.x, self.y = self.parent.x + (-self.w-CATWIDTH if self.parent.facing == "l" else 0) + (-1 if self.parent.facing == "l" else 1) * self.offsetx, self.parent.y + self.offsety 
        
        self.duration -= delta
        if self.duration <= 0:
            self.dead = True

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.w, self.h))
