import pygame
import pygame_menu

pygame.init()


class Menu():
    def __init__(self, state) -> None:
        self.state = state
    def set_difficulty(self, value, difficulty):
    # Do the job here !
        pass

    def start_the_game(self):
    # Do the job here !
        self.state.screen = 1
        self.menu.disable()
    def render(self, screen):
        self.menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input('Name :', default='Catgirl 1')
        self.menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.mainloop(screen)