import pygame
import pygame_menu

pygame.init()


class Menu():
    def __init__(self, state) -> None:
        self.state = state
    def set_controls(self, player, controls):
        self.state.controls[player] = controls
        # 0: wasd, 1: ijkl

    def start_the_game(self):
    # Do the job here !
        if self.state.controls[0] != self.state.controls[1]:
            self.state.screen = 1
            self.menu.disable()
    def render(self, screen):
        self.menu = pygame_menu.Menu('Welcome', 400, 400,
                       theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input('Name :', default='Catgirl 1')
        self.menu.add.selector('Player 1 Controls:', [["wasd",0], ["ijkl",1]], onchange=(lambda _, y: self.set_controls(0, y)))
        self.menu.add.selector('Player 2 Controls:', [["ijkl",1], ["wasd",0]], onchange=(lambda _, y: self.set_controls(1, y)))
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.mainloop(screen)