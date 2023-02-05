import pygame
from handle_input import *
from funs import *
import pygame_menu

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
        self.bgbeat2 = pygame.transform.scale(self.bg, (self.width+8, self.height+4))
        self.overlay = pygame.Surface((self.width,self.height))  # the size of your rect
        self.overlay.set_alpha(128)                # alpha level
        self.overlay.fill((255, 0, 119))           # this fills the entire surface
        pygame.display.set_caption("Nyance Nyance Revolution: Beat Beat-Up")
        pygame.display.flip()
        self.screen.fill((255, 255, 255))

    def renderFrame(self, timer, entities):
        self.renderBG(timer)
        self.renderHUD(entities)
        self.renderEntities(entities)

    def blitScreen(self):
        pygame.display.flip()

    def renderBG(self, timer):
        (accuracy,whichNote)=timer.onRhythm()
        if (accuracy=="perfect" and whichNote==0 and FLASH):
            self.screen.blit(self.bgbeat, (-16, -9))
        elif (accuracy=="perfect" and whichNote==1 and FLASH):
            self.screen.blit(self.bgbeat2, (-4, -2))
        else:
            self.screen.blit(self.bg, (0, 0))

    def renderHUD(self, entities):
        entities["p1"].renderHealth(self.screen)
        entities["p2"].renderHealth(self.screen)
        self.font = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 30)
        for c in range (0,2):
            _text = self.font.render(self.state.names[c], True, (255, 0, 119))
            self.screen.blit(_text, (c*780 + 180, 11))
        entities["p1"].renderText(self.screen)
        entities["p2"].renderText(self.screen)
        entities["p1"].renderCombo(self.screen)
        entities["p2"].renderCombo(self.screen)


    def renderEntities(self, entities):
        for entity in entities.values():
            entity.render(self.screen)

    def renderMenu(self, menu):
        menu.render(self.screen)

    def renderDeath(self, entities):
        self.font = pygame.font.Font(pygame_menu.font.FONT_8BIT, 100)
        _winner = self.state.names[0] if entities["p1"].health > 0 else self.state.names[1]
        _text = self.font.render(_winner + " wins", True, (255,255,255))
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(_text, (self.width/2 - _text.get_width()/2, self.height/2 - _text.get_height()/2))
        #deathmenu.render(self.screen)