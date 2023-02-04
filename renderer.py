import pygame

class Renderer:
    def initRenderer(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Nya Nya Revolution")
        pygame.display.flip()
        self.screen.fill((255, 255, 255))

    def gameLoop(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.screen.fill((255, 255, 255))
                pygame.display.flip()
                if event.type == pygame.QUIT:
                    running = False

    def renderMenu(self, menu):
        menu.render(self.screen)

