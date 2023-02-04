import pygame
import pygame_menu

pygame.init()


class Menu():
    def __init__(self) -> None:
        pass
    def set_difficulty(self, value, difficulty):
    # Do the job here !
        pass

    def start_the_game(self):
    # Do the job here !
        pass
    def render(self, screen):
        menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

        menu.add.text_input('Name :', default='Catgirl 1')
        menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=self.set_difficulty)
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(screen)