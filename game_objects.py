import pygame

GRAVITY = 0.025

entities = []

def initEntities():
    e = Entity()
    e.gravity = True
    entities.append(e)


class Entity:
    x = 0.0
    y = 0.0
    gravity = False

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 100, 100))

    def tick(self, delta):
        if self.gravity:
            self.y += GRAVITY*delta

class EntityMovable(Entity):
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
