import pygame

GRAVITY = 0.0005
MAXVELY = 20

entities = []

def initEntities():
    e = EntityMovable()
    e.gravity = True
    entities.append(e)


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
        self.vely = min(self.vely, MAXVELY)
        self.x += self.velx
        self.y += self.vely
    def accel(self, x, y):
        self.velx += x
        self.vely += y
