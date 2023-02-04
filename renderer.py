import pygame
from game_objects import *

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
        self.screen.fill((255, 255, 255))
        for entity in entities:
            entity.render(self.screen)
        pygame.display.flip()

    def renderMenu(self, menu):
        menu.render(self.screen)

