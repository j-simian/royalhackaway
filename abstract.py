import pygame
from options import *
from utils import *
import pygame_menu

class Entity:
    def __init__(self, state):
        self.x = 0.0
        self.y = 0.0
        self.state = state
    #def render(self, screen):
    #    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 100, 100))

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
        if self.gravity:
            self.vely += GRAVITY*delta
        self.vely = clampAbs(self.vely, MAXVELY)
        self.velx = clampAbs(self.velx, MAXVELX+self.dash)
        self.x += self.velx*delta
        self.y = min(self.y+self.vely*delta, GROUNDHEIGHT)
        self.x = clamp(CATWIDTH/2 - 120, self.x, self.state.WIDTH-CATWIDTH/2 + 120) #INVISIBLE WALLS DEFINED HERE! 100 = magic number
        self.dash=max(self.dash-DASHDECREASE*delta,0)
    def accel(self, x, y):
        self.velx += x
        self.vely += y
    def dashing(self):
        return self.dash > 0