import pygame
from utils import *

GRAVITY = 0.001
MAXVELY = 20
MAXVELX = 0.5
FRICTION = 1.05
AIRFRICTION = 1.01
PLAYERACCEL = 2
AIRACCEL = 0.02
JUMPVEL = -0.5
GROUNDHEIGHT = 500

entities = {}
def initEntities(state):
    p1 = Player(0, state)
    p2 = Player(1, state)
    p1.x = 200
    p2.x = 600
    p1.y = 400
    p2.y = 400
    entities["p1"] = p1
    entities["p2"] = p2


def handleMove(player, control, event):
    if event.type == pygame.KEYDOWN:
        if event.key == control['left']:
            player.moving = -1
        if event.key == control['right']:
            player.moving = 1
        if event.key == control['up']:
            player.jumping = 1

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
        if event.key == control['up'] and player.jumping > 0:
            player.jumping = 0

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
        self.gravity = True
    def tick(self, delta):
        super().tick(delta)
        #if self.gravity:
        #    self.vely += GRAVITY*delta
        self.vely = clamp(-MAXVELY, self.vely, MAXVELY)
        self.velx = clamp(-MAXVELX, self.velx, MAXVELX)
        self.x += self.velx*delta
        self.y += self.vely*delta
        self.x = clamp(0, self.x, self.state.WIDTH-40)
    def accel(self, x, y):
        self.velx += x
        self.vely += y

class Player(EntityMovable):
    def __init__(self, id, state):
        super().__init__(state)
        self.id = id
        self.health = 100
        self.touchingFloor = True
        self.gravity = True #true if we are in air and fall
        self.moving = 0 #nonzero if needs to move
        self.jumping = 0 #positive if we ned to jump
    def tick(self, delta):
        super().tick(delta)
        if self.moving !=0:
            if self.touchingFloor:
                self.accel(PLAYERACCEL*self.moving, 0)
            else:
                self.accel(AIRACCEL*self.moving, 0)
        if self.jumping != 0 and self.touchingFloor: #jumps iff on floor; jumping == scale of how high to jump
            self.y = GROUNDHEIGHT - 1; self.vely = JUMPVEL*self.jumping; self.gravity = True
            #makes you go off the ground and accelerates up to jump; makes jumping state 0 so we don't continue jumping
        if self.gravity:
            self.accel(0, GRAVITY*delta) #applies gravity
        self.touchingFloor = self.y >= GROUNDHEIGHT

        if self.touchingFloor: #makes you not falling if youre on ground
            self.velx /= FRICTION
            self.vely = 0
            self.y = GROUNDHEIGHT
            self.gravity = False
        else:
            self.velx /= AIRFRICTION #applies the right friction by reducing speed by dividing

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 255) if self.id == 1 else (0, 255, 255), pygame.Rect(self.x, self.y, 40, 100))
        self.renderHealth(screen)

    def renderHealth(self, screen):
        health_bar = pygame.Rect(0, 0, 640, 50) if self.id == 0 else pygame.Rect(640, 0, 640, 50)
        pygame.draw.rect(screen, (127, 0, 0), health_bar)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0 if self.id == 0 else 1280-640.0*self.health/100.0, 0, 640.0*self.health/100.0, 50))
