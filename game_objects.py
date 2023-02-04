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
    p1.y = 400
    p2.y = 400
    entities["p1"] = p1
    entities["p2"] = p2
    return entities

def handleMove(player, control, event, timer, state):
    if event.type == pygame.KEYDOWN:
        (accuracy,whichNote)=timer.onRhythm(False)
        frame = timer.getFullFrame()
        #print(frame)
        if event.key == control['left']:
            player.moving = -1
            if accuracy == 'perfect' and (player.lastdash+1/2<frame or player.lastdashdir!=player.moving):
                player.lastdash = frame + whichNote/2
                player.lastdashdir = player.moving
                player.dash+=MAXVELX*DASHRATIO
        if event.key == control['right']:
            player.moving = 1
            if accuracy == 'perfect' and (player.lastdash+1/2<frame or player.lastdashdir!=player.moving):
                player.lastdash = frame + whichNote/2
                player.lastdashdir = player.moving
                player.dash+=MAXVELX*DASHRATIO
        if event.key == control['up']:
            player.jumping = 0.6

    if event.type == pygame.KEYUP:
        if event.key == control['left'] and player.moving == -1:
            if pygame.key.get_pressed()[control['right']]:
                player.moving = 1
            else:
                player.moving = 0
        if event.key == control['right'] and player.moving == 1:
            if pygame.key.get_pressed()[control['left']]:
                player.moving = -1
            else:
                player.moving = 0
        if event.key == control['down']:
            player.charging = 0.1
        if event.key == control['up'] and player.jumping > 0:
            player.jumping = 0

class Entity:
    def __init__(self, state):
        self.x = 0.0
        self.y = 0.0
        self.state = state
    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 100, 100))


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
        self.vely = clamp(-MAXVELY, self.vely, MAXVELY)
        self.velx = clamp(-MAXVELX - self.dash, self.velx, MAXVELX+self.dash)
        self.x += self.velx*delta
        self.y += self.vely*delta
        self.x = clamp(0, self.x, self.state.WIDTH-40)
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
        self.comboNum = 0 #which hit of combo (currently unused)

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
        self.renderHealth(screen)

    def renderHealth(self, screen):
        screen.blit(self.healthbar, (self.id*400 + 100, 50))
        #pygame.draw.rect(screen, (127, 0, 0), healthbar)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0 if self.id == 0 else 1280-640.0*self.health/100.0, 0, 640.0*self.health/100.0, 50))

class Hitbox(Entity):
    def __init__(self, id, offset, dimensions, damage, knockback, stun, duration, state, parent):
        super().__init__(state)
        self.id = id
        self.offsetx, self.offsety = offset #offset from x,y coords of parent NOTE: also consider direction player is facing
        self.w, self.h = dimensions
        self.damage = damage
        self.kbx, self.kby = knockback
        self.stun = stun                    #amount of time the opponent can't act for when getting hit by this
        self.duration = duration            #amount of time before the hitbox disappears
        self.parent = parent                #player the hitbox is attached to

    def tick(self,delta): #collision in here
        super().tick(delta)
        self.x, self.y = self.parent.x, self.parent.y #NOTE: also consider direction player is facing
        self.duration -= delta
        if self.duration <= 0:
            pass #remove this object