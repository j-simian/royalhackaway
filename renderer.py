import pygame

class Renderer:


    def initRenderer(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()
        pygame.display.set_caption("Nya Nya Revolution")
        self.screen.fill((255, 255, 255))

    def gameLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

renderer = Renderer()
renderer.initRenderer()
renderer.gameLoop()
