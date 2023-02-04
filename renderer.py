import pygame
from game_objects import *
from funs import *

FLASH = False

class Renderer:
    def __init__(self, state):
        pygame.init()
        self.state = state
        self.width = self.state.WIDTH
        self.height = self.state.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load("./assets/imgs/bg.png").convert()
        pygame.display.set_caption("Nya Nya Revolution")
        pygame.display.flip()
        self.screen.fill((255, 255, 255))

    def renderFrame(self):
        (accuracy,whichNote)=onRhythm(pygame.mixer.music.get_pos()/1000, 0, 110)

        if (accuracy=="perfect" and whichNote==0 and FLASH):
            self.screen.fill((255, 255, 255))
        else:
            self.screen.blit(self.bg, (0, 0))


        for entity in entities.values():
            entity.render(self.screen)
        pygame.display.flip()

    def renderMenu(self, menu):
        menu.render(self.screen)

