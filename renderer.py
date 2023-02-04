import pygame
from game_objects import *
from funs import *

class Renderer:
    
    def __init__(self, state):
        pygame.init()
        self.state = state
        self.width = self.state.WIDTH
        self.height = self.state.HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Nya Nya Revolution")
        pygame.display.flip()
        self.screen.fill((255, 255, 255))

    def renderFrame(self):
        (accuracy,whichNote)=onRhythm(pygame.mixer.music.get_pos()/1000, 0, 110)

        if (accuracy=="perfect" and whichNote==0):
            self.screen.fill((255, 255, 255))
        else:
            self.screen.fill((230, 230, 230))


        for entity in entities.values():
            entity.render(self.screen)
        pygame.display.flip()

    def renderMenu(self, menu):
        menu.render(self.screen)

