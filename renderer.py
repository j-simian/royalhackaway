import pygame
from game_objects import *
from funs import *

FLASH = True

class Renderer:
    def __init__(self, state):
        pygame.init()
        self.state = state
        self.width = self.state.WIDTH
        self.height = self.state.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load("./assets/imgs/bg.png").convert()
        self.bgbeat = pygame.transform.scale(self.bg, (self.width+32, self.height+18))
        pygame.display.set_caption("Nya Nya Revolution")
        pygame.display.flip()
        self.screen.fill((255, 255, 255))

    def renderFrame(self, timer, entities):
        (accuracy,whichNote)=timer.onRhythm()
        if (accuracy=="perfect" and whichNote==0 and FLASH):
            self.screen.blit(self.bgbeat, (-16, -9))
        else:
            self.screen.blit(self.bg, (0, 0))

        entities["p1"].renderHealth(self.screen)
        entities["p2"].renderHealth(self.screen)
        for entity in entities.values():
            entity.render(self.screen)
        pygame.display.flip()

    def renderMenu(self, menu):
        menu.render(self.screen)
