import pygame

GRAVITY = 0.000025
MAXVELY = 20
MAXVELX = 0.2
FRICTION = 1.1
PLAYERACCEL = 2
JUMPVEL = -2
GROUNDHEIGHT = 400

entities = {}
def clampAbs(value, limit):
    right = limit
    left = - limit
    if value < left:
        value = left
    if value > right:
        value = right
    return value
def initEntities():
    p1 = Player(0)
    p2 = Player(1)
    p1.x = 200
    p2.x = 600
    p1.y = 400
    p2.y = 400
    entities["p1"] = p1
    entities["p2"] = p2


class Entity:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 100, 100))

    def tick(self, delta):
        pass

class EntityMovable(Entity):
    def __init__(self):
        super().__init__()
        self.velx = 0
        self.vely = 0
        self.gravity = True
    def tick(self, delta):
        super().tick(delta)
        if self.gravity:
            self.vely += GRAVITY*delta
        self.vely = clampAbs(self.vely, MAXVELY)
        self.velx = clampAbs(self.velx, MAXVELX)
        self.x += self.velx*delta
        self.y += self.vely*delta
    def accel(self, x, y):
        self.velx += x
        self.vely += y

class Player(EntityMovable):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.health = 100
        self.touchingFloor = True
        self.gravity = not self.touchingFloor
        self.moving = 0
        self.jumping = 0
    def tick(self, delta):
        super().tick(delta)
        if self.moving !=0:
            self.accel(PLAYERACCEL*self.moving, 0)
        if self.jumping != 0:
            self.vely = JUMPVEL*self.jumping; self.jumping = 0
        self.touchingFloor = self.y >= GROUNDHEIGHT
        self.gravity = not self.touchingFloor
        if self.touchingFloor:
            self.velx /= FRICTION
    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 255) if self.id == 1 else (0, 255, 255), pygame.Rect(self.x, self.y, 40, 100))
